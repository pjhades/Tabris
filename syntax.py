# -*- coding: utf-8 -*-

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
    while not binds.isnil:
        varl.append(caar(binds))
        binds = cdr(binds)
    return varl

def let_vals(binds):
    vall = []
    while not binds.isnil:
        vall.append(cadar(binds))
        binds = cdr(binds)
    return vall

def scanout_defs(exp):
    """Scan out the definitions, return the list of 
    names that will be bound through such definitions.
    This will be called before the compiler begin to
    work on a sequence.
    """
    current = exp
    varl = []
    while not current.isnil:
        s = car(current)
        if get_sexp_type(s) == 'define':
            if lib_issymbol(cadr(s)):
                varl.append(cadr(s))
            else:
                varl.append(caadr(s))
        current = cdr(current)
    return varl

