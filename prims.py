# -*- coding: utf-8 -*-

from scmtypes import Closure
from scmlib import *
from arith import *

# mapping from symbol to closure to be added to global environment
prim_mappings = {
    Symbol('+'): Closure(None, prim_add, None, isprim=True),
    Symbol('-'): Closure(None, prim_sub, None, isprim=True),
    Symbol('*'): Closure(None, prim_mul, None, isprim=True),
    Symbol('/'): Closure(None, prim_div, None, isprim=True),
    Symbol('='): Closure(None, prim_eq, None, isprim=True),
    Symbol('>'): Closure(None, prim_gt, None, isprim=True),
    Symbol('<'): Closure(None, prim_lt, None, isprim=True),
    Symbol('>='): Closure(None, prim_ge, None, isprim=True),
    Symbol('<='): Closure(None, prim_le, None, isprim=True),

    Symbol('cons'): Closure(None, cons, None, isprim=True),

    Symbol('car'): Closure(None, car, None, isprim=True),
    Symbol('cdr'): Closure(None, cdr, None, isprim=True),

    Symbol('caar'): Closure(None, caar, None, isprim=True),
    Symbol('cadr'): Closure(None, cadr, None, isprim=True),
    Symbol('cdar'): Closure(None, cdar, None, isprim=True),
    Symbol('cddr'): Closure(None, cddr, None, isprim=True),

    Symbol('caaar'): Closure(None, caaar, None, isprim=True),
    Symbol('caadr'): Closure(None, caadr, None, isprim=True),
    Symbol('cadar'): Closure(None, cadar, None, isprim=True),
    Symbol('caddr'): Closure(None, caddr, None, isprim=True),
    Symbol('cdaar'): Closure(None, cdaar, None, isprim=True),
    Symbol('cdadr'): Closure(None, cdadr, None, isprim=True),
    Symbol('cddar'): Closure(None, cddar, None, isprim=True),
    Symbol('cdddr'): Closure(None, cdddr, None, isprim=True),

    Symbol('caaaar'): Closure(None, caaaar, None, isprim=True),
    Symbol('caaadr'): Closure(None, caaadr, None, isprim=True),
    Symbol('caadar'): Closure(None, caadar, None, isprim=True),
    Symbol('caaddr'): Closure(None, caaddr, None, isprim=True),
    Symbol('cadaar'): Closure(None, cadaar, None, isprim=True),
    Symbol('cadadr'): Closure(None, cadadr, None, isprim=True),
    Symbol('caddar'): Closure(None, caddar, None, isprim=True),
    Symbol('cadddr'): Closure(None, cadddr, None, isprim=True),
    Symbol('cdaaar'): Closure(None, cdaaar, None, isprim=True),
    Symbol('cdaadr'): Closure(None, cdaadr, None, isprim=True),
    Symbol('cdadar'): Closure(None, cdadar, None, isprim=True),
    Symbol('cdaddr'): Closure(None, cdaddr, None, isprim=True),
    Symbol('cddaar'): Closure(None, cddaar, None, isprim=True),
    Symbol('cddadr'): Closure(None, cddadr, None, isprim=True),
    Symbol('cdddar'): Closure(None, cdddar, None, isprim=True),
    Symbol('cddddr'): Closure(None, cddddr, None, isprim=True),

    Symbol('null?'): Closure(None, lib_isnull, None, isprim=True),
    Symbol('pair?'): Closure(None, lib_ispair, None, isprim=True),
    Symbol('list?'): Closure(None, lib_islist, None, isprim=True),
    Symbol('list'): Closure(None, lib_list, None, isprim=True),
    Symbol('length'): Closure(None, lib_length, None, isprim=True),
    Symbol('append'): Closure(None, lib_append, None, isprim=True),
    Symbol('reverse'): Closure(None, lib_reverse, None, isprim=True),
    Symbol('list-tail'): Closure(None, lib_list_tail, None, isprim=True),

    Symbol('number?'): Closure(None, lib_isnumber, None, isprim=True),
    Symbol('string?'): Closure(None, lib_isstring, None, isprim=True),
    Symbol('symbol?'): Closure(None, lib_issymbol, None, isprim=True),
    Symbol('boolean?'): Closure(None, lib_isboolean, None, isprim=True),
}
