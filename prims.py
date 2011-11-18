# -*- coding: utf-8 -*-


from stypes import *
from errors import *

def check_argc(min_argc, max_argc=float('inf')):
    def inner(f):
        def func(args):
            if not min_argc <= len(args) <= max_argc:
                raise SchemeEvalError('', 'wrong argument number')
            return f(args)
        return func
    return inner

@check_argc(1)
def prim_add(args):
    result = Rational(0, 1)
    for arg in args:
        result += arg

    return result

@check_argc(1)
def prim_sub(args):
    if len(args) == 1:
        return -args[0]
        
    result = Rational(0, 1)
    result += args[0]
    for arg in args[1:]:
        result -= arg

    return result

@check_argc(1)
def prim_mul(args):
    result = Rational(1, 1)
    for arg in args:
        result *= arg

    return result

@check_argc(1)
def prim_div(args):
    if len(args) == 1:
        return Rational(1, 1) / args[0]
        
    result = Rational(1, 1)
    result *= args[0]
    for arg in args[1:]:
        result /= arg

    return result

@check_argc(2)
def prim_eq(args):
    for arg in args[1:]:
        if Boolean.true(arg == args[0]):
            continue
        return Boolean(False)
    return Boolean(True)

@check_argc(2)
def prim_lt(args):
    now = args[0]
    for arg in args[1:]:
        if Boolean.true(now >= arg):
            return Boolean(False)
    return Boolean(True)

@check_argc(2)
def prim_le(args):
    now = args[0]
    for arg in args[1:]:
        if Boolean.true(now > arg):
            return Boolean(False)
    return Boolean(True)

@check_argc(2)
def prim_gt(args):
    now = args[0]
    for arg in args[1:]:
        if Boolean.true(now <= arg):
            return Boolean(False)
    return Boolean(True)

@check_argc(2)
def prim_ge(args):
    now = args[0]
    for arg in args[1:]:
        if Boolean.true(now < arg):
            return Boolean(False)
    return Boolean(True)

@check_argc(2)
def prim_cons(args):
    # TODO
    pass

def prim_car(args):
    # TODO
    pass

def prim_cdr(args):
    # TODO
    pass

# handlers for primitives
prim_handlers = {'+': prim_add, \
                 '-': prim_sub, \
                 '*': prim_mul, \
                 '/': prim_div, \
                 '=': prim_eq, \
                 '<': prim_lt, \
                 '>': prim_gt, \
                 '<=': prim_le, \
                 '>=': prim_ge, \
                 'car': prim_car, \
                 'cdr': prim_cdr, \
                 'cons': prim_cons}
