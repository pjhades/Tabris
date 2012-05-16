# -*- coding: utf-8 -*-

from errors import *

def check_arg_number(min_argc):
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

@check_arg_number(0)
def prim_add(*args):
    return sum(args)

@check_arg_number(1)
def prim_sub(*args):
    if len(args) == 1:
        return -args[0]
    result = args[0]
    for arg in args[1:]:
        result -= arg
    return result

@check_arg_number(0)
def prim_mul(*args):
    result = 1
    for arg in args:
        result *= arg
    return result

@check_arg_number(1)
def prim_div(*args):
    if len(args) == 1:
        return 1 / args[0]
    result = args[0]
    for arg in args[1:]:
        result /= arg
    return result

@check_arg_number(2)
def prim_eq(*args):
    for arg in args[1:]:
        if arg != args[0]:
            return False
    return True

@check_arg_number(2)
def prim_lt(*args):
    pre = args[0]
    for arg in args[1:]:
        if pre >= arg:
            return False
        pre = arg
    return True

@check_arg_number(2)
def prim_le(*args):
    pre = args[0]
    for arg in args[1:]:
        if pre > arg:
            return False
        pre = arg
    return True

@check_arg_number(2)
def prim_gt(*args):
    pre = args[0]
    for arg in args[1:]:
        if pre <= arg:
            return False
        pre = arg
    return True

@check_arg_number(2)
def prim_ge(*args):
    pre = args[0]
    for arg in args[1:]:
        if pre < arg:
            return False
        pre = arg
    return True

@check_arg_number(0)
def prim_and(*args):
    if len(args) == 0:
        return True
    for arg in args:
        if arg is False:
            return False
    return args[-1]

@check_arg_number(0)
def prim_or(*args):
    if len(args) == 0:
        return False
    for arg in args:
        if arg is not False:
            return arg
    return False

@check_arg_number(0)
def prim_not(*args):
    val = args[0]
    if val is False:
        return True
    return False

