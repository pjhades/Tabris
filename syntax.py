# -*- coding: utf-8 -*-

from errors import *

import re

RESERVED = ('define', 'if', 'cond', 'else', 'let', 'quote', 'begin', \
            'lambda', 'set!')

RE_STRING = re.compile(r'^".*"$', flags = re.DOTALL)
RE_INTEGER = re.compile(r'^[+-]?\d+$')
RE_DECIMAL = re.compile(r'^[+-]?(\d+\.\d*|\.\d+)$')
RE_FRACTION = re.compile(r'^[+-]?\d+/\d+$')
# fuck this, just the repetition
RE_COMPLEX = re.compile(r'''(    # both real and imaginary part
                              ^( ([+-]?\d+              | # real is integer
                                  [+-]?(\d+\.\d*|\.\d+) | # real is decimal
                                  [+-]?\d+/\d+)           # real is fraction

                                 ([+-]                  |
                                  [+-]\d+              |
                                  [+-](\d+\.\d*|\.\d+) |
                                  [+-]\d+/\d+)i$ ) 
                                                        |
                                 # no real part
                               ^ ([+-]                 | # imaginary==1 or -1
                                  [+-]?\d+              |
                                  [+-]?(\d+\.\d*|\.\d+) |
                                  [+-]?\d+/\d+)i$ )
                                ''', flags=re.VERBOSE)
RE_IDENTIFIER = re.compile(r'^([+-]|[+-]?[a-zA-Z!$%&*/:<=>?^_~@][\w!$%&*/:<=>?^_~@\.+-]*)$')
RE_SHARP = re.compile(r'^#[tf]$')

def parse(tokens):
    """
        Perform syntax analysis, construct the syntax tree
        represented by a nested list.
    """
    expr_stack = [[]]

    for tok in tokens:
        if tok == '(':
            expr_stack.append([])
        elif tok == ')':
            #if len(expr_stack) == 1:
            #    return expr_stack[0]
            expr_stack[-2].append(expr_stack.pop())
            while expr_stack[-1][0] == 'quote\'':
                expr_stack[-2].append(expr_stack.pop())
        elif tok == '\'':
            expr_stack.append(['quote\''])
        else:
            expr_stack[-1].append(tok)
            while expr_stack[-1][0] == 'quote\'':
                expr_stack[-2].append(expr_stack.pop())

    return expr_stack[0]

def is_string(expr):
    return not isinstance(expr, list) and \
           RE_STRING.search(expr) != None

def is_integer(expr):
    return not isinstance(expr, list) and \
           RE_INTEGER.search(expr) != None

def is_decimal(expr):
    return not isinstance(expr, list) and \
           RE_DECIMAL.search(expr) != None

def is_fraction(expr):
    return not isinstance(expr, list) and \
           RE_FRACTION.search(expr) != None

def is_complex(expr):
    return not isinstance(expr, list) and \
           RE_COMPLEX.search(expr) != None

def is_identifier(expr):
    return not isinstance(expr, list) and \
           not expr in RESERVED and \
           RE_IDENTIFIER.search(expr) != None

def is_sharp(expr):
    return not isinstance(expr, list) and RE_SHARP.search(expr) != None

def get_expr_type(expr):
    if expr == []:
        raise SchemeBadSyntaxError(expr, 'misssing procedure expression')
    return expr[0]

# define
# (define foo <expr>)
# (define (foo arg1 arg2 arg3)
#     <expr1>
#     <expr2>
#     <expr3>)
def check_define(expr):
    if len(expr) < 3:
        raise SchemeBadSyntaxError(expr, 'bad define syntax')
    if isinstance(expr[1], list):
        if list in [type(x) for x in expr[1]]:
            raise SchemeBadSyntaxError(expr, 'bad define syntax')
        if not is_identifier(expr[1][0]):
            raise SchemeBadSyntaxError(expr, 'not a valid identifier')
    else:
        if len(expr) > 3:
            raise SchemeBadSyntaxError(expr, 'multiple expressions after identifier')
        if not is_identifier(expr[1]):
            raise SchemeBadSyntaxError(expr, 'not a valid identifier')

def define_var(expr):
    return expr[1] if not isinstance(expr[1], list) else expr[1][0]

def define_value(expr):
    return expr[2] if not isinstance(expr[1], list) else make_lambda(expr[1][1:], expr[2:])

# set!
# (set! var <expr>)
def check_set(expr):
    if len(expr) != 3:
        raise SchemeBadSyntaxError(expr, 'bad set! syntax')
    if not is_identifier(expr[1]):
        raise SchemeBadSyntaxError(expr, 'not a valid identifier')

