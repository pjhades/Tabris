# -*- coding: utf-8 -*-

from errors import *
from stypes import Procedure

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
        raise SchemeUnboundError(var)

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
        raise SchemeUnboundError(var)

def extend_env(var_list, value_list, base_env):
    return Env(var_list, value_list, base_env)

global_env = Env()

def init_env():
    global_env.add_var('+', Procedure('', '+', global_env, is_prim=True))
    global_env.add_var('-', Procedure('', '-', global_env, is_prim=True))
    global_env.add_var('*', Procedure('', '*', global_env, is_prim=True))
    global_env.add_var('/', Procedure('', '/', global_env, is_prim=True))
    global_env.add_var('=', Procedure('', '=', global_env, is_prim=True))
    global_env.add_var('>', Procedure('', '>', global_env, is_prim=True))
    global_env.add_var('<', Procedure('', '<', global_env, is_prim=True))
    global_env.add_var('>=', Procedure('', '>=', global_env, is_prim=True))
    global_env.add_var('<=', Procedure('', '<=', global_env, is_prim=True))
