# -*- coding: utf-8 -*-

from environment import Frame
from closure import Closure
from tsymbol import tsym
from scmlib import *
from prim import *

def init_compiletime_env():
    return Frame(list(top_bindings.keys()))

def init_runtime_env():
    return Frame(list(top_bindings.values()))

top_bindings = {
    tsym('+'): Closure((0, -1), prim_add, None, isprim=True),
    tsym('-'): Closure((1, -1), prim_sub, None, isprim=True),
    tsym('*'): Closure((0, -1), prim_mul, None, isprim=True),
    tsym('/'): Closure((1, -1), prim_div, None, isprim=True),
    tsym('='): Closure((2, -1), prim_eq, None, isprim=True),
    tsym('>'): Closure((2, -1), prim_gt, None, isprim=True),
    tsym('<'): Closure((2, -1), prim_lt, None, isprim=True),
    tsym('>='): Closure((2, -1), prim_ge, None, isprim=True),
    tsym('<='): Closure((2, -1), prim_le, None, isprim=True),
    tsym('or'): Closure((0, -1), prim_or, None, isprim=True),
    tsym('and'): Closure((0, -1), prim_and, None, isprim=True),
    tsym('not'): Closure((1, 1), prim_not, None, isprim=True),
    tsym('max'): Closure((1, -1), prim_max, None, isprim=True),
    tsym('min'): Closure((1, -1), prim_min, None, isprim=True),
    tsym('abs'): Closure((1, 1), prim_abs, None, isprim=True),
    tsym('gcd'): Closure((2, 2), prim_gcd, None, isprim=True),
    tsym('lcm'): Closure((2, 2), prim_lcm, None, isprim=True),
    tsym('floor'): Closure((1, 1), prim_floor, None, isprim=True),
    tsym('ceiling'): Closure((1, 1), prim_ceiling, None, isprim=True),
    tsym('remainder'): Closure((2, 2), prim_mod, None, isprim=True),

    tsym('cons'): Closure((2, 2), cons, None, isprim=True),

    tsym('car'): Closure((1, 1), car, None, isprim=True),
    tsym('cdr'): Closure((1, 1), cdr, None, isprim=True),

    tsym('caar'): Closure((1, 1), caar, None, isprim=True),
    tsym('cadr'): Closure((1, 1), cadr, None, isprim=True),
    tsym('cdar'): Closure((1, 1), cdar, None, isprim=True),
    tsym('cddr'): Closure((1, 1), cddr, None, isprim=True),

    tsym('caaar'): Closure((1, 1), caaar, None, isprim=True),
    tsym('caadr'): Closure((1, 1), caadr, None, isprim=True),
    tsym('cadar'): Closure((1, 1), cadar, None, isprim=True),
    tsym('caddr'): Closure((1, 1), caddr, None, isprim=True),
    tsym('cdaar'): Closure((1, 1), cdaar, None, isprim=True),
    tsym('cdadr'): Closure((1, 1), cdadr, None, isprim=True),
    tsym('cddar'): Closure((1, 1), cddar, None, isprim=True),
    tsym('cdddr'): Closure((1, 1), cdddr, None, isprim=True),

    tsym('caaaar'): Closure((1, 1), caaaar, None, isprim=True),
    tsym('caaadr'): Closure((1, 1), caaadr, None, isprim=True),
    tsym('caadar'): Closure((1, 1), caadar, None, isprim=True),
    tsym('caaddr'): Closure((1, 1), caaddr, None, isprim=True),
    tsym('cadaar'): Closure((1, 1), cadaar, None, isprim=True),
    tsym('cadadr'): Closure((1, 1), cadadr, None, isprim=True),
    tsym('caddar'): Closure((1, 1), caddar, None, isprim=True),
    tsym('cadddr'): Closure((1, 1), cadddr, None, isprim=True),
    tsym('cdaaar'): Closure((1, 1), cdaaar, None, isprim=True),
    tsym('cdaadr'): Closure((1, 1), cdaadr, None, isprim=True),
    tsym('cdadar'): Closure((1, 1), cdadar, None, isprim=True),
    tsym('cdaddr'): Closure((1, 1), cdaddr, None, isprim=True),
    tsym('cddaar'): Closure((1, 1), cddaar, None, isprim=True),
    tsym('cddadr'): Closure((1, 1), cddadr, None, isprim=True),
    tsym('cdddar'): Closure((1, 1), cdddar, None, isprim=True),
    tsym('cddddr'): Closure((1, 1), cddddr, None, isprim=True),

    tsym('list'): Closure((0, -1), lib_list, None, isprim=True),
    tsym('null?'): Closure((1, 1), lib_isnull, None, isprim=True),
    tsym('pair?'): Closure((1, 1), lib_ispair, None, isprim=True),
    tsym('list?'): Closure((1, 1), lib_islist, None, isprim=True),
    tsym('length'): Closure((1, 1), lib_length, None, isprim=True),
    tsym('append'): Closure((0, -1), lib_append, None, isprim=True),
    tsym('reverse'): Closure((1, 1), lib_reverse, None, isprim=True),
    tsym('list-tail'): Closure((2, 2), lib_list_tail, None, isprim=True),

    tsym('number?'): Closure((1, 1), lib_isnumber, None, isprim=True),
    tsym('string?'): Closure((1, 1), lib_isstring, None, isprim=True),
    tsym('symbol?'): Closure((1, 1), lib_issymbol, None, isprim=True),
    tsym('boolean?'): Closure((1, 1), lib_isboolean, None, isprim=True),

    tsym('call/cc'): lib_callcc,
    tsym('call-with-current-continuation'): lib_callcc,

    tsym('display'): Closure((1, -1), lib_display, None, isprim=True),
    tsym('newline'): Closure((0, 0), lib_newline, None, isprim=True),

    tsym('eqv?'): Closure((2, -1), lib_iseqv, None, isprim=True),
    tsym('eq?'): Closure((2, -1), lib_iseqv, None, isprim=True),
    tsym('equal?'): Closure((2, -1), lib_isequal, None, isprim=True),

    tsym('exit'): Closure((0, 0), lib_exit, None, isprim=True),
}
