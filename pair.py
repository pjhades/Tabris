# -*- coding: utf-8 -*-

from trampoline import Bounce, pogo_stick

class Pair(list):
    def __init__(self, *args, **kwargs):
        super(Pair, self).__init__(*args)

        if self == []:
            self.islist = True
            self.length =0
            return

        if isinstance(self[1], Pair) and self[1].islist:
            self.islist = True
        else:
            self.islist = False

        if not self.islist:
            self.length = 0
        else:
            self.length = self[1].length + 1

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
    while not lst == []:
        res.append(lst[0])
        lst = lst[1]
    return res


def is_null(v):
    return v == []

def is_pair(v):
    return isinstance(v, Pair) 

def is_list(p):
    return isinstance(p, Pair) and p.islist
