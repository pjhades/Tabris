# -*- coding: utf-8 -*-

import sys
from tsymbol import Symbol
from tpair import Pair, to_str, NIL
from closure import Closure
from insts import LIB_CALLCC_CLOSURE
from trampoline import *
from errors import *

# Base types
def lib_isnumber(val):
    """(number? val)
    """
    return isinstance(val, int) or isinstance(val, float) or isinstance(val, complex) 

def lib_isstring(val):
    """(string? val)
    """
    return isinstance(val, str)

def lib_issymbol(val):
    """(symbol? val)
    """
    return isinstance(val, Symbol)

def lib_isboolean(val):
    """(boolean? val)
    """
    return isinstance(val, bool)

def lib_isnull(val):
    """(null? val)
    """
    return isinstance(val, Pair) and val.islist and val.length == 0

def lib_ispair(val):
    """(pair? val)
    """
    return isinstance(val, Pair)

def lib_isprocedure(val):
    """(procedure? val)
    """
    return isinstance(val, Closure)


# Equivalence predicates
def lib_iseqv(*args):
    prev = args[0]
    for now in args[1:]:
        if lib_isboolean(prev) and lib_isboolean(now) or \
                lib_issymbol(prev) and lib_issymbol(now) or \
                lib_isnumber(prev) and lib_isnumber(now) or \
                lib_isstring(prev) and lib_isstring(now) or \
                lib_isnull(prev) and lib_isnull(now):
            if prev != now:
                return False
        else:
            if not prev is now:
                return False
        prev = now 
    return True

def _lib_isequal(v1, v2, cont):
    def compared_first(result):
        if result is False:
            return False
        return bounce(_lib_isequal, cdr(v1), cdr(v2), cont)

    if not isinstance(v1, Pair) and not isinstance(v2, Pair) or \
            lib_isnull(v1) and lib_isnull(v2):
        # both are not pair or both are '()
        return bounce(cont, lib_iseqv(v1, v2))
    elif isinstance(v1, Pair) and isinstance(v2, Pair):
        # both are pairs
        return bounce(_lib_isequal, car(v1), car(v2), compared_first)
    else:
        return bounce(cont, False)

def lib_isequal(*args):
    """(equal? x1 x2)
    """
    return pogo_stick(bounce(_lib_isequal, args[0], args[1], lambda d:d))


# List and pair operations
def cons(first, second):
    return Pair([first, second])

def _check_cxr_param(cxr):
    """Check if the argument cannot be cxred.
    """
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


def lib_islist(v):
    """(list? p)
    """
    return isinstance(v, Pair) and v.islist


def lib_list(*elems):
    """(list 1 2 3)
    """
    res = NIL
    for elem in reversed(elems):
        res = cons(elem, res)
    return res


def lib_length(p):
    """(length '(1 2 3))
    """
    if not p.islist:
        raise SchemeError('expects proper list, given %s' % (to_str(p)))
    return p.length


def lib_append(*args):
    """(append '(1 2) '(a b)) 
    or
       (append '(1 2) 'x)
    """
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
    if lib_islist(lsts[-1]):
        res.islist = True
    else:
        res.islist = False
    if res.islist:
        res.length = sum([x.length for x in args])
    else:
        res.length = 0

    return res


def lib_reverse(p):
    """(reverse '(a b c))
    """
    elems = []
    while p != NIL:
        elems.append(car(p))
        p = cdr(p)
    return lib_list(*list(reversed(elems)))


def lib_list_tail(p, start):
    """(list-tail '(a b c) 1)
    """
    orig = p
    try:
        now = 0
        while now != start:
            p = cdr(p)
            now += 1
        return p
    except SchemeError:
        raise SchemeError('index %s is too large for %s' % (start, to_str(orig)))


# Control flow related
lib_callcc = LIB_CALLCC_CLOSURE


# Utilities
def lib_display(*args):
    print(*args, end='')
    sys.stdout.flush()
    return None

def lib_newline():
    print()
    sys.stdout.flush()
    return None

