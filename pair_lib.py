# -*- coding: utf-8 -*-

"""Pair and list library."""

from basic_type import Boolean
from pair import Pair, to_str, is_list, is_null, is_pair
from errors import *

def cons(first, second):
    return Pair([first, second])

NIL = Pair([])

def _check_cxr_param(cxr):
    """Check if the argument cannot be cxred."""
    def f(func):
        def g(p):
            try:
                return func(p)
            except Exception:
                raise SchemeError('expect %sable pairs, given %s' % (cxr, to_str(p)))
        return g
    return f

@_check_cxr_param('car')
def car(p):
    return p[0]

@_check_cxr_param('cdr')
def cdr(p):
    return p[1]

@_check_cxr_param('caar')
def caar(p):
    return p[0][0]

@_check_cxr_param('cdar')
def cdar(p):
    return p[0][1]

@_check_cxr_param('cadr')
def cadr(p):
    return p[1][0]

@_check_cxr_param('cddr')
def cddr(p):
    return p[1][1]

@_check_cxr_param('caaar')
def caaar(p):
    return p[0][0][0]

@_check_cxr_param('caadr')
def caadr(p):
    return p[1][0][0]

@_check_cxr_param('cadar')
def cadar(p):
    return p[0][1][0]

@_check_cxr_param('caddr')
def caddr(p):
    return p[1][1][0]

@_check_cxr_param('cdaar')
def cdaar(p):
    return p[0][0][1]

@_check_cxr_param('cdadr')
def cdadr(p):
    return p[1][0][1]

@_check_cxr_param('cddar')
def cddar(p):
    return p[0][1][1]

@_check_cxr_param('cdddr')
def cdddr(p):
    return p[1][1][1]

@_check_cxr_param('caaaar')
def caaaar(p):
	return p[0][0][0][0]

@_check_cxr_param('caaadr')
def caaadr(p):
	return p[1][0][0][0]

@_check_cxr_param('caadar')
def caadar(p):
	return p[0][1][0][0]

@_check_cxr_param('caaddr')
def caaddr(p):
	return p[1][1][0][0]

@_check_cxr_param('cadaar')
def cadaar(p):
	return p[0][0][1][0]

@_check_cxr_param('cadadr')
def cadadr(p):
	return p[1][0][1][0]

@_check_cxr_param('caddar')
def caddar(p):
	return p[0][1][1][0]

@_check_cxr_param('cadddr')
def cadddr(p):
	return p[1][1][1][0]

@_check_cxr_param('cdaaar')
def cdaaar(p):
	return p[0][0][0][1]

@_check_cxr_param('cdaadr')
def cdaadr(p):
	return p[1][0][0][1]

@_check_cxr_param('cdadar')
def cdadar(p):
	return p[0][1][0][1]

@_check_cxr_param('cdaddr')
def cdaddr(p):
	return p[1][1][0][1]

@_check_cxr_param('cddaar')
def cddaar(p):
	return p[0][0][1][1]

@_check_cxr_param('cddadr')
def cddadr(p):
	return p[1][0][1][1]

@_check_cxr_param('cdddar')
def cdddar(p):
	return p[0][1][1][1]

@_check_cxr_param('cddddr')
def cddddr(p):
	return p[1][1][1][1]

def null_query(v):
    """(null? p)"""
    return Boolean(is_null(v))

def pair_query(v):
    """(pair? p)"""
    return Boolean(is_pair(v))

def list_query(v):
    """(list? p)"""
    return Boolean(is_list(v))

def make_list(*elems):
    """(list 1 2 3)"""
    res = NIL
    for elem in reversed(elems):
        res = cons(elem, res)
    return res

def get_length(p):
    """(length '(1 2 3))"""
    if not p.islist:
        raise SchemeError('expects proper list, given %s' % (to_str(p)))
    return p.length

def append_lst(*args):
    """(append '(1 2) '(a b))"""
    if len(args) == 0:
        return NIL

    import copy
    lsts = [copy.deepcopy(x) for x in args]
    
    res = lsts[-1]
    for lst in reversed(lsts[:-1]):
        try:
            if lst == NIL:
                continue
            p = lst
            while cdr(p) != NIL:
                p = cdr(p)
            p[1] = res
            res = lst
        except SchemeError:
            raise SchemeError('expects proper list, given %s' % (to_str(p)))

    if not isinstance(res, Pair):
        return res

    res.islist = lsts[-1].islist
    if res.islist:
        res.length = sum([x.length for x in args])
    else:
        res.length = 0

    return res

def reverse_lst(p):
    """(reverse '(a b c))"""
    elems = []
    while p != NIL:
        elems.append(car(p))
        p = cdr(p)
    return make_list(*list(reversed(elems)))

def get_list_tail(p, start):
    """(list-tail '(a b c) 1)"""
    orig = p
    try:
        now = 0
        while now != start:
            p = cdr(p)
            now += 1
        return p
    except SchemeError:
        raise SchemeError('index %s is too large for %s' % (start, to_str(orig)))

