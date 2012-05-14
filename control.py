# -*- coding: utf-8 -*-

from tpair import from_python_list
from environment import Frame
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


class ActivationRecord(object):
    def __init__(self, env, code, retaddr):
        self.env = env
        self.code = code
        self.retaddr = retaddr

 
class Continuation(object):
    def __init__(self, vm):
        import copy
        self.stack = copy.deepcopy(vm.stack)
