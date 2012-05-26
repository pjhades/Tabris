# -*- coding: utf-8 -*-

from scmlib import *

# TODO: change these names to integer constant
# to save comparing and equality checking time
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
    """Get a unique type string of each S-expression type.
    """
    if lib_issymbol(exp):
        return 'symbol'
    elif lib_isnumber(exp) or lib_isboolean(exp) or lib_isstring(exp):
        return 'selfeval'
    else:
        first = str(car(exp))
        if first == 'let' and lib_issymbol(cadr(exp)):
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