def set_var(expr):
    return expr[1]

def set_value(expr):
    return expr[2]

# quote
# (quote a)
def check_quote(expr):
    if len(expr) != 2:
        raise SchemeBadSyntaxError(expr, 'bad quote syntax')

# if
# (if <predicate>
#     <consequent>
#     <alternative>)
def check_if(expr):
    if len(expr) != 3 and len(expr) != 4:
        raise SchemeBadSyntaxError(expr, 'bad if syntax')

def if_pred(expr):
    return expr[1]

def if_yes(expr):
    return expr[2]

def if_has_no(expr):
    return len(expr) == 4

def if_no(expr):
    return expr[3]

# lambda
# (lambda (arg1 arg2 arg3)
#     <expr1>
#     <expr2>
#     <expr3>)
def check_lambda(expr):
    if len(expr) < 3:
        raise SchemeBadSyntaxError(expr, 'bad lambda syntax')

def lambda_params(expr):
    return expr[1]

def lambda_body(expr):
    return expr[2:]

def make_lambda(args, body):
    return ['lambda', args] + body

# begin
# (begin <expr1>
#        <expr2>
#        <expr3>)
def check_begin(expr):
    if len(expr) < 2:
        raise SchemeBadSyntaxError(expr, 'empty begin form')

def begin_exprs(expr):
    return expr[1:]

# cond
# (cond (<predicate1> <consequent1>)
#       (<predicate2> <consequent2>)
#       (<predicate2> => <recipient>)
#       (else <alternative>))
def check_cond(expr):
    if len(expr) < 2:
        raise SchemeBadSyntaxError(expr, 'no cond clauses')
    if [x for x in expr[1:] if len(x) < 2] != []:
        raise SchemeBadSyntaxError(expr, 'cond clause has no action')
    if [x for x in expr[1:] if x[1] == '=>' and len(x) != 3] != []:
        raise SchemeBadSyntaxError(expr, 'bad cond => syntax')
    if [x[0] for x in expr[1:]].index('else') != len(expr[1:]) - 1:
        raise SchemeBadSyntaxError(expr, 'else clause is not the last one')

def cond_has_else(expr):
    return expr[-1][0] == 'else'

def cond_clauses(expr):
    return expr[1:-1] if cond_has_else(expr) else expr[1:]

def cond_else(expr):
    return expr[-1]

# let
# (let ((var1 <expr1>)
#       (var2 <expr2>))
#    <body>)
#TODO: add support for named let
def check_let(expr):
    if len(expr) < 3:
        raise SchemeBadSyntaxError(expr, 'bad let syntax')
    if not isinstance(expr[1], list):
        raise SchemeBadSyntaxError(expr, 'bad let binding syntax')
    if [x for x in expr[1] if not isinstance(x, list) or len(x) != 2 or \
                              not is_identifier(x[0])] != []:
        raise SchemeBadSyntaxError(expr, 'bad let binding syntax')

def let_bindings(expr):
    return expr[1]

def let_body(expr):
    return expr[2:]

# let*
# syntax same as let
def letstar_to_lambda(expr):
    bindings = let_bindings(expr)
    if bindings == []:
        return [make_lambda([], let_body(expr))]

    # construct the inner-most lambda body
    body = [make_lambda([bindings[-1][0]], let_body(expr)), bindings[-1][1]]
    for b in bindings[:-1][::-1]:
        body = [make_lambda([b[0]], [body]), b[1]]
    return body

# letrec
# syntax same as let
def letrec_to_lambda(expr):
    bindings = let_bindings(expr)
    if bindings == []:
        return [make_lambda([], let_body(expr))]

    args = [b[0] for b in bindings]
    set_exprs = [['set!'] + b for b in bindings]
    return [make_lambda(args, set_exprs + let_body(expr))] + \
           [['quote', '*unassigned*']] * len(bindings)

# and/or
# (and <expr1> <expr2> <expr3>)
# (or <expr1> <expr2> <expr3>)
def and_or_exprs(expr):
    return expr[1:]

# apply
# (apply proc '(arg1 arg2 arg3))
def check_apply(expr):
    if len(expr) != 3:
        raise SchemeBadSyntaxError(expr, 'bad apply syntax')

def apply_proc(expr):
    return expr[1]

def apply_args(expr):
    return expr[2]

# application
# (proc arg1 arg2 arg3)
def call_proc(expr):
    return expr[0]

def call_args(expr):
    return expr[1:]
