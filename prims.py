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

    'null?': func_isnull,
    'pair?': func_ispair,
    'list?': func_islist,
    'list': func_list, 
    'length': func_length,
    'append': func_append,
    'reverse': func_reverse,
    'list-tail': func_listtail, 

    'number?': func_isnumber,
    'string?': func_isstring,
    'symbol?': func_issymbol, 
    'boolean?': func_isboolean
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
