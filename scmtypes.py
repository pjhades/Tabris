# -*- coding: utf-8 -*-

_sym_table = {}

# TODO: this should be rewritten
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


class Closure(object):
    def __init__(self, params, body, env, isprim=False, isvararg=False):
        self.params = params
        self.body = body
        self.env = env
        self.isprim = isprim
        self.isvararg = isvararg
    def __call__(self, *args, **kwargs):
        return self.body(*args, **kwargs)
    def __str__(self):
        return '<procedure>'


class ActivationRecord(object):
    def __init__(self, env, code, retaddr):
        self.env = env
        self.code = code
        self.retaddr = retaddr
