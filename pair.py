# -*- coding: utf-8 -*-

from trampoline import Bounce, pogo_stick

class Pair(list):
    def __init__(self, *args, **kwargs):
        super(Pair, self).__init__(*args)
        self.islist = _islist(self)
        self.length = _getlen(self) if self.islist else 0
    def __str__(self):
        return to_str(self)

def _to_str(p, cont):
    """Give the neat string representation of a pair."""
    def done_first(first):
        def done_rest(rest):
            if rest[0] == '(':
                if rest[1:-1] == '':
                    return Bounce(cont, '(' + first + ')')
                else:
                    return Bounce(cont, '(' + first + ' ' + rest[1:-1] + ')')
            else:
                return Bounce(cont, '(' + first + ' . ' + rest + ')')
        return Bounce(_to_str, p[1], done_rest)

    if not isinstance(p, Pair):
        return Bounce(cont, str(p))
    if len(p) == 0:
        return Bounce(cont, '()')
    return Bounce(_to_str, p[0], done_first)

def to_str(p):
    return pogo_stick(Bounce(_to_str, p, lambda d:d))

def to_python_list(lst):
    """Convert a Scheme list back into a Python list."""
    res = []
    NIL = Pair([])
    while not lst == NIL:
        res.append(lst[0])
        lst = lst[1]
    return res

def is_null(v):
    return v == []

def is_pair(v):
    return isinstance(v, Pair) 

def is_list(p):
    return isinstance(p, Pair) and p.islist

def _getlen(p):
    """
    get the length of a list, called when the list
    is created or modified
    """
    ret = 0 
    while p != []:
        ret += 1
        p = p[1]
    return ret 

def _islist(p):
    """
    check if a pair is a list, called when the pair
    is created or modified
    """
    while isinstance(p, Pair):
        if p == []:
            return True
        p = p[1]
    return False

