# -*- coding: utf-8 -*-

from vm import VM
from tsymbol import tsym
from environment import Frame
from tpair import to_python_list, from_python_list, to_str
from scmlib import *
from errors import *
from insts import *
from syntax import *
from trampoline import *

def label_generator():
    """Produce a label generator.
    """
    counter = 0
    def f():
        nonlocal counter
        counter += 1
        return 'label%d' % (counter - 1)
    return f


label = label_generator()


def resolve_label(code):
    """Resolve all the labels in the instructions. Labels
    will all be replaced by offset from the target instruction
    to the current one.
    """
    label2addr = {}
    tmp = []
    # get address of all labels
    for i in range(len(code)):
        if isinstance(code[i], tuple):
            tmp.append(code[i])
        else:
            label2addr[code[i]] = len(tmp)
    # convert labels
    insts = []
    for i in range(len(tmp)):
        if tmp[i][0] in (inst_j, inst_jt, inst_jf):
            insts.append((tmp[i][0], label2addr[tmp[i][1]] - i))
        else:
            insts.append(tmp[i])
    return insts


def define_dumb(exps, env):
    """Return the instructions to bind the names in 
    `varl' in `env' to None, indicating that those are unassigned. 
    Later definition forms will set them to actual values.
    Return the code to bind names at runtime.
    """
    # this is for the toplevel definitions, convert
    # the python list of expressions into a Scheme list
    # to work with scanout_defs()
    if not isinstance(exps, Pair):
        exps = lib_list(*exps)

    varl = scanout_defs(exps)
    if varl != []:
        code = [
            (inst_loadi, VM.REG_VAL, None),
        ]
    else:
        code = []

    for var in varl:
        if var not in env.binds:
            env.binds.append(var)
        code += [
            (inst_bindvar, env.get_lexaddr(var)),
        ]

    return code


