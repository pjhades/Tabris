# -*- coding: utf-8 -*-

from vm import REG_VAL, inst_loadi, inst_refvar, inst_bindvar, inst_setvar, \
        inst_jf, inst_jt, inst_j
from pair import cons, car, cdr, cadr, cddr, caddr, cadddr, cdddr, \
        to_python_list, func_islist
from scmtypes import func_issymbol, Closure, Symbol
from environment import Frame
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
    if func_issymbol(var):
        return bounce(dispatch_exp, car(val), env, got_val)
    else:
        lambda_form = func_append(
                func_list(Symbol('lambda'), cdr(var)), val)
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
        newenv = Frame(params, [0]*len(params), env)
        closure = Closure(params, body_code, newenv)
        code = [
            (inst_loadi, REG_VAL, closure),
        ]
        return bounce(cont, code)

    params, body = cadr(exp), cddr(exp)
    varargs = False
    if func_issymbol(params):
        params = [params]
        varargs = True
    elif func_islist(params):
        params = to_python_list(params)
    else:
        tmplist = []
        while isinstance(cdr(params), Pair):
            tmplist.append(car(params))
            params = cdr(params)
        tmplist.append(car(params))
        tmplist.append(cdr(params))
        params = tmplist
        varargs = True
    return bounce(compile_sequence, body, [], env, got_body)


def compile_sequence(exp, code, env, cont):
    def got_first(code_first):
        nonlocal code
        code += code_first
        return bounce(compile_sequence, cdr(exp), code, env, cont)
    def emit_last(code_last):
        nonlocal code
        code += code_last
        return bounce(cont, code)

    if func_isnull(cdr(exp)):
        return bounce(dispatch_exp, car(exp), env, emit_last)
    else:
        return bounce(dispatch_exp, car(exp), env, got_first)


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
                return bounce(cont, code)
            if no is None:
                nonlocal code
                label_after = label()
                code += [
                    (inst_jf, label_after),
                ] + yes_code + [
                    label_after,
                ]
                return bounce(cont, code)
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


def compile_cond(exp, env, cont):
    #TODO:
    pass


def dispatch_exp(exp, env, cont):
    """Compile S-expression `exp' with compile-time
    environment `env'."""
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
        return bounce(compile_sequence, cdr(exp), [], env, cont)
    elif isif(exp):
        return bounce(compile_if, exp, env, cont)
    else:
        raise SchemeError('unknown expression ' + str(exp))

        
def tcompile(exp, env):
    return pogo_stick(bounce(dispatch_exp, exp, env, lambda d:d))
    
