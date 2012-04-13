# -*- coding: utf-8 -*-

from scmtypes import *
from arith import *
from pair import *

# mapping from primitive body to the actual function
prim_ops = {
    '+': prim_add,
    '-': prim_sub,
    '*': prim_mul,
    '/': prim_div,
    '=': prim_eq,
    '<': prim_lt,
    '>': prim_gt,
    '<=': prim_le,
    '>=': prim_ge,

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

    'number?': number_query,
    'string?': string_query,
    'symbol?': symbol_query, 
    'boolean?': boolean_query
}

# name of primitives to be added to global environment
prim_mappings = {
    Symbol('+'): Procedure(None, '+', None, True),
    Symbol('-'): Procedure(None, '-', None, True),
    Symbol('*'): Procedure(None, '*', None, True),
    Symbol('/'): Procedure(None, '/', None, True),
    Symbol('='): Procedure(None, '=', None, True),
    Symbol('>'): Procedure(None, '>', None, True),
    Symbol('<'): Procedure(None, '<', None, True),
    Symbol('>='): Procedure(None, '>=', None, True),
    Symbol('<='): Procedure(None, '<=', None, True),

    Symbol('cons'): Procedure(None, 'cons', None, True),
                                                                        
    Symbol('car'): Procedure(None, 'car', None, True),
    Symbol('cdr'): Procedure(None, 'cdr', None, True),
                                                                        
    Symbol('caar'): Procedure(None, 'caar', None, True),
    Symbol('cadr'): Procedure(None, 'cadr', None, True),
    Symbol('cdar'): Procedure(None, 'cdar', None, True),
    Symbol('cddr'): Procedure(None, 'cddr', None, True),
                                                                        
    Symbol('caaar'): Procedure(None, 'caaar', None, True),
    Symbol('caadr'): Procedure(None, 'caadr', None, True),
    Symbol('cadar'): Procedure(None, 'cadar', None, True),
    Symbol('caddr'): Procedure(None, 'caddr', None, True),
    Symbol('cdaar'): Procedure(None, 'cdaar', None, True),
    Symbol('cdadr'): Procedure(None, 'cdadr', None, True),
    Symbol('cddar'): Procedure(None, 'cddar', None, True),
    Symbol('cdddr'): Procedure(None, 'cdddr', None, True),
                                                                        
    Symbol('caaaar'): Procedure(None, 'caaaar', None, True),
    Symbol('caaadr'): Procedure(None, 'caaadr', None, True),
    Symbol('caadar'): Procedure(None, 'caadar', None, True),
    Symbol('caaddr'): Procedure(None, 'caaddr', None, True),
    Symbol('cadaar'): Procedure(None, 'cadaar', None, True),
    Symbol('cadadr'): Procedure(None, 'cadadr', None, True),
    Symbol('caddar'): Procedure(None, 'caddar', None, True),
    Symbol('cadddr'): Procedure(None, 'cadddr', None, True),
    Symbol('cdaaar'): Procedure(None, 'cdaaar', None, True),
    Symbol('cdaadr'): Procedure(None, 'cdaadr', None, True),
    Symbol('cdadar'): Procedure(None, 'cdadar', None, True),
    Symbol('cdaddr'): Procedure(None, 'cdaddr', None, True),
    Symbol('cddaar'): Procedure(None, 'cddaar', None, True),
    Symbol('cddadr'): Procedure(None, 'cddadr', None, True),
    Symbol('cdddar'): Procedure(None, 'cdddar', None, True),
    Symbol('cddddr'): Procedure(None, 'cddddr', None, True),
                                                                        
    Symbol('null?'): Procedure(None, 'null?', None, True),
    Symbol('pair?'): Procedure(None, 'pair?', None, True),
    Symbol('list?'): Procedure(None, 'list?', None, True),
    Symbol('list'): Procedure(None, 'list', None, True),
    Symbol('length'): Procedure(None, 'length', None, True),
    Symbol('append'): Procedure(None, 'append', None, True),
    Symbol('reverse'): Procedure(None, 'reverse', None, True),
    Symbol('list-tail'): Procedure(None, 'list-tail', None, True),
                                                                        
    Symbol('number?'): Procedure(None, 'number?', None, True),
    Symbol('string?'): Procedure(None, 'string?', None, True),
    Symbol('symbol?'): Procedure(None, 'symbol?', None, True),
    Symbol('boolean?'): Procedure(None, 'boolean?', None, True),
}

# value of primitives names to be added to global environment
#prim_vals = (
#    # arithmetic_lib.py
#    Procedure(None, '+', None, True),
#    Procedure(None, '-', None, True),
#    Procedure(None, '*', None, True),
#    Procedure(None, '/', None, True),
#    Procedure(None, '=', None, True),
#    Procedure(None, '>', None, True),
#    Procedure(None, '<', None, True),
#    Procedure(None, '>=', None, True),
#    Procedure(None, '<=', None, True),
#
#    # pair_lib.py
#    Procedure(None, 'cons', None, True),
#
#    Procedure(None, 'car', None, True),
#    Procedure(None, 'cdr', None, True),
#
#    Procedure(None, 'caar', None, True),
#    Procedure(None, 'cadr', None, True),
#    Procedure(None, 'cdar', None, True),
#    Procedure(None, 'cddr', None, True),
#
#    Procedure(None, 'caaar', None, True),
#    Procedure(None, 'caadr', None, True),
#    Procedure(None, 'cadar', None, True),
#    Procedure(None, 'caddr', None, True),
#    Procedure(None, 'cdaar', None, True),
#    Procedure(None, 'cdadr', None, True),
#    Procedure(None, 'cddar', None, True),
#    Procedure(None, 'cdddr', None, True),
#
#    Procedure(None, 'caaaar', None, True),
#    Procedure(None, 'caaadr', None, True),
#    Procedure(None, 'caadar', None, True),
#    Procedure(None, 'caaddr', None, True),
#    Procedure(None, 'cadaar', None, True),
#    Procedure(None, 'cadadr', None, True),
#    Procedure(None, 'caddar', None, True),
#    Procedure(None, 'cadddr', None, True),
#    Procedure(None, 'cdaaar', None, True),
#    Procedure(None, 'cdaadr', None, True),
#    Procedure(None, 'cdadar', None, True),
#    Procedure(None, 'cdaddr', None, True),
#    Procedure(None, 'cddaar', None, True),
#    Procedure(None, 'cddadr', None, True),
#    Procedure(None, 'cdddar', None, True),
#    Procedure(None, 'cddddr', None, True),
#
#    Procedure(None, 'null?', None, True),
#    Procedure(None, 'pair?', None, True),
#    Procedure(None, 'list?', None, True),
#    Procedure(None, 'list', None, True),
#    Procedure(None, 'length', None, True),
#    Procedure(None, 'append', None, True),
#    Procedure(None, 'reverse', None, True),
#    Procedure(None, 'list-tail', None, True),
#
#    # type_lib.py
#    Procedure(None, 'number?', None, True),
#    Procedure(None, 'string?', None, True),
#    Procedure(None, 'symbol?', None, True),
#    Procedure(None, 'boolean?', None, True),
#)
