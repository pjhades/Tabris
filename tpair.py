# -*- coding: utf-8 -*-

from trampoline import bounce, pogo_stick
from errors import *

class Pair(object):
    def __init__(self, elems):
        self.elems = elems

        if elems == []:
            self.islist = True
            self.length = 0
            return

        if isinstance(elems[1], Pair) and elems[1].islist:
            self.islist = True
            self.length = elems[1].length + 1
        else:
            self.islist = False
            self.length = 0 

    @property
    def isnil(self):
        return self.elems == []

    def __eq__(self, other):
        return isinstance(other, Pair) and self.elems == other.elems

    def __getitem__(self, key):
        return self.elems[key]
    def __setitem__(self, key, val):
        self.elems[key] = val

    def __str__(self):
        return to_str(self)
    def __repr__(self):
        return to_str(self)


NIL = Pair([])


def _to_str(p, cont):
    """Give the neat string representation of a pair.
    """
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
    if p.isnil:
        return bounce(cont, '()')
    return bounce(_to_str, p[0], done_first)

def to_str(p):
    return pogo_stick(bounce(_to_str, p, lambda d:d))

def _to_python_list(scmlist, pylist, cont):
    """Convert a Scheme list into a Python list.
    """
    def got_first(first):
        nonlocal pylist
        pylist.append(first)
        return bounce(_to_python_list, scmlist[1], pylist, cont)

    if scmlist.isnil:
        return bounce(cont, pylist)

    if isinstance(scmlist[0], Pair):
        return bounce(_to_python_list, scmlist[0], [], got_first)

    pylist.append(scmlist[0])
    return bounce(_to_python_list, scmlist[1], pylist, cont)

def to_python_list(scmlist):
    return pogo_stick(bounce(_to_python_list, scmlist, [], lambda d:d))

def _from_python_list(pylist, scmlist, cont):
    """Produce a Scheme list from a Python list.
    """
    def got_first(first):
        nonlocal scmlist
        scmlist = Pair([first, scmlist])
        return bounce(_from_python_list, pylist[1:], scmlist, cont)

    if pylist == []:
        return bounce(cont, scmlist)

    if isinstance(pylist[0], list):
        return bounce(_from_python_list, list(reversed(pylist[0])), NIL, got_first)

    scmlist = Pair([pylist[0], scmlist])
    return bounce(_from_python_list, pylist[1:], scmlist, cont)

def from_python_list(pylist):
    return pogo_stick(bounce(_from_python_list, list(reversed(pylist)), NIL, lambda d:d))
