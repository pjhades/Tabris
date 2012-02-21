# -*- coding: utf-8 -*-

"""\
Environment
"""

from typedef import Symbol, Procedure
from errors import *

class Env(object):
    def __init__(self, var_list=[], val_list=[], outer=None):
        self.bindings = {}
        for var, val in zip(var_list, val_list):
            self.bindings[var] = val
        self.outer = outer

    def get_var(self, var):
        e = self
        while e:
            if var not in e.bindings:
                e = e.outer
            else:
                return e.bindings[var]
        raise SchemeError('unbound variable ' + var)

    def add_var(self, var, val):
        self.bindings[var] = val

    def set_var(self, var, val):
        e = self
        while e:
            if var not in e.bindings:
                e = e.outer
            else:
                e.bindings[var] = val
                return
        raise SchemeError('unbound variable ' + var)

def extend_env(var_list, val_list, base_env):
    # `var_list' and `val_list' are python lists
    return Env(var_list, val_list, base_env)

def init_global():
    prim_vars = [
        Symbol('+'),
        Symbol('-'),
        Symbol('*'),
        Symbol('/'),
        Symbol('='),
        Symbol('>'),
        Symbol('<'),
        Symbol('>='),
        Symbol('<=')
    ]

    prim_vals = [
        Procedure(None, '+', None, True),
        Procedure(None, '-', None, True),
        Procedure(None, '*', None, True),
        Procedure(None, '/', None, True),
        Procedure(None, '=', None, True),
        Procedure(None, '>', None, True),
        Procedure(None, '<', None, True),
        Procedure(None, '>=', None, True),
        Procedure(None, '<=', None, True)
    ]

    global_env = Env(prim_vars, prim_vals)
    return global_env
