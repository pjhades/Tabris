# -*- coding: utf-8 -*-

from environment import Frame
from closure import Closure
from tsymbol import tsym
from scmlib import *
from prim import *

def init_global():
    return Frame(top_bindings.keys(), top_bindings.values())

def init_compiletime_env():
    return Frame(top_bindings.keys(), 
                 [None]*len(top_bindings),
                 None)

top_bindings = {
    tsym('+'): Closure(None, prim_add, None, isprim=True),
    tsym('-'): Closure(None, prim_sub, None, isprim=True),
    tsym('*'): Closure(None, prim_mul, None, isprim=True),
    tsym('/'): Closure(None, prim_div, None, isprim=True),
    tsym('='): Closure(None, prim_eq, None, isprim=True),
    tsym('>'): Closure(None, prim_gt, None, isprim=True),
    tsym('<'): Closure(None, prim_lt, None, isprim=True),
    tsym('>='): Closure(None, prim_ge, None, isprim=True),
    tsym('<='): Closure(None, prim_le, None, isprim=True),
    tsym('and'): Closure(None, prim_and, None, isprim=True),
    tsym('or'): Closure(None, prim_or, None, isprim=True),
    tsym('not'): Closure(None, prim_not, None, isprim=True),

    tsym('cons'): Closure(None, cons, None, isprim=True),

    tsym('car'): Closure(None, car, None, isprim=True),
    tsym('cdr'): Closure(None, cdr, None, isprim=True),

    tsym('caar'): Closure(None, caar, None, isprim=True),
    tsym('cadr'): Closure(None, cadr, None, isprim=True),
    tsym('cdar'): Closure(None, cdar, None, isprim=True),
    tsym('cddr'): Closure(None, cddr, None, isprim=True),

    tsym('caaar'): Closure(None, caaar, None, isprim=True),
    tsym('caadr'): Closure(None, caadr, None, isprim=True),
    tsym('cadar'): Closure(None, cadar, None, isprim=True),
    tsym('caddr'): Closure(None, caddr, None, isprim=True),
    tsym('cdaar'): Closure(None, cdaar, None, isprim=True),
    tsym('cdadr'): Closure(None, cdadr, None, isprim=True),
    tsym('cddar'): Closure(None, cddar, None, isprim=True),
    tsym('cdddr'): Closure(None, cdddr, None, isprim=True),

    tsym('caaaar'): Closure(None, caaaar, None, isprim=True),
    tsym('caaadr'): Closure(None, caaadr, None, isprim=True),
    tsym('caadar'): Closure(None, caadar, None, isprim=True),
    tsym('caaddr'): Closure(None, caaddr, None, isprim=True),
    tsym('cadaar'): Closure(None, cadaar, None, isprim=True),
    tsym('cadadr'): Closure(None, cadadr, None, isprim=True),
    tsym('caddar'): Closure(None, caddar, None, isprim=True),
    tsym('cadddr'): Closure(None, cadddr, None, isprim=True),
    tsym('cdaaar'): Closure(None, cdaaar, None, isprim=True),
    tsym('cdaadr'): Closure(None, cdaadr, None, isprim=True),
    tsym('cdadar'): Closure(None, cdadar, None, isprim=True),
    tsym('cdaddr'): Closure(None, cdaddr, None, isprim=True),
    tsym('cddaar'): Closure(None, cddaar, None, isprim=True),
    tsym('cddadr'): Closure(None, cddadr, None, isprim=True),
    tsym('cdddar'): Closure(None, cdddar, None, isprim=True),
    tsym('cddddr'): Closure(None, cddddr, None, isprim=True),

    tsym('list'): Closure(None, lib_list, None, isprim=True),
    tsym('null?'): Closure(None, lib_isnull, None, isprim=True),
    tsym('pair?'): Closure(None, lib_ispair, None, isprim=True),
    tsym('list?'): Closure(None, lib_islist, None, isprim=True),
    tsym('length'): Closure(None, lib_length, None, isprim=True),
    tsym('append'): Closure(None, lib_append, None, isprim=True),
    tsym('reverse'): Closure(None, lib_reverse, None, isprim=True),
    tsym('list-tail'): Closure(None, lib_list_tail, None, isprim=True),

    tsym('number?'): Closure(None, lib_isnumber, None, isprim=True),
    tsym('string?'): Closure(None, lib_isstring, None, isprim=True),
    tsym('symbol?'): Closure(None, lib_issymbol, None, isprim=True),
    tsym('boolean?'): Closure(None, lib_isboolean, None, isprim=True),

    tsym('call/cc'): lib_callcc,
    tsym('call-with-current-continuation'): lib_callcc,

    tsym('display'): Closure(None, lib_display, None, isprim=True),
    tsym('newline'): Closure(None, lib_newline, None, isprim=True),

    tsym('eqv?'): Closure(None, lib_iseqv, None, isprim=True),
    tsym('eq?'): Closure(None, lib_iseqv, None, isprim=True),
    tsym('equal?'): Closure(None, lib_isequal, None, isprim=True),
}
