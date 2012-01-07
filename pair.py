# -*- coding: utf-8 -*-

from errors import *

import trampoline

class Pair(list):
    def __eq__(self, v):
        return super().__eq__(v)


NIL = Pair([])


def is_pair(v):
    return isinstance(v, Pair) 

def is_null(v):
    return v == NIL


def cons(first, second):
    return Pair([first, second])

def make_list(*elems):
    """Cons the elements to form a Scheme list."""

    res = NIL
    for elem in reversed(elems):
        res = cons(elem, res)
    return res

def to_python_list(lst):
    """Convert a Scheme list back into a Python list."""
    res = []
    while not is_null(lst):
        res.append(car(lst))
        lst = cdr(lst)
    return res

def is_list(p):
    """Tell if a pair is a list."""

    while isinstance(p, Pair):
        if len(p) == 0:
            return True
        p = cdr(p)
    return False


def _to_str(p):
    """Give the neat string representation of a pair."""

    def f(first):
        def g(rest):
            if rest[0] == '(':
                if rest[1:-1] == '':
                    return trampoline.fall('(' + first + ')')
                else:
                    return trampoline.fall('(' + first + ' ' + rest[1:-1] + ')')
            else:
                return trampoline.fall('(' + first + ' . ' + rest + ')')
        return trampoline.sequence([g], trampoline.bounce(_to_str, p[1]))

    if not isinstance(p, Pair):
        return trampoline.fall(str(p))
    if len(p) == 0:
        return trampoline.fall('()')
    return trampoline.sequence([f], trampoline.bounce(_to_str, p[0]))

def to_str(p):
    return trampoline.pogo_stick(_to_str(p))


def check_cxr_param(cxr):
    """Check if the argument cannot be cxred."""

    def f(func):
        def g(p):
            if not isinstance(p, Pair):
                raise SchemeEvalError('expect {0}able pairs, given {1}'.format(cxr, to_str(p)))
            try:
                return func(p)
            except Exception:
                raise SchemeEvalError('expect {0}able pairs, given {1}'.format(cxr, to_str(p)))
        return g
    return f


# c*r operations for pair manipulation
@check_cxr_param('car')
def car(p):
    return p[0]

@check_cxr_param('cdr')
def cdr(p):
    return p[1]

@check_cxr_param('caar')
def caar(p):
    return p[0][0]

@check_cxr_param('cdar')
def cdar(p):
    return p[0][1]

@check_cxr_param('cadr')
def cadr(p):
    return p[1][0]

@check_cxr_param('cddr')
def cddr(p):
    return p[1][1]

@check_cxr_param('caaar')
def caaar(p):
    return p[0][0][0]

@check_cxr_param('caadr')
def caadr(p):
    return p[1][0][0]

@check_cxr_param('cadar')
def cadar(p):
    return p[0][1][0]

@check_cxr_param('caddr')
def caddr(p):
    return p[1][1][0]

@check_cxr_param('cdaar')
def cdaar(p):
    return p[0][0][1]

@check_cxr_param('cdadr')
def cdadr(p):
    return p[1][0][1]

@check_cxr_param('cddar')
def cddar(p):
    return p[0][1][1]

@check_cxr_param('cdddr')
def cdddr(p):
    return p[1][1][1]

@check_cxr_param('caaaar')
def caaaar(p):
	return p[0][0][0][0]

@check_cxr_param('caaadr')
def caaadr(p):
	return p[1][0][0][0]

@check_cxr_param('caadar')
def caadar(p):
	return p[0][1][0][0]

@check_cxr_param('caaddr')
def caaddr(p):
	return p[1][1][0][0]

@check_cxr_param('cadaar')
def cadaar(p):
	return p[0][0][1][0]

@check_cxr_param('cadadr')
def cadadr(p):
	return p[1][0][1][0]

@check_cxr_param('caddar')
def caddar(p):
	return p[0][1][1][0]

@check_cxr_param('cadddr')
def cadddr(p):
	return p[1][1][1][0]

@check_cxr_param('cdaaar')
def cdaaar(p):
	return p[0][0][0][1]

@check_cxr_param('cdaadr')
def cdaadr(p):
	return p[1][0][0][1]

@check_cxr_param('cdadar')
def cdadar(p):
	return p[0][1][0][1]

@check_cxr_param('cdaddr')
def cdaddr(p):
	return p[1][1][0][1]

@check_cxr_param('cddaar')
def cddaar(p):
	return p[0][0][1][1]

@check_cxr_param('cddadr')
def cddadr(p):
	return p[1][0][1][1]

@check_cxr_param('cdddar')
def cdddar(p):
	return p[0][1][1][1]

@check_cxr_param('cddddr')
def cddddr(p):
	return p[1][1][1][1]

