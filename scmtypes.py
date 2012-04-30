# -*- coding: utf-8 -*-

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
        return super(Symbol, self).__eq__(other)
    def __cmp__(self, other):
        return super(Symbol, self).__cmp__(other)
    def __hash__(self):
        return super(Symbol, self).__hash__()


class Procedure(object):
    def __init__(self, params, body, env, is_prim=False):
        """
        If (lambda args ...), `params' is not a python list, then
        it's a argument list, `is_var_args' is true. otherwise
        else `params' is a python list, `is_var_args' is false.
        """
        self.params = params
        self.body = body
        self.env = env
        self.is_prim = is_prim 
        self.is_var_args = not isinstance(params, list)

    def __str__(self):
        return '[procedure]'


def func_isnumber(v):
    return isinstance(v, int) or isinstance(v, float) or isinstance(v, complex) 


def func_isstring(v):
    return isinstance(v, str)


def func_issymbol(v):
    return isinstance(v, Symbol)


def func_isboolean(v):
    return isinstance(v, bool)

