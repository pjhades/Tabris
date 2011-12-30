#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import traceback
import parser
from trampoline import *

def ill_fact(n, r):
    if n == 1:
        return fall(r)
    #return bounce(fact, n-1, n*r)
    return sequence(add1, bounce(ill_fact, n-1, n*r))

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
    return fall(n+1)

if __name__ == '__main__':
    sys.setrecursionlimit(10)

    code ="'''''x"

    #code = "''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''x"

    try:
        sexp = parser.parse(parser.Tokenizer().tokenize_single(code + '\n'))[0]
        print(sexp)
    except RuntimeError as e:
        print(e)

    #print(pogo_stick(sequence(add1, bounce(fact, 5, 1))))
    #print(pogo_stick(ill_fact(10, 1)))
