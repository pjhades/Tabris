# -*- coding: utf-8 -*-

import utils
from errors import *

class Boolean:
    def __init__(self, value):
        self.value = value

    # emulate !, && and ||
    def __mul__(self, other):
        return Boolean(self.value and other.value)
    def __add__(self, other):
        return Boolean(self.value or other.value)
    def __neg__(self, other):
        return Boolean(not self.value)

    @staticmethod
    def true(v):
        if isinstance(v, Boolean) and not v.value:
            return False
        return True

    def __str__(self):
        return '#t' if self.value else '#f'

class String:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

class Procedure:
    def __init__(self, params, body, env, is_prim=False):
        self.params = params # name of params
        self.body = body
        self.env = env
        self.is_prim = is_prim # var arg list if not list
        self.is_var_args = not isinstance(params, list)

    def __str__(self):
        return '<procedure> ' + \
               ('params:{0}, body:{1}, env:{2}'.format(self.params, self.body, self.env) \
               if not self.is_prim else self.body)

