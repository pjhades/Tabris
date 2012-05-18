# -*- coding: utf-8 -*-

class Symbol(object):
    def __init__(self, sym):
        self.sym = sym

    def __str__(self):
        return self.sym

    def __repr__(self):
        return self.__str__()

    def __cmp__(self, other):
        return self is other

    def __hash__(self):
        return self.sym.__hash__()

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

_sym_table = {}

def tsym(sym):
    if sym in _sym_table:
        return _sym_table[sym]
    else:
        new_sym = Symbol(sym)
        _sym_table[sym] = new_sym
    return new_sym

