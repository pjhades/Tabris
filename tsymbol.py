# -*- coding: utf-8 -*-

_sym_table = {}

#class Symbol(object):
#    def __new__(cls, sym):
#        if sym not in _sym_table:
#            return super().__new__(cls)
#        else:
#            return _sym_table[sym]
#
#    def __init__(self, sym):
#        self.sym = sym
#        _sym_table[sym] = self
#
#    def __str__(self):
#        return self.sym
#
#    def __cmp__(self, other):
#        return self is other
#
#    def __hash__(self):
#        return self.sym.__hash__()


class Symbol(str):
    """Symbols with the same spell will share the same object."""
    def __new__(cls, sym):
        if sym not in _sym_table:
            return str.__new__(cls, sym)
        else:
            return _sym_table[sym]

    def __init__(self, sym):
        _sym_table[sym] = self

    def __cmp__(self, other):
        return super(Symbol, self).__cmp__(other)

    def __hash__(self):
        return super(Symbol, self).__hash__()


