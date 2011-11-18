# -*- coding: utf-8 -*-

from errors import *
from types import Procedure

# each env is represented by a dict, new->old, from left to right
all_envs = []
global_env = {}

#TODO: is the environment structure linear at any time?
def lookup_variable(var, env):
    while env:
        if var in env:
            return env[var]
        env = next_env(env)
    raise SchemeUnboundError(var)

def set_variable(var, value, env):
    while env:
        if var in env:
            env[var] = value
            return
        env = next_env(env)
    raise SchemeUnboundError(var)

#TODO: this may be wrong, and needs gc?
def extend_env(var_list, value_list, base_env):
    all_envs.insert(0, {var: val for (var, val) in zip (var_list, value_list)})
    return all_envs[0]

def remove_env(env):
    all_envs.remove(env)

def add_binding(var, value, env):
    env[var] = value

#TODO: this may be wrong, two frames are the same?
def next_env(env):
    if env == global_env:
        return None
    return all_envs[all_envs.index(env) + 1]

def init_env():
    #TODO: add global bindings to global_env, put global_env to all_envs

    # primitives
    global_env['+'] = Procedure('', '+', global_env, True)
    global_env['-'] = Procedure('', '-', global_env, True)
    global_env['*'] = Procedure('', '*', global_env, True)
    global_env['/'] = Procedure('', '/', global_env, True)
    global_env['='] = Procedure('', '=', global_env, True)
    global_env['>'] = Procedure('', '>', global_env, True)
    global_env['<'] = Procedure('', '<', global_env, True)
    global_env['>='] = Procedure('', '>=', global_env, True)
    global_env['<='] = Procedure('', '<=', global_env, True)
    global_env['cons'] = Procedure('', 'cons', global_env, True)
    global_env['car'] = Procedure('', 'car', global_env, True)
    global_env['cdr'] = Procedure('', 'cdr', global_env, True)
    all_envs.append(global_env)
