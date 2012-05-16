# -*- coding: utf-8 -*-

from errors import *

class Closure(object):
    def __init__(self, params, body, env, isprim=False, isvararg=False):
        self.params = params
        self.body = body
        self.env = env
        self.isprim = isprim
        self.isvararg = isvararg

    def primcall(self, args):
        """Call a primitive procedure."""
        try:
            return self.body(*args)
        except TypeError:
            raise SchemeError('bad arguments')

    def __str__(self):
        return '<procedure>'
