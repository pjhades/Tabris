# -*- coding: utf-8 -*-

from scmtypes import Symbol
from environment import Frame
from pair import to_python_list
from scmlib import *
from insts import *
from syntax import *
from trampoline import *


def _label_gen():
    counter = 0
    def f():
        nonlocal counter
        counter += 1
        return 'label%d' % (counter - 1)
    return f


label = _label_gen()


def resolve_label(code):
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


def compile_selfeval(exp, env, cont):
    code = [
        (inst_loadi, REG_VAL, exp),
    ]
    return bounce(cont, code)


def compile_quote(exp, env, cont):
    code = [
        (inst_loadi, REG_VAL, cadr(exp)),
    ]
    return bounce(cont, code)


def compile_symbol(exp, env, cont):
    code = [
        (inst_refvar, exp),
    ]
    return bounce(cont, code)


def compile_define(exp, env, cont):
    def got_val(val_code):
        code = val_code + [
            (inst_bindvar, var),
        ]
        return bounce(cont, code)
    var, val = cadr(exp), cddr(exp)
    if lib_issymbol(var):
        return bounce(dispatch_exp, car(val), env, got_val)
    else:
        lambda_form = lib_append(
                lib_list(Symbol('lambda'), cdr(var)), val)
        var = car(var)
        return bounce(compile_lambda, lambda_form, env, got_val)


def compile_set(exp, env, cont):
    def got_val(val_code):
        code = val_code + [
            (inst_setvar, var),
        ]
        return bounce(cont, code)

    var, val = cadr(exp), caddr(exp)
    return bounce(dispatch_exp, val, env, got_val)


def compile_lambda(exp, env, cont):
    def got_body(body_code):
        body_code += [
            (inst_ret,),
        ]
        code = [
            (inst_closure, params, body_code, isvararg),
        ]
        return bounce(cont, code)

    params, body = cadr(exp), cddr(exp)
    isvararg = False
    if lib_issymbol(params):
        params = [params]
        isvararg = True
    elif lib_islist(params):
        params = to_python_list(params)
    else:
        tmplist = []
        while isinstance(cdr(params), Pair):
            tmplist.append(car(params))
            params = cdr(params)
        tmplist.append(car(params))
        tmplist.append(cdr(params))
        params = tmplist
        isvararg = True
    newenv = Frame(params, [None]*len(params), env)
    return bounce(compile_sequence, body, [], newenv, got_body)


def compile_sequence(exp, code, env, cont):
    def got_first(code_first):
        nonlocal code
        code += code_first
        return bounce(compile_sequence, cdr(exp), code, env, cont)
    def emit_last(code_last):
        nonlocal code
        code += code_last
        return bounce(cont, code)

    if lib_isnull(cdr(exp)):
        return bounce(dispatch_exp, car(exp), env, emit_last)
    else:
        return bounce(dispatch_exp, car(exp), env, got_first)


def compile_begin(exp, env, cont):
    return bounce(compile_sequence, cdr(exp), [], env, cont)


def compile_if(exp, env, cont):
    def got_test(test_code):
        def got_yes(yes_code):
            def got_no(no_code):
                nonlocal code
                label_true, label_after = label(), label()
                code += [
                    (inst_jt, label_true),
                ] + no_code + [
                    (inst_j, label_after),
                    label_true,
                ] + yes_code + [
                    label_after,
                ]
                return bounce(cont, resolve_label(code))
            if no is None:
                nonlocal code
                label_after = label()
                code += [
                    (inst_jf, label_after),
                ] + yes_code + [
                    label_after,
                ]
                return bounce(cont, resolve_label(code))
            else:
                return bounce(dispatch_exp, no, env, got_no)

        nonlocal code
        code += test_code
        return bounce(dispatch_exp, yes, env, got_yes)

    test, yes = cadr(exp), caddr(exp)
    if cdddr(exp) == NIL:
        no = None
    else:
        no = cadddr(exp)
    code = []
    return bounce(dispatch_exp, test, env, got_test)


# TODO: (cond (<test> => <func>) ... )
# if <test> evaluates to true, call <func> on the return
# value of <test>
def compile_clauses(clauses, code, label_after, env, cont):
    def got_test(test_code):
        def got_action(action_code):
            nonlocal code
            if test == Symbol('else'):
                code += action_code + [
                    label_after,
                ]
                return bounce(cont, resolve_label(code))
            elif cdr(clauses) == NIL:
                code += test_code + [
                    (inst_jf, label_after),
                ] + action_code + [
                    label_after,
                ]
                return bounce(cont, resolve_label(code))
            else:
                label_next = label()
                code += test_code + [
                    (inst_jf, label_next),
                ] + action_code + [
                    (inst_j, label_after),
                    label_next,
                ]
                return bounce(compile_clauses, cdr(clauses), code, 
                              label_after, env, cont)

        seq = cdar(clauses)
        return bounce(compile_sequence, seq, [], env, got_action)

    test = caar(clauses)
    return bounce(dispatch_exp, test, env, got_test)


def compile_cond(exp, env, cont):
    label_after = label()
    return bounce(compile_clauses, cdr(exp), [], label_after, env, cont)


def compile_let_binds(binds, code, varl, env, cont):
    """Each binding of `let' is evaluated in a separated environment."""
    def got_bind(bind_code):
        nonlocal code
        nonlocal varl
        # record each variable
        varl.append(caar(binds))
        # generate code for getting each value, and
        # push them onto the stack
        code += bind_code + [
            (inst_pushr, REG_VAL),
        ]
        return bounce(compile_let_binds, cdr(binds), code, varl, env, cont)

    if binds == []:
        return bounce(cont, (code, varl))
    else:
        return bounce(dispatch_exp, cadar(binds), env, got_bind)


