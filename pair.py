# -*- coding: utf-8 -*-

from errors import *

import trampoline

class Pair(list):
    pass

NIL = []

def cons(first, second):
    return Pair([first, second])

def make_list(*elems):
    """Cons the elements to form a Scheme list."""
    res = NIL
    for elem in reversed(elems):
        res = cons(elem, res)
    return res

def car(pair):
    return pair[0]

def cdr(pair):
    return pair[1]
