# -*- coding: utf-8 -*-

from errors import *
from trampoline import Bounce, pogo_stick

class Pair(list):
    def __eq__(self, v):
        return super(Pair, self).__eq__(v)
    def __str__(self):
        return to_str(self)

def cons(first, second):
    return Pair([first, second])

NIL = Pair([])

def _to_str(p, cont):
    "Give the neat string representation of a pair."
    def done_first(first):
        def done_rest(rest):
            if rest[0] == '(':
                if rest[1:-1] == '':
                    return Bounce(cont, '(' + first + ')')
                else:
                    return Bounce(cont, '(' + first + ' ' + rest[1:-1] + ')')
            else:
                return Bounce(cont, '(' + first + ' . ' + rest + ')')
        return Bounce(_to_str, cdr(p), done_rest)

    if not isinstance(p, Pair):
        return Bounce(cont, str(p))
    if len(p) == 0:
        return Bounce(cont, '()')
    return Bounce(_to_str, car(p), done_first)

def to_str(p):
    return pogo_stick(Bounce(_to_str, p, lambda d:d))

def check_cxr_param(cxr):
    """Check if the argument cannot be cxred."""

    def f(func):
        def g(p):
            if not isinstance(p, Pair):
                raise SchemeError('expect %sable pairs, given %s' % (cxr, to_str(p)))
            try:
                return func(p)
            except Exception:
                raise SchemeError('expect %sable pairs, given %s' % (cxr, to_str(p)))
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


# library for list manipulation
def is_pair(v):
    """(pair? x)"""
    return isinstance(v, Pair) 

def is_null(v):
    """(null? x)"""
    return v == NIL

def make_list(*elems):
    """(list 1 2 3)"""
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

def get_length(p):
    """(length '(1 2 3))"""
    try:
        res = 0
        while p != NIL:
            res += 1
            p = cdr(p)
        return res
    except SchemeError:
        raise SchemeError('expects proper list, given %s' % (to_str(p)))

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

# TODO map, filter, for-each