def compile_let(exp, env, cont):
    def got_binds(binds_code_varl):
        def got_body(body_code):
            nonlocal code
            code += body_code + [
                (inst_killenv,),
            ]
            return bounce(cont, code)

        binds_code, varl = binds_code_varl
        code = binds_code + [
            (inst_extenv,),
        ]
        for var in reversed(varl):
            code += [
                (inst_pop, REG_VAL),
                (inst_bindvar, var),
            ]
        newenv = Frame(varl, [None]*len(varl), env)
        return bounce(compile_sequence, cddr(exp), [], newenv, got_body)

    return bounce(compile_let_binds, cadr(exp), [], [], env, got_binds)


def compile_letstar_binds(binds, code, env, cont):
    """Each binding of `let*' is evaluated in an environment in which
    all the previous bindings are visible."""
    def got_bind(bind_code):
        nonlocal code
        # generate code for getting each value, and 
        # bind this variable
        code += bind_code + [
            (inst_bindvar, caar(binds)),
        ]
        # setup the variable in the compile-time frame 
        env.bindvar(caar(binds), None)
        return bounce(compile_letstar_binds, cdr(binds), code, env, cont)

    if binds == []:
        return bounce(cont, code)
    else:
        return bounce(dispatch_exp, cadar(binds), env, got_bind)


def compile_letstar(exp, env, cont):
    def got_binds(binds_code):
        def got_body(body_code):
            nonlocal code
            code += body_code + [
                (inst_killenv,),
            ]
            return bounce(cont, code)

        code = [
             (inst_extenv,),
        ] + binds_code

        return bounce(compile_sequence, cddr(exp), [], newenv, got_body)

    # create a new compile-time frame
    newenv = Frame(outer=env)
    return bounce(compile_letstar_binds, cadr(exp), [], newenv, got_binds)


def compile_letrec_binds(binds, code, env, cont):
    """Each binding of `letrec' is evaluated in an environment in which
    all the bindings are visible."""
    def got_bind(bind_code):
        nonlocal code
        # generate code for getting each value, and 
        # bind this variable
        code += bind_code + [
            (inst_setvar, caar(binds)),
        ]
        return bounce(compile_letrec_binds, cdr(binds), code, env, cont)

    if binds == []:
        return bounce(cont, code)
    else:
        return bounce(dispatch_exp, cadar(binds), env, got_bind)


def compile_letrec(exp, env, cont):
    def got_binds(binds_code):
        def got_body(body_code):
            nonlocal code
            code += body_code + [
                (inst_killenv,),
            ]
            return bounce(cont, code)

        code = [
            (inst_extenv,),
            (inst_loadi, REG_VAL, None),
        ]
        for var in varl:
            code += [
                (inst_bindvar, var),
            ]
        code += binds_code
        return bounce(compile_sequence, cddr(exp), [], newenv, got_body)

    # all binding variables are set to undefined first
    varl = letrec_vars(cadr(exp))
    # create a new compile-time frame
    newenv = Frame(varl, [None]*len(varl), outer=env)
    return bounce(compile_letrec_binds, cadr(exp), [], newenv, got_binds)


def compile_apply_args(args, code, env, cont):
    def got_arg(arg_code):
        nonlocal code
        code += arg_code + [
            (inst_addarg,),
        ]
        return bounce(compile_apply_args, cdr(args), code, env, cont)

    if args == []:
        return bounce(cont, code)
    else:
        return bounce(dispatch_exp, car(args), env, got_arg)


def compile_apply(exp, env, cont):
    def got_args(args_code):
        def got_proc(proc_code):
            code = args_code + proc_code + [
                (inst_call,),
                (inst_pop, REG_ARGS),
            ]
            return bounce(cont, code)

        return bounce(dispatch_exp, car(exp), env, got_proc)

    code = [
        (inst_pushr, REG_ARGS),
        (inst_clrargs,),
    ]
    return bounce(compile_apply_args, cdr(exp), code, env, got_args)


def dispatch_exp(exp, env, cont):
    """Compile S-expression `exp' with compile-time environment `env'."""
    if issymbol(exp):
        return bounce(compile_symbol, exp, env, cont) 
    elif isquote(exp):
        return bounce(compile_quote, exp, env, cont)
    elif isselfeval(exp):
        return bounce(compile_selfeval, exp, env, cont)
    elif isdefine(exp):
        return bounce(compile_define, exp, env, cont)
    elif isset(exp):
        return bounce(compile_set, exp, env, cont)
    elif islambda(exp):
        return bounce(compile_lambda, exp, env, cont)
    elif isbegin(exp):
        return bounce(compile_begin, exp, env, cont)
    elif isif(exp):
        return bounce(compile_if, exp, env, cont)
    elif iscond(exp):
        return bounce(compile_cond, exp, env, cont)
    elif islet(exp):
        return bounce(compile_let, exp, env, cont)
    elif isletstar(exp):
        return bounce(compile_letstar, exp, env, cont)
    elif isletrec(exp):
        return bounce(compile_letrec, exp, env, cont)
    elif isapply(exp):
        return bounce(compile_apply, exp, env, cont)
    else:
        raise SchemeError('unknown expression ' + str(exp))

        
def tcompile(exp, env):
    return pogo_stick(bounce(dispatch_exp, exp, env, lambda d:d))
    