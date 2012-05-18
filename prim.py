# -*- coding: utf-8 -*-

import math
from scmlib import lib_isnumber
from errors import *

def force_number_type(f):
    def inner(*args):
        for arg in args:
            if arg is True or arg is False or not lib_isnumber(arg):
                raise SchemeError('expect numbers as arguments')
        return f(*args)
    return inner

def force_arg_number(min_argc):
    def inner(f):
        def func(*args):
            if len(args) < min_argc:
                raise SchemeError('wrong argument number')
            return f(*args)
        return func
    return inner

@force_number_type
def prim_add(*args):
    if len(args) == 0:
        return 0
    return sum(args)

@force_arg_number(1)
@force_number_type
def prim_sub(*args):
    if len(args) == 1:
        return -args[0]
    result = args[0]
    for arg in args[1:]:
        result -= arg
    return result

@force_number_type
def prim_mul(*args):
    result = 1
    for arg in args:
        result *= arg
    return result

@force_arg_number(1)
@force_number_type
def prim_div(*args):
    if len(args) == 1:
        return 1 / args[0]
    result = args[0]
    for arg in args[1:]:
        result /= arg
    return result

@force_number_type
def prim_mod(a, b):
    return a % b

@force_arg_number(2)
@force_number_type
def prim_eq(*args):
    for arg in args[1:]:
        if arg != args[0]:
            return False
    return True

@force_arg_number(2)
@force_number_type
def prim_lt(*args):
    pre = args[0]
    for arg in args[1:]:
        if pre >= arg:
            return False
        pre = arg
    return True

@force_arg_number(2)
@force_number_type
def prim_le(*args):
    pre = args[0]
    for arg in args[1:]:
        if pre > arg:
            return False
        pre = arg
    return True

@force_arg_number(2)
@force_number_type
def prim_gt(*args):
    pre = args[0]
    for arg in args[1:]:
        if pre <= arg:
            return False
        pre = arg
    return True

@force_arg_number(2)
@force_number_type
def prim_ge(*args):
    pre = args[0]
    for arg in args[1:]:
        if pre < arg:
            return False
        pre = arg
    return True

def prim_and(*args):
    if len(args) == 0:
        return True
    for arg in args:
        if arg is False:
            return False
    return args[-1]

def prim_or(*args):
    if len(args) == 0:
        return False
    for arg in args:
        if arg is not False:
            return arg
    return False

def prim_not(val):
    if val is False:
        return True
    return False

@force_arg_number(1)
def prim_max(*args):
    return max(args)

@force_arg_number(1)
def prim_min(*args):
    return min(args)

@force_number_type
def prim_abs(val):
    return abs(val)

@force_number_type
def prim_gcd(a, b):
    if a < b:
        a, b = b, a
    while a % b != 0:
        a, b = b, a % b
    return b

@force_number_type
def prim_lcm(a, b):
    if a < b:
        a, b = b, a
    while a % b != 0:
        a += a
    return a

@force_number_type
def prim_floor(val):
    return math.floor(val)

@force_number_type
def prim_ceiling(val):
    return math.ceil(val)
    return math.floor(val)
