# -*- coding: utf-8 -*-

import copy
from errors import *

class ActivationRecord(object):
    def __init__(self, env, code, retaddr):
        self.env = env
        self.code = code
        self.retaddr = retaddr

# TODO: this need to be modified with a better implementation.
class Continuation(object):
    def __init__(self, vm):
        self.stack = copy.deepcopy(vm.stack)
