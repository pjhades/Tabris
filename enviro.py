# -*- coding: utf-8 -*-

"""\
Environment
"""

from errors import *

class Env:
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
    return Env(var_list, val_list, base_env)

def init_global():
    from typedef import Symbol
    from number import Rational
    global_env = Env()
    return global_env
    #TODO: add initial bindings to global env
