#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import traceback
import parser
import pair
from trampoline import *

def fact(n, r):
    if n == 1:
        return fall(r)
    return bounce(fact, n-1, n*r)

def mem(n, ls):
    if len(ls) == 0:
        return fall(False)
    if ls[0] == n:
        return fall(True)
    return bounce(mem, n, ls[1:])

def add1(n):
    #print('add1(): n=', n)
    return fall(n+1)

def to_str(p):
    if not isinstance(p, pair.Pair):
        return fall(str(p))

    if len(p) == 0:
        return fall('()')

    def f(car):
        def g(cdr):
            if cdr[0] == '(':
                if cdr[1:-1] == '':
                    return fall('(' + car + ')')
                else:
                    return fall('(' + car + ' ' + cdr[1:-1] + ')')
            else:
                return fall('(' + car + ' . ' + cdr + ')')
        return sequence([g], bounce(to_str, p[1]))

    return sequence([f], bounce(to_str, p[0]))

if __name__ == '__main__':
    sys.setrecursionlimit(15)

    #code = "lambda"
    code = "'"*10000 + "x"

    try:
        exp = parser.parse(parser.Tokenizer().tokenize_single(code + '\n'))[0]
        print(pogo_stick(to_str(exp)))
    except RuntimeError as e:
        print('this can never happen')

