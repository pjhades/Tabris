# -*- coding: utf-8 -*-

import syntax as syn
from errors import *

class Symbol:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return '\'' + str(self.value)

class Pair:
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

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

        print('create pair, car={0} of type {1},   cdr={2} of type {3}'.format(str(self.car), type(self.car), str(self.cdr), type(self.cdr)))

    def _to_str(self):
        # TODO: rethink the s-exp structure
        if not self.car and not self.cdr:
            # empty list
            return ''

        if isinstance(self.car, Symbol) and self.car.value == 'quote' and self.length == 2:
            # simplify (quote x) by 'x
            if isinstance(self.cdr, Symbol):
                return '\'' + self.cdr.value
            else:
                cdr = self.cdr._to_str()
                return '\'' + ('()' if cdr == '' else cdr)

        # the car part without leading single quote
        s = self.car.value if isinstance(self.car, Symbol) else '(' + str(self.car)[1:] + ')'

        if isinstance(self.cdr, Symbol):
            # cdr is a symbol
            return s + ' . ' + self.cdr.value
        else:
            # or we can omit the dot
            cdr = self.cdr._to_str()
            return s + (' (' + cdr + ')' if cdr != '' else '')

    def __str__(self):
        # TODO
        #return '\'(' + self._to_str() + ')'
        return '\'' + self._to_str()
