# -*- coding: utf-8 -*-

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
        if not self.car and not self.cdr or cdr.is_list:
            self.is_list = True
        else:
            self.is_list = False

    @staticmethod
    def chain(expr):
        if not isinstance(expr, list):
            return Symbol(expr)

        if expr == []:
            return Pair('', '')

        if '.' not in expr:
            expr = expr[0:1] + ['.'] + [expr[1:]]

        car = Pair.chain(expr[0])
        cdr = Pair.chain(expr[2])

        return Pair(car, cdr)

    def __str__(self):
        print('(' + self.car)
        if isinstance(self.cdr, Symbol):
            print(' . ' + self.cdr)
        elif self.cdr.is_list:
            print(' ' + self.cdr)
        else:
            print(' . ' + self.cdr)
