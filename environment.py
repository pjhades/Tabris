# -*- coding: utf-8 -*-

from errors import *

class Frame(object):
    def __init__(self, binds, outer=None):
        self.binds = binds
        self.outer = outer

    def get_lexaddr(self, var):
        """Return the lexical address of symbol `var'.
        If it's found in the global bindings, return
        its index in it. Otherwise return the number
        of frames to go back and the index.
        """
        frm = self
        back = 0
        while frm is not None:
            if var not in frm.binds:
                frm = frm.outer
                back += 1
            else:
                if frm.outer is None:
                    return frm.binds.index(var)
                return (back, frm.binds.index(var))
        raise SchemeError('unbound variable: ' + str(var))

    def refvar(self, lexaddr):
        """Reference a non-toplevel name.
        """
        back, idx = lexaddr
        frm = self
        while back > 0:
            frm = frm.outer
            back -= 1
        return frm.binds[idx]

    def setvar(self, lexaddr, val):
        """Set a non-toplevel name.
        """
        back, idx = lexaddr
        frm = self
        while back > 0:
            frm = frm.outer
            back -= 1
        frm.binds[idx] = val

    def bindvar(self, lexaddr, val):
        if lexaddr == len(self.binds):
            self.binds.append(val)
        else:
            self.binds[lexaddr] = val

