# -*- coding: utf-8 -*-

from errors import *

class Closure(object):
    def __init__(self, arity, body, env, isprim=False, isvararg=False):
        self.arity = arity
        self.body = body
        self.env = env
        self.isprim = isprim
        self.isvararg = isvararg

    def check_arity(self, argc):
        """Check if the arguments given satisfy the
        requirement of the closure.
        """
        nmin, nmax = self.arity
        if nmax == -1:
            if argc < nmin:
                raise SchemeError('expects at least %d arguments, given %d' % \
                                  (nmin, argc))
        else:
            if not nmin <= argc <= nmax:
                raise SchemeError('expects %d arguments, given %d' % \
                                  (nmin, argc))

    def primcall(self, args):
        """Call a primitive procedure.
        """
        self.check_arity(len(args))
        try:
            return self.body(*args)
        except TypeError:
            raise SchemeError('bad arguments type')
        except ZeroDivisionError:
            raise SchemeError('divided by zero')

    def __str__(self):
        return '<procedure>'
