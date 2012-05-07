# -*- coding: utf-8 -*-

from trampoline import bounce, pogo_stick
from errors import *

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
                    return bounce(cont, '(' + first + ')')
                else:
                    return bounce(cont, '(' + first + ' ' + rest[1:-1] + ')')
            else:
                return bounce(cont, '(' + first + ' . ' + rest + ')')
        return bounce(_to_str, p[1], done_rest)

    if not isinstance(p, Pair):
        return bounce(cont, str(p))
    if len(p) == 0:
        return bounce(cont, '()')
    return bounce(_to_str, p[0], done_first)


def to_str(p):
    return pogo_stick(bounce(_to_str, p, lambda d:d))


def to_python_list(scmlist):
    """Convert a Scheme list back into a Python list."""
    res = []
    while not scmlist == []:
        res.append(scmlist[0])
        scmlist = scmlist[1]
    return res


def from_python_list(pylist):
    """Produce a Scheme list from a Python list."""
    res = Pair([])
    for x in reversed(pylist):
        res = Pair([x, res])
    return Pair(res)
