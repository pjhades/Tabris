# -*- coding: utf-8 -*-

from scmtypes import Symbol
from scmlib import *


def isselfeval(exp):
    return lib_isnumber(exp) or lib_isboolean(exp) or lib_isstring(exp)


def issymbol(exp):
    return lib_issymbol(exp)


def isquote(exp):
    return lib_islist(exp) and car(exp) == Symbol('quote')


def isdefine(exp):
    return lib_islist(exp) and car(exp) == Symbol('define')


def isset(exp):
    return lib_islist(exp) and car(exp) == Symbol('set!')


def islambda(exp):
    return lib_islist(exp) and car(exp) == Symbol('lambda')


def isbegin(exp):
    return lib_islist(exp) and car(exp) == Symbol('begin')


def isif(exp):
    return lib_islist(exp) and car(exp) == Symbol('if')


def iscond(exp):
    return lib_islist(exp) and car(exp) == Symbol('cond')


def islet(exp):
    return lib_islist(exp) and car(exp) == Symbol('let')


def isletstar(exp):
    return lib_islist(exp) and car(exp) == Symbol('let*')
