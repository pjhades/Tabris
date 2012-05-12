# -*- coding: utf-8 -*-

from errors import *

class Frame(object):
    def __init__(self, varl=[], vall=[], outer=None):
        self.binds = {p[0]: p[1] for p in zip(varl, vall)}
        self.outer = outer

    def refvar(self, var):
        frm = self
        while frm:
            if var not in frm.binds:
                frm = frm.outer
            else:
                return frm.binds[var]
        raise SchemeError('unbound variable ' + var)

    def setvar(self, var, val):
        frm = self
        while frm:
            if var not in frm.binds:
                frm = frm.outer
            else:
                frm.binds[var] = val
                return
        raise SchemeError('unbound variable ' + var)

    def bindvar(self, var, val):
        self.binds[var] = val

    def extend(self, varl, vall):
        for b in zip(varl, vall):
            self.binds[b[0]] = b[1]
