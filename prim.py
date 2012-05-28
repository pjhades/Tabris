# -*- coding: utf-8 -*-

import math
from scmlib import lib_isnumber
from errors import *

def prim_add(*args):
    return sum(args)

def prim_sub(*args):
    if len(args) == 1:
        return -args[0]
    result = args[0]
    for arg in args[1:]:
        result -= arg
    return result

def prim_mul(*args):
    result = 1
    for arg in args:
        result *= arg
    return result

def prim_div(*args):
    if len(args) == 1:
        return 1 / args[0]
    result = args[0]
    for arg in args[1:]:
        result /= arg
    return result

def prim_mod(a, b):
    return a % b

def prim_eq(*args):
    for arg in args[1:]:
        if arg != args[0]:
            return False
    return True

def prim_lt(*args):
    pre = args[0]
    for arg in args[1:]:
        if pre >= arg:
            return False
        pre = arg
    return True

def prim_le(*args):
    pre = args[0]
    for arg in args[1:]:
        if pre > arg:
            return False
        pre = arg
    return True

def prim_gt(*args):
    pre = args[0]
    for arg in args[1:]:
        if pre <= arg:
            return False
        pre = arg
    return True

def prim_ge(*args):
    pre = args[0]
    for arg in args[1:]:
        if pre < arg:
            return False
        pre = arg
    return True

def prim_and(*args):
    if False in args:
        return False
    if len(args) == 0:
        return True
    return args[-1]

def prim_or(*args):
    for arg in args:
        if arg is not False:
            return arg
    return False

def prim_not(val):
    if val is False:
        return True
    return False

def prim_max(*args):
    return max(args)

def prim_min(*args):
    return min(args)

def prim_abs(val):
    return abs(val)

def prim_gcd(a, b):
    if a < b:
        a, b = b, a
    while a % b != 0:
        a, b = b, a % b
    return b

def prim_lcm(a, b):
    if a < b:
        a, b = b, a
    while a % b != 0:
        a += a
    return a

def prim_floor(val):
    return math.floor(val)

def prim_ceiling(val):
    return math.ceil(val)
