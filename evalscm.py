# -*- coding: utf-8 -*-

import env
import utils
import syntax as syn

from arith import *
from pairs import *
from stypes import *
from errors import *
from prims import prim_handlers

def eval_define(expr, en):
    syn.check_define(expr)
    en.add_var(syn.define_var(expr), eval(syn.define_value(expr), en))
    return syn.define_var(expr)

def chain(expr):
    if not isinstance(expr, list):
        if syn.is_identifier(expr):
            return Symbol(expr)
        else:
            return eval_atom(expr, None)

    if expr == []:
        return Pair('', '', '()')

    car = chain(expr[0])
    if len(expr) == 3:
        cdr = chain(expr[2]) if expr[1] == '.' else chain(expr[1:])
    else:
        cdr = chain(expr[1:])

    return Pair(car, cdr, utils.get_clean_code(expr))

def eval_quote(expr, en):
    syn.check_quote(expr)
    syn.check_dotted_pair(expr[1])

    if not isinstance(expr[1], list):
        if syn.is_identifier(expr[1]):
            return Symbol(expr[1])
        else:
            eval_atom(expr[1], en)
    else:
        return chain(expr[1])

def eval_set(expr, en):
    syn.check_set(expr)
    env.set_variable(syn.set_var(expr), eval(syn.set_value(expr), en), en)

#TODO: optimize tail call
def eval_if(expr, en):
    syn.check_if(expr)
    if Boolean.true(eval(syn.if_pred(expr), en)):
        return eval(syn.if_yes(expr), en)
    elif syn.if_has_no(expr):
        return eval(syn.if_no(expr), en)

def eval_lambda(expr, en):
    syn.check_lambda(expr)
    return Procedure(syn.lambda_params(expr), syn.lambda_body(expr), en)

#TODO: optimize tail call
def eval_begin(expr, en):
    subexprs = syn.begin_exprs(expr)

    if subexprs == []:
        return

    for e in subexprs[:-1]:
        eval(e, en)

    return eval(subexprs[-1], en)

#TODO: optimize tail call
def eval_cond(expr, en):
    syn.check_cond(expr)

    # all clauses except else
    for clause in syn.cond_clauses(expr):
        test = eval(clause[0], en)

        if Boolean.true(test):
            if clause[1] == '=>':
                return apply(eval(clause[2], en), [test])
            for sub_expr in clause[1:-1]:
                eval(sub_expr, en)
            return eval(clause[-1], en)
        
    # else clause
    if syn.cond_has_else(expr):
        for sub_expr in syn.cond_else(expr)[1:-1]:
            eval(sub_expr, en)
        return eval(syn.cond_else(expr)[-1], en)

#TODO: optimize tail call
def eval_let(expr, en):
    syn.check_let(expr)

    var = [x[0] for x in syn.let_bindings(expr)]
    body = syn.let_body(expr)
    param = [x[1] for x in syn.let_bindings(expr)]

    return eval([syn.make_lambda(var, body)] + param, en)

#TODO: optimize tail call
def eval_letstar(expr, en):
    syn.check_let(expr)
    return eval(syn.letstar_to_lambda(expr), en)

#TODO: optimize tail call
def eval_letrec(expr, en):
    syn.check_let(expr)
    return eval(syn.letrec_to_lambda(expr), en)

def eval_and(expr, en):
    for e in syn.and_or_exprs(expr):
        if not Boolean.true(eval(e, en)):
            return Boolean(False)
    return Boolean(True)

def eval_or(expr, en):
    for e in syn.and_or_exprs(expr):
        if Boolean.true(eval(e, en)):
            return Boolean(True)
    return Boolean(False)

#TODO: optimize tail call
def eval_apply(expr, en):
    """
        Scheme apply
    """
    syn.check_apply(expr)
    #TODO: this apply is the Scheme apply, not apply of interpreter.
    # therefore the apply_args(expr) will be interpreted to a list
    # which is represented by Pair objects
    # We need to change this list to python list
    # Implement car and cdr first !
    return apply(eval(syn.apply_proc(expr), en), eval(syn.apply_args(expr), en))

#TODO: optimize tail call
def eval_call(expr, en):
    """
        Procedure call
    """
    proc = eval(syn.call_proc(expr), en)
    args = [eval(arg, en) for arg in syn.call_args(expr)]
    return apply(proc, args)

def eval_atom(expr, en):
    if syn.is_string(expr):
        return String(expr)

    elif syn.is_integer(expr):
        return Rational(int(expr), 1)

    elif syn.is_decimal(expr):
        return Real(float(expr))

    elif syn.is_fraction(expr):
        x, y = expr.split('/')
        return Rational(int(x), int(y))

    elif syn.is_complex(expr):
        part = syn.RE_COMPLEX.search(expr).groups()

        real, imag = (part[2], part[4]) if part[2] and part[4] else ('0', part[6])
        imag = ('-1' if imag == '-' else '+1') if imag in '+-' else imag
        real, imag = eval(real, en), eval(imag, en)

        if Boolean.true(imag == Rational(0, 1)):
            return real

        return Complex(real, imag)

    elif expr in syn.RESERVED:
        raise SchemeBadSyntaxError(expr, 'bad use of reserved word')

    elif syn.is_identifier(expr):
        return en.get_var(expr) 

    elif syn.is_sharp(expr):
        return Boolean(True) if expr == '#t' else Boolean(False)

    else:
        raise SchemeEvalError(expr, 'unknown expression type')


expr_handlers = {'define': eval_define, \
                 'quote': eval_quote, \
                 'set!': eval_set, \
                 'if': eval_if, \
                 'lambda': eval_lambda, \
                 'begin': eval_begin, \
                 'cond': eval_cond, \
                 'let': eval_let, \
                 'let*': eval_letstar, \
                 'letrec': eval_letrec, \
                 'and': eval_and, \
                 'or': eval_or, \
                 'apply': eval_apply}

def eval(expr, en):
    if not isinstance(expr, list):
        return eval_atom(expr, en)
    else:
        tag = expr[0]
        if isinstance(tag, list):
            return eval_call(expr, en)
        return expr_handlers[tag](expr, en) if tag in expr_handlers else eval_call(expr, en)

#TODO: optimize tail call
def apply(proc, args):
    if proc.is_prim:
        return prim_handlers[proc.body](args)
    else:
        en = env.extend_env([proc.params] if proc.is_var_args else proc.params, args, proc.env)
        for expr in proc.body[:-1]:
            eval(expr, en)
        return eval(proc.body[-1], en)
