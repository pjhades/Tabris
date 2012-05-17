# -*- coding: utf-8 -*-

from tsymbol import Symbol
from scmlib import *

forms = (
    'if', 
    'let', 
    'let*', 
    'set!', 
    'cond', 
    'quote',
    'begin', 
    'define', 
    'lambda', 
    'letrec',
)

def isselfeval(exp):
    return lib_isnumber(exp) or lib_isboolean(exp) or lib_isstring(exp)

def issymbol(exp):
    return lib_issymbol(exp)

def get_sexp_type(exp):
    if lib_issymbol(exp):
        return 'symbol'
    elif lib_isnumber(exp) or lib_isboolean(exp) or lib_isstring(exp):
        return 'selfeval'
    else:
        first = str(car(exp))
        if first == 'let' and lib_length(exp) >= 4:
            return 'namedlet'
        elif first in forms:
            return str(car(exp))
        else:
            return 'apply'

def let_vars(binds):
    varl = []
    while binds != []:
        varl.append(caar(binds))
        binds = cdr(binds)
    return varl

def let_vals(binds):
    vall = []
    while binds != []:
        vall.append(cadar(binds))
        binds = cdr(binds)
    return vall

