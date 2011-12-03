# -*- coding: utf-8 -*-

import syntax as syn
from errors import *

class Symbol:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return '\'' + str(self.value)

class Pair:
    def __init__(self, car, cdr, code):
        self.car = car
        self.cdr = cdr
        self.code = code

        if not self.car and not self.cdr:
            # empty list
            self.is_list = True
            self.length = 0
        elif isinstance(cdr, Pair) and cdr.is_list:
            # cdr is a list
            self.is_list = True
            self.length = 1 + self.cdr.length
        else:
            self.is_list = False

    def __str__(self):
        return '\'' + self.code
