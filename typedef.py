# -*- coding: utf-8 -*-

"""
Type definitions for boolean, symbol, string, procedure
"""

from errors import *

class Boolean:
    def __init__(self, value):
        self.value = value
    def __mul__(self, other):
        return Boolean(self.value and other.value)
    def __add__(self, other):
        return Boolean(self.value or other.value)
    def __neg__(self, other):
        return Boolean(not self.value)
    def __str__(self):
        return '#t' if self.value else '#f'

def is_true(v):
    """v is true if it's not #f."""
    return not isinstance(v, Boolean) or v.value


# Store symbols we have created.
_sym_table = {}

class Symbol(str):
    """Symbols with the same spell will share the same object."""
    def __new__(cls, sym):
        if sym not in _sym_table:
            return str.__new__(cls, sym)
        else:
            return _sym_table[sym]
    def __init__(self, sym):
        _sym_table[sym] = self
    def __eq__(self, other):
        return super().__eq__(other)
    def __cmp__(self, other):
        return super().__cmp__(other)
    def __hash__(self):
        return super().__hash__()


class String:
    def __init__(self, value):
        self.value = value[1:len(value)-1]
    def __str__(self):
        return '"' + self.value + '"'


class Procedure:
    def __init__(self, params, body, env, is_prim=False):
        # this should be a list
        self.params = params
        self.body = body
        self.env = env
        self.is_prim = is_prim 

        # if not list, self.params represents a scheme list
        self.is_var_args = not isinstance(params, list)

    def __str__(self):
        return '<procedure> ' + \
               ('params:{0}, body:{1}, env:{2}'.format(self.params, self.body, self.env) \
                if not self.is_prim else self.body)


def is_boolean(v):
    return isinstance(v, Boolean)

def is_string(v):
    return isinstance(v, String)

def is_symbol(v):
    return isinstance(v, Symbol)

