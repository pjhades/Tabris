# -*- coding: utf-8 -*-

from scmtypes import Symbol, func_isnumber, func_isboolean, \
        func_isstring, func_issymbol
from pair import *


def isselfeval(exp):
    return func_isnumber(exp) or func_isboolean(exp) or func_isstring(exp)


def issymbol(exp):
    return func_issymbol(exp)


def isquote(exp):
    return func_islist(exp) and car(exp) == Symbol('quote')


def isdefine(exp):
    return func_islist(exp) and car(exp) == Symbol('define')


def isset(exp):
    return func_islist(exp) and car(exp) == Symbol('set!')


def islambda(exp):
    return func_islist(exp) and car(exp) == Symbol('lambda')


def isbegin(exp):
    return func_islist(exp) and car(exp) == Symbol('begin')


def isif(exp):
    return func_islist(exp) and car(exp) == Symbol('if')


def iscond(exp):
    return func_islist(exp) and car(exp) == Symbol('cond')