class Compiler(object):
    def __init__(self):
        self.compiler_dispatch = {
            'if': self.compile_if,
            'let': self.compile_let,
            'let*': self.compile_letstar,
            'set!': self.compile_set,
            'cond': self.compile_cond,
            'apply': self.compile_call,
            'quote': self.compile_quote,
            'begin': self.compile_begin,
            'symbol': self.compile_symbol,
            'define': self.compile_define,
            'lambda': self.compile_lambda,
            'letrec': self.compile_letrec,
            'namedlet': self.compile_namedlet,
            'selfeval': self.compile_selfeval,
        }

    def compile_selfeval(self, exp, env, cont, istail=False):
        code = [
            (inst_loadi, VM.REG_VAL, exp),
        ]
        return bounce(cont, code)
    
    def compile_quote(self, exp, env, cont, istail=False):
        code = [
            (inst_loadi, VM.REG_VAL, cadr(exp)),
        ]
        return bounce(cont, code)
    
    def compile_symbol(self, exp, env, cont, istail=False):
        code = [
            (inst_refvar, env.get_lexaddr(exp)),
        ]
        return bounce(cont, code)
    
    def compile_define(self, exp, env, cont, istail=False):
        def got_val(val_code):
            if var not in env.binds:
                env.binds.append(var)
            code = val_code + [
                (inst_bindvar, env.get_lexaddr(var)),
            ]
            return bounce(cont, code)
    
        var, val = cadr(exp), cddr(exp)
        if lib_issymbol(var):
            return bounce(self.dispatch_exp, car(val), env, got_val)

        lambda_form = lib_append(lib_list(tsym('lambda'), cdr(var)), val)
        var = car(var)
        return bounce(self.compile_lambda, lambda_form, env, got_val)
    
    def compile_set(self, exp, env, cont, istail=False):
        def got_val(val_code):
            code = val_code + [
                (inst_setvar, env.get_lexaddr(var)),
            ]
            return bounce(cont, code)
    
        var, val = cadr(exp), caddr(exp)
        return bounce(self.dispatch_exp, val, env, got_val)
    
    def compile_lambda(self, exp, env, cont, istail=False):
        def got_body(body_code):
            body_code += [
                (inst_ret,),
            ]

            code = [
                (inst_closure, (len(params), len(params)), body_code, isvararg),
            ]
            return bounce(cont, code)
    
        params, body = cadr(exp), cddr(exp)
        isvararg = False

        if lib_issymbol(params):
            # variable arguments, (lambda x ...)
            params = [params]
            isvararg = True
        elif lib_islist(params):
            # normal argument, (lambda (x y) ...)
            params = to_python_list(params)
        else:
            # dotted tail arguments, (lambda (x . y) ...)
            tmplist = []
            while isinstance(cdr(params), Pair):
                tmplist.append(car(params))
                params = cdr(params)
            tmplist.append(car(params))
            tmplist.append(cdr(params))
            params = tmplist
            isvararg = True

        # list() is needed, or `params' will be modified
        # if the lambda body creates new bindings
        newenv = Frame(list(params), env)
        defs = define_dumb(body, newenv)

        return bounce(self.compile_sequence, body, defs, newenv, got_body, istail=True)
    
    def compile_sequence(self, exp, code, env, cont, istail=False):
        """Compile a sequence like ((...) (...) ...). Compile
        the S-expressions in the sequence one by one. If the whole
        sequence is in tail position, so is the last expression
        in the sequence.
        """
        def got_first(code_first):
            nonlocal code
            code += code_first
            return bounce(self.compile_sequence, cdr(exp), code, env, cont, 
                          istail=istail)
    
        def emit_last(code_last):
            nonlocal code
            code += code_last
            return bounce(cont, code)
    
        if lib_isnull(cdr(exp)):
            return bounce(self.dispatch_exp, car(exp), env, emit_last, 
                      istail=istail)

        return bounce(self.dispatch_exp, car(exp), env, got_first)

    def compile_begin(self, exp, env, cont, istail=False):
        defs = define_dumb(cdr(exp), env)
        return bounce(self.compile_sequence, cdr(exp), defs, env, cont, 
                      istail=istail)
    
    def compile_if(self, exp, env, cont, istail=False):
        def got_test(test_code):
            nonlocal code
            code += test_code
            return bounce(self.dispatch_exp, yes_exp, env, got_yes, istail=istail)
    
        def got_yes(yes_code):
            if no_exp is None:
                nonlocal code
                label_after = label()
                code += [
                    (inst_jf, label_after),
                ] + yes_code + [
                    label_after,
                ]
                return bounce(cont, resolve_label(code))
            else:
                nonlocal compiled_yes_code
                compiled_yes_code = yes_code
                return bounce(self.dispatch_exp, no_exp, env, got_no, 
                              istail=istail)
    
        def got_no(no_code):
            nonlocal code
            label_true, label_after = label(), label()
            code += [
                (inst_jt, label_true),
            ] + no_code + [
                (inst_j, label_after),
                label_true,
            ] + compiled_yes_code + [
                label_after,
            ]
            return bounce(cont, resolve_label(code))
    
        compiled_yes_code = None
        test_exp, yes_exp = cadr(exp), caddr(exp)
        if lib_isnull(cdddr(exp)):
            no_exp = None
        else:
            no_exp = cadddr(exp)
        code = []
        return bounce(self.dispatch_exp, test_exp, env, got_test)
    
    def compile_clauses(self, clauses, code, label_after, env, cont, istail=False):
        """Compile clauses of a cond form. Decide if each clause
        is a normal clause or an arrow clause. If the clause is a
        normal one, the last expression in the action part of the
        chosen clause will be in tail position if the whole cond is
        in tail position; if the clause is an arrow clause, the call
        will be a tail call.
        """
        def got_test(test_code):
            nonlocal compiled_test_code
            compiled_test_code = test_code
            if cadar(clauses) is tsym('=>'):
                # current clause is in arrow form (foo => proc)
                proc = caddar(clauses)
                return bounce(self.dispatch_exp, proc, env, got_proc, 
                              istail=istail)

            # normal cond clause ((foo x) (bar))
            seq = cdar(clauses)
            defs = define_dumb(seq, env)

            return bounce(self.compile_sequence, seq, defs, env, got_action, 
                          istail=istail)
    
        def got_proc(proc_code):
            nonlocal code
            if lib_isnull(cdr(clauses)):
                if istail:
                    code += compiled_test_code + [
                        (inst_jf, label_after),
                        (inst_clrargs,),
                        (inst_addarg,),
                    ] + proc_code + [
                        (inst_tailcall,),
                        label_after,
                    ]
                else:
                    code += compiled_test_code + [
                        (inst_jf, label_after),
                        (inst_pushr, VM.REG_ARGS),
                        (inst_clrargs,),
                        (inst_addarg,),
                    ] + proc_code + [
                        (inst_call,),
                        (inst_pop, VM.REG_ARGS),
                        label_after,
                    ]
                return bounce(cont, resolve_label(code))
            else:
                label_next = label()
                code += compiled_test_code + [
                    (inst_jf, label_next),
                    (inst_pushr, VM.REG_ARGS),
                    (inst_clrargs,),
                    (inst_addarg,),
                ] + proc_code + [
                    (inst_call,),
                    (inst_pop, VM.REG_ARGS),
                    (inst_j, label_after),
                    label_next,
                ]
                return bounce(self.compile_clauses, cdr(clauses), code, 
                              label_after, env, cont, istail=istail)
    
        def got_action(action_code):
            nonlocal code
            if test is tsym('else'):
                code += action_code + [
                    label_after,
                ]
                return bounce(cont, resolve_label(code))
            elif lib_isnull(cdr(clauses)):
                code += compiled_test_code + [
                    (inst_jf, label_after),
                ] + action_code + [
                    label_after,
                ]
                return bounce(cont, resolve_label(code))
            else:
                label_next = label()
                code += compiled_test_code + [
                    (inst_jf, label_next),
                ] + action_code + [
                    (inst_j, label_after),
                    label_next,
                ]
                return bounce(self.compile_clauses, cdr(clauses), code, label_after, 
                              env, cont, istail=istail)
    
        compiled_test_code = None
        test = caar(clauses)
        if test is tsym('else'):
            defs = define_dumb(cdar(clauses), env)
            return bounce(self.compile_sequence, cdar(clauses), defs, env, got_action, 
                          istail=istail)
        return bounce(self.dispatch_exp, test, env, got_test)
    
    def compile_cond(self, exp, env, cont, istail=False):
        label_after = label()
        return bounce(self.compile_clauses, cdr(exp), [], label_after, 
                      env, cont, istail=istail)
    
    def compile_let_binds(self, binds, code, varl, env, cont, istail=False):
        """Compile bindings of a normal let form. Each binding will
        be evaluated in a separated environment. The bind values will be
        evaluated and pushed onto the stack, then a new runtime environment
        will be created and those bind values will be popped and bound in
        the new environment.
        """
        def got_bind(bind_code):
            nonlocal code
            nonlocal varl
            varl.append(caar(binds))
            code += bind_code + [
                (inst_pushr, VM.REG_VAL),
            ]
            return bounce(self.compile_let_binds, cdr(binds), code, varl, env, cont)
    
        if binds.isnil:
            return bounce(cont, (code, varl))
        else:
            return bounce(self.dispatch_exp, cadar(binds), env, got_bind)
    
    def compile_let(self, exp, env, cont, istail=False):
        def got_binds(binds_code_varl):
            binds_code, varl = binds_code_varl
            nonlocal code
            code += binds_code + [
                (inst_extenv,),
            ]

            newenv = Frame([], outer=env)
            for var in reversed(varl):
                newenv.binds.append(var)
                code += [
                    (inst_pop, VM.REG_VAL),
                    (inst_bindvar, newenv.get_lexaddr(var)),
                ]

            defs = define_dumb(cddr(exp), newenv)
                
            return bounce(self.compile_sequence, cddr(exp), defs, newenv, got_body, 
                          istail=istail)
    
        def got_body(body_code):
            nonlocal code
            code += body_code + [
                (inst_killenv,),
            ]
            return bounce(cont, code)
    
        code = []
        return bounce(self.compile_let_binds, cadr(exp), [], [], env, got_binds)
    
    def compile_letstar_binds(self, binds, code, env, cont, istail=False):
        """Compile the bindings of a let* form. Each binding will be 
        evaluated in an environment in which all the previously
        evaluated bindings are visible.
        """
        def got_bind(bind_code):
            nonlocal code
            # generate code for getting each value, and bind this variable
            var = caar(binds)
            if var not in env.binds:
                env.binds.append(var)
            code += bind_code + [
                (inst_bindvar, env.get_lexaddr(var)),
            ]
            return bounce(self.compile_letstar_binds, cdr(binds), code, env, cont)
    
        if binds.isnil:
            return bounce(cont, code)
        else:
            return bounce(self.dispatch_exp, cadar(binds), env, got_bind)
    
    def compile_letstar(self, exp, env, cont, istail=False):
        def got_binds(binds_code):
            nonlocal code
            code += [
                 (inst_extenv,),
            ] + binds_code

            defs = define_dumb(cddr(exp), newenv)

            return bounce(self.compile_sequence, cddr(exp), defs, newenv, got_body, 
                          istail=istail)
    
        def got_body(body_code):
            nonlocal code
            code += body_code + [
                (inst_killenv,),
            ]
            return bounce(cont, code)
    
        code = []
        newenv = Frame([], outer=env)
        return bounce(self.compile_letstar_binds, cadr(exp), [], newenv, 
                      got_binds)
    
    def compile_letrec_binds(self, binds, code, env, cont, istail=False):
        """Compile the bindings of a letrec form. Each binding will be
        evaluated in an environment in which all the bindings are visible.
        """
        def got_bind(bind_code):
            nonlocal code
            # generate code for getting each value, and bind this variable
            var = caar(binds)
            code += bind_code + [
                (inst_setvar, env.get_lexaddr(var)),
            ]
            return bounce(self.compile_letrec_binds, cdr(binds), code, env, cont)
    
        if binds.isnil:
            return bounce(cont, code)
        else:
            return bounce(self.dispatch_exp, cadar(binds), env, got_bind)
    
    def compile_letrec(self, exp, env, cont, istail=False):
        def got_binds(binds_code):
            nonlocal code
            code += [
                (inst_extenv,),
                (inst_loadi, VM.REG_VAL, None),
            ]
            for var in names:
                code += [
                    (inst_bindvar, newenv.get_lexaddr(var)),
                ]
            code += binds_code

            defs = define_dumb(cddr(exp), newenv)

            return bounce(self.compile_sequence, cddr(exp), defs, newenv, got_body, 
                          istail=istail)
    
        def got_body(body_code):
            nonlocal code
            code += body_code + [
                (inst_killenv,),
            ]
            return bounce(cont, code)
    
        code = []
        # all binding variables are set to undefined first
        names = let_vars(cadr(exp))
        newenv = Frame(names, outer=env)
        return bounce(self.compile_letrec_binds, cadr(exp), [], newenv, got_binds)
    
    def compile_namedlet(self, exp, env, cont, istail=False):
        """Compile a named let form. At runtime a new frame will
        be created and the closure will be defined in such frame
        and applied to the arguments listed in the bindings.
        """
        def got_define(define_code):
            nonlocal compiled_define_code
            compiled_define_code = define_code
            apply_form = cons(proc_name, from_python_list(vall))
            return bounce(self.compile_call, apply_form, newenv, got_apply, istail=istail)
    
        def got_apply(apply_code):
            code = [
                (inst_extenv,),
            ] + compiled_define_code + \
                apply_code + [
                (inst_killenv,),
            ]
            return bounce(cont, code)
    
        proc_name = cadr(exp)
        varl = let_vars(caddr(exp))
        vall = let_vals(caddr(exp))
    
        lambda_form = lib_append(
                        lib_list(
                            tsym('lambda'), from_python_list(varl)), 
                        cdddr(exp))
        define_form = lib_list(tsym('define'), proc_name, lambda_form)
    
        newenv = Frame([proc_name], outer=env)
        compiled_define_code = None

        return bounce(self.compile_define, define_form, newenv, got_define)
    
    def compile_call_args(self, args, code, env, cont, istail=False):
        """Compile arguments of a call. Arguments will be evaluted
        from left to right.
        """
        def got_arg(arg_code):
            nonlocal code
            code += arg_code + [
                (inst_addarg,),
            ]
            return bounce(self.compile_call_args, cdr(args), code, env, cont)
    
        if args.isnil:
            return bounce(cont, code)
        return bounce(self.dispatch_exp, car(args), env, got_arg)
    
    def compile_call(self, exp, env, cont, istail=False):
        def got_args(args_code):
            nonlocal compiled_args_code
            compiled_args_code = args_code
            return bounce(self.dispatch_exp, car(exp), env, got_proc)
    
        def got_proc(proc_code):
            if istail:
                code = compiled_args_code + proc_code + [
                    (inst_tailcall,)
                ]
            else:
                code = compiled_args_code + proc_code + [
                    (inst_call,),
                    (inst_pop, VM.REG_ARGS),
                ]
            return bounce(cont, code)
    
        if istail:
            code = [
                (inst_clrargs,),
            ]
        else:
            code = [
                (inst_pushr, VM.REG_ARGS),
                (inst_clrargs,),
            ]
        compiled_args_code = None
        return bounce(self.compile_call_args, cdr(exp), code, env, got_args)
    
    def dispatch_exp(self, exp, env, cont, istail=False):
        return bounce(self.compiler_dispatch[get_sexp_type(exp)], 
                      exp, env, cont, istail=istail)
            
    def compile(self, exp, env):
        """Compile S-expression `exp' with 
        compile-time environment `env'.
        """
        return pogo_stick(bounce(self.dispatch_exp, exp, env, lambda d:d))
        
