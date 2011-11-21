# -*- coding: utf-8 -*-

import env
import syntax as syn

from stypes import *
from errors import *
from prims import prim_handlers

def eval_define(expr, en):
    syn.check_define(expr)
    env.add_binding(syn.define_var(expr), eval(syn.define_value(expr), en), en)
    return syn.define_var(expr)

def eval_quote(expr, en):
    syn.check_quote(expr)
    if not isinstance(expr[1], list):
        return Symbol(expr)
    else:
        return List(expr)

def eval_set(expr, en):
    syn.check_set(expr)
    env.set_variable(syn.set_var(expr), eval(syn.set_value(expr), en), en)
    return None

def eval_if(expr, en):
    syn.check_if(expr)
    if Boolean.true(eval(syn.if_pred(expr), en)):
        return eval(syn.if_yes(expr), en)
    elif syn.if_has_no(expr):
        return eval(syn.if_no(expr), en)
    else:
        return None

def eval_lambda(expr, en):
    syn.check_lambda(expr)
    return Procedure(syn.lambda_params(expr), syn.lambda_body(expr), en)

def eval_begin(expr, en):
    syn.check_begin(expr)
    ret = [eval(subexpr, en) for subexpr in syn.begin_exprs(expr)]
    return None if ret == [] else ret[-1]

def eval_cond(expr, en):
    syn.check_cond(expr)
    # all clauses except else
    for clause in syn.cond_clauses(expr):
        test = eval(clause[0], en)
        if Boolean.true(test):
            # <test> => <proc> form
            # TODO: modify this after finishing apply()
            #if clause[1] == '=>':
            #    apply(eval(clause[2], en), [test])
            # normal form
            for sub_expr in clause[1:-1]:
                eval(sub_expr, en)
            return eval(clause[-1], en)
    # else clause
    if syn.cond_has_else(expr):
        for sub_expr in syn.cond_else(expr)[1:-1]:
            eval(sub_expr, en)
        return eval(syn.cond_else(expr)[-1], en)
    return None

def eval_let(expr, en):
    syn.check_let(expr)
    return eval([syn.make_lambda([x[0] for x in syn.let_bindings(expr)], \
                                    syn.let_body(expr))] + \
                    [x[1] for x in syn.let_bindings(expr)], en)

def eval_letstar(expr, en):
    syn.check_let(expr)
    return eval(syn.letstar_to_lambda(expr), en)

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

def eval_apply(expr, en):
    syn.check_apply(expr)
    return apply(eval(syn.apply_proc(expr), en), \
                 eval(syn.apply_args(expr), en))

def eval_call(expr, en):
    proc = eval(syn.call_proc(expr), en)
    args = [eval(arg, en) for arg in syn.call_args(expr)]
    return apply(proc, args)

# handlers for each expression type
expr_handlers = {'define': eval_define, \
                 'quote': eval_quote, \
                 'quote\'': eval_quote, \
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
            # extract each part from the pattern
            part = syn.RE_COMPLEX.search(expr).groups()

            if part[2] and part[4]:
                real, imag = part[2], part[4]
            else:
                real, imag = '0', part[6]

            if imag == '-':
                imag = '-1'
            elif imag == '+':
                imag = '+1'

            real, imag = eval(real, en), eval(imag, en)

            if Boolean.true(imag == Rational(0, 1)):
                return real

            return Complex(real, imag)

        elif expr in syn.RESERVED:
            raise BadSyntaxError(expr, 'bad use of reserved word')

        elif syn.is_identifier(expr):
            return env.lookup_variable(expr, en) 

        elif syn.is_sharp(expr):
            return Boolean(True) if expr == '#t' else Boolean(False)

        else:
            raise SchemeEvalError(expr, 'unknown expression type')
    else:
        tag = syn.get_expr_type(expr)
        return expr_handlers[tag](expr, en) if tag in expr_handlers else \
               eval_call(expr, en)

def apply(proc, args):
    if proc.is_prim:
        return prim_handlers[proc.body](args)
    else:
        en = env.extend_env([proc.params] if proc.is_var_args else proc.params, args, proc.en)
        for expr in proc.body[:-1]:
            eval(expr, en)
        result = eval(proc.body[-1], en)
        env.remove_env(en)

        return result
