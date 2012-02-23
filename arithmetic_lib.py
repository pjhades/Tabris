# -*- coding: utf-8 -*-

"""
Arithmetic library. These functions all take as argument a
python list containing the operands.
"""

from basic_type import Boolean, is_true
from number_type import Rational
from errors import *

def _check_argc(min_argc, max_argc=float('inf')):
    def inner(f):
        def func(*args):
            if not min_argc <= len(args) <= max_argc:
                raise SchemeError('', 'wrong argument number')
            return f(*args)
        return func
    return inner

@_check_argc(0)
def prim_add(*args):
    result = Rational(0, 1)
    for arg in args:
        result += arg

    return result

@_check_argc(1)
def prim_sub(*args):
    if len(args) == 1:
        return -args[0]
        
    result = Rational(0, 1)
    result += args[0]
    for arg in args[1:]:
        result -= arg

    return result

@_check_argc(0)
def prim_mul(*args):
    result = Rational(1, 1)
    for arg in args:
        result *= arg

    return result

@_check_argc(1)
def prim_div(*args):
    if len(args) == 1:
        return Rational(1, 1) / args[0]
        
    result = Rational(1, 1)
    result *= args[0]
    for arg in args[1:]:
        result /= arg

    return result

@_check_argc(2)
def prim_eq(*args):
    for arg in args[1:]:
        if is_true(arg == args[0]):
            continue
        return Boolean(False)
    return Boolean(True)

@_check_argc(2)
def prim_lt(*args):
    now = args[0]
    for arg in args[1:]:
        if is_true(now >= arg):
            return Boolean(False)
    return Boolean(True)

@_check_argc(2)
def prim_le(*args):
    now = args[0]
    for arg in args[1:]:
        if is_true(now > arg):
            return Boolean(False)
    return Boolean(True)

@_check_argc(2)
def prim_gt(*args):
    now = args[0]
    for arg in args[1:]:
        if is_true(now <= arg):
            return Boolean(False)
    return Boolean(True)

@_check_argc(2)
def prim_ge(*args):
    now = args[0]
    for arg in args[1:]:
        if is_true(now < arg):
            return Boolean(False)
    return Boolean(True)

