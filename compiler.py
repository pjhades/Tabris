# -*- coding: utf-8 -*-

from vm import REG_VAL, inst_loadi, inst_refvar, inst_bindvar, inst_setvar
from pair import car, cdr, cadr, cddr, caddr, to_python_list, func_islist
from scmtypes import func_issymbol, Closure
from environment import Frame
from syntax import *
from trampoline import *


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


# TODO: (define (foo x) ..)
def compile_define(exp, env, cont):
    def got_val(val_code):
        code = val_code + [
            (inst_bindvar, var),
        ]
        return bounce(cont, code)
    var, val = cadr(exp), caddr(exp)
    return bounce(dispatch_exp, val, env, got_val)


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


def dispatch_exp(exp, env, cont):
    """Compile S-expression `exp' with compile-time
    environment `env'."""
    #print(exp, type(exp))
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
    else:
        raise SchemeError('unknown expression ' + str(exp))

        
def tcompile(exp, env):
    return pogo_stick(bounce(dispatch_exp, exp, env, lambda d:d))
    
