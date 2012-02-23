# -*- coding: utf-8 -*-

from basic_type import Procedure, Symbol
from arithmetic_lib import *
from pair_lib import *
from type_lib import *

# mapping from primitive body to the actual function
prim_ops = {
    # arithmetic_lib.py
    '+': prim_add,
    '-': prim_sub,
    '*': prim_mul,
    '/': prim_div,
    '=': prim_eq,
    '<': prim_lt,
    '>': prim_gt,
    '<=': prim_le,
    '>=': prim_ge,

    # pair_lib.py
    'cons': cons,

    'car': car,
    'cdr': cdr,

    'caar': caar,
    'cadr': cadr,
    'cdar': cdar,
    'cddr': cddr,

    'caaar': caaar,
    'caadr': caadr,
    'cadar': cadar,
    'caddr': caddr,
    'cdaar': cdaar,
    'cdadr': cdadr,
    'cddar': cddar,
    'cdddr': cdddr,

    'caaaar': caaaar,
    'caaadr': caaadr,
    'caadar': caadar,
    'caaddr': caaddr,
    'cadaar': cadaar,
    'cadadr': cadadr,
    'caddar': caddar,
    'cadddr': cadddr,
    'cdaaar': cdaaar,
    'cdaadr': cdaadr,
    'cdadar': cdadar,
    'cdaddr': cdaddr,
    'cddaar': cddaar,
    'cddadr': cddadr,
    'cdddar': cdddar,
    'cddddr': cddddr,

    'null?': null_query,
    'pair?': pair_query,
    'list?': list_query,
    'list': make_list, 
    'length': get_length,
    'append': append_lst,
    'reverse': reverse_lst,
    'list-tail': get_list_tail, 

    # type_lib.py
    'number?': number_query,
    'string?': string_query,
    'symbol?': symbol_query, 
    'boolean?': boolean_query
}

# name of primitives to be added to global environment
prim_vars = (
    # arithmetic_lib.py
    Symbol('+'),
    Symbol('-'),
    Symbol('*'),
    Symbol('/'),
    Symbol('='),
    Symbol('>'),
    Symbol('<'),
    Symbol('>='),
    Symbol('<='),

    # pair_lib.py
    Symbol('cons'),

    Symbol('car'),
    Symbol('cdr'),

    Symbol('caar'),
    Symbol('cadr'),
    Symbol('cdar'),
    Symbol('cddr'),

    Symbol('caaar'),
    Symbol('caadr'),
    Symbol('cadar'),
    Symbol('caddr'),
    Symbol('cdaar'),
    Symbol('cdadr'),
    Symbol('cddar'),
    Symbol('cdddr'),

    Symbol('caaaar'),
    Symbol('caaadr'),
    Symbol('caadar'),
    Symbol('caaddr'),
    Symbol('cadaar'),
    Symbol('cadadr'),
    Symbol('caddar'),
    Symbol('cadddr'),
    Symbol('cdaaar'),
    Symbol('cdaadr'),
    Symbol('cdadar'),
    Symbol('cdaddr'),
    Symbol('cddaar'),
    Symbol('cddadr'),
    Symbol('cdddar'),
    Symbol('cddddr'),

    Symbol('null?'),
    Symbol('pair?'),
    Symbol('list?'),
    Symbol('list'),
    Symbol('length'),
    Symbol('append'),
    Symbol('reverse'),
    Symbol('list-tail'),

    # type_lib.py
    Symbol('number?'),
    Symbol('string?'),
    Symbol('symbol?'),
    Symbol('boolean?'),
)

# value of primitives names to be added to global environment
prim_vals = (
    # arithmetic_lib.py
    Procedure(None, '+', None, True),
    Procedure(None, '-', None, True),
    Procedure(None, '*', None, True),
    Procedure(None, '/', None, True),
    Procedure(None, '=', None, True),
    Procedure(None, '>', None, True),
    Procedure(None, '<', None, True),
    Procedure(None, '>=', None, True),
    Procedure(None, '<=', None, True),

    # pair_lib.py
    Procedure(None, 'cons', None, True),

    Procedure(None, 'car', None, True),
    Procedure(None, 'cdr', None, True),

    Procedure(None, 'caar', None, True),
    Procedure(None, 'cadr', None, True),
    Procedure(None, 'cdar', None, True),
    Procedure(None, 'cddr', None, True),

    Procedure(None, 'caaar', None, True),
    Procedure(None, 'caadr', None, True),
    Procedure(None, 'cadar', None, True),
    Procedure(None, 'caddr', None, True),
    Procedure(None, 'cdaar', None, True),
    Procedure(None, 'cdadr', None, True),
    Procedure(None, 'cddar', None, True),
    Procedure(None, 'cdddr', None, True),

    Procedure(None, 'caaaar', None, True),
    Procedure(None, 'caaadr', None, True),
    Procedure(None, 'caadar', None, True),
    Procedure(None, 'caaddr', None, True),
    Procedure(None, 'cadaar', None, True),
    Procedure(None, 'cadadr', None, True),
    Procedure(None, 'caddar', None, True),
    Procedure(None, 'cadddr', None, True),
    Procedure(None, 'cdaaar', None, True),
    Procedure(None, 'cdaadr', None, True),
    Procedure(None, 'cdadar', None, True),
    Procedure(None, 'cdaddr', None, True),
    Procedure(None, 'cddaar', None, True),
    Procedure(None, 'cddadr', None, True),
    Procedure(None, 'cdddar', None, True),
    Procedure(None, 'cddddr', None, True),

    Procedure(None, 'null?', None, True),
    Procedure(None, 'pair?', None, True),
    Procedure(None, 'list?', None, True),
    Procedure(None, 'list', None, True),
    Procedure(None, 'length', None, True),
    Procedure(None, 'append', None, True),
    Procedure(None, 'reverse', None, True),
    Procedure(None, 'list-tail', None, True),

    # type_lib.py
    Procedure(None, 'number?', None, True),
    Procedure(None, 'string?', None, True),
    Procedure(None, 'symbol?', None, True),
    Procedure(None, 'boolean?', None, True),
)
