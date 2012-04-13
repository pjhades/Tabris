# -*- coding: utf-8 -*-

"""
Arithmetic library. These functions all take as argument a
python list containing the operands.
"""

from errors import *

def _check_argc(min_argc):
    def inner(f):
        def func(*args):
            if len(args) < min_argc:
                raise SchemeError('', 'wrong argument number')
            try:
                return f(*args)
            except TypeError:
                raise SchemeError('wrong argument type')
        return func
    return inner


@_check_argc(0)
def prim_add(*args):
    return sum(args)


@_check_argc(1)
def prim_sub(*args):
    if len(args) == 1:
        return -args[0]
    result = args[0]
    for arg in args[1:]:
        result -= arg
    return result


@_check_argc(0)
def prim_mul(*args):
    result = 1
    for arg in args:
        result *= arg
    return result


@_check_argc(1)
def prim_div(*args):
    if len(args) == 1:
        return 1 / args[0]
    result = args[0]
    for arg in args[1:]:
        result /= arg
    return result


@_check_argc(2)
def prim_eq(*args):
    for arg in args[1:]:
        if arg != args[0]:
            return False
    return True


@_check_argc(2)
def prim_lt(*args):
    pre = args[0]
    for arg in args[1:]:
        if pre >= arg:
            return False
        pre = arg
    return True


@_check_argc(2)
def prim_le(*args):
    pre = args[0]
    for arg in args[1:]:
        if pre > arg:
            return False
        pre = arg
    return True


@_check_argc(2)
def prim_gt(*args):
    pre = args[0]
    for arg in args[1:]:
        if pre <= arg:
            return False
        pre = arg
    return True


@_check_argc(2)
def prim_ge(*args):
    pre = args[0]
    for arg in args[1:]:
        if pre < arg:
            return False
        pre = arg
    return True
