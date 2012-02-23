# -*- coding: utf-8 -*-

class String(object):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return '"' + self.value + '"'
    def __eq__(self, other):
        return self.value == other.value

def is_string(v):
    return isinstance(v, String)

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
        return super(Symbol, self).__eq__(other)
    def __cmp__(self, other):
        return super(Symbol, self).__cmp__(other)
    def __hash__(self):
        return super(Symbol, self).__hash__()

def is_symbol(v):
    return isinstance(v, Symbol)


class Boolean(object):
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
    def __eq__(self, other):
        return self.value == other.value

def is_true(v):
    """v is true if it's not #f."""
    return not isinstance(v, Boolean) or v.value

def is_boolean(v):
    return isinstance(v, Boolean)

class Procedure(object):
    def __init__(self, params, body, env, is_prim=False):
        """\
        if (lambda args ...), `params' is not a python list, then
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

