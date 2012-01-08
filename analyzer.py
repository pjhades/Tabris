# -*- coding: utf-8 -*-

"""
    Implementation of the analyzer that checks if
    the forms are valid according to Scheme's syntax
    rules.
"""

import number
import typedef
import pair

from errors import *

def is_tagged_list(exp, tag):
    return pair.is_list(exp) and pair.car(exp) == tag


# self-evaluting
def is_self_evaluating(exp):
    return number.is_number(exp) or typedef.is_boolean(exp) or typedef.is_string(exp)


# variable
def is_variable(exp):
    return typedef.is_symbol(exp)


# quotation
def is_quote(exp):
    return is_tagged_list(exp, typedef.Symbol('quote'))

def get_quote_text(exp):
    return pair.cadr(exp)


# assignment
def is_assignment(exp):
    return is_tagged_list(exp, typedef.Symbol('set!'))

def get_assignment_var(exp):
    return pair.cadr(exp)

def get_assignment_val(exp):
    return pair.caddr(exp)


# definition
def is_definition(exp):
    return is_tagged_list(exp, typedef.Symbol('define'))

def get_define_var(exp):
    x = pair.cadr(exp)
    if typedef.is_symbol(x):
        return x
    return pair.car(x)

def get_define_val(exp):
    x = pair.cadr(exp)
    if typedef.is_symbol(x):
        return pair.caddr(exp)
    return make_lambda(pair.cdadr(exp), pair.cddr(exp))


# lambda
def is_lambda(exp):
    return is_tagged_list(exp, typedef.Symbol('lambda'))

def get_lambda_params(exp):
    return pair.cadr(exp)

def get_lambda_body(exp):
    return pair.cddr(exp)

def make_lambda(params, body):
    return pair.cons(typedef.Symbol('lambda'), pair.cons(params, body))


# if form
def is_if(exp):
    return is_tagged_list(exp, typedef.Symbol('if'))

def get_if_predicate(exp):
    return pair.cadr(exp)

def get_if_consequent(exp):
    return pair.caddr(exp)

def get_if_alternative(exp):
    x = pair.cdddr(exp)
    if not pair.is_null(x):
        return pair.car(x)
    return typedef.Boolean(False)

def make_if(predicate, consequent, alternative):
    return pair.make_list(typedef.Symbol('if'), predicate, consequent, alternative)


# begin form
def is_begin(exp):
    return is_tagged_list(exp, typedef.Symbol('begin'))

def get_begin_actions(exp):
    return pair.cdr(exp)

def seq_to_exp(seq):
    if pair.is_null(seq):
        return seq
    elif pair.is_null(pair.cdr(seq)):
        return pair.car(seq)
    else:
        return make_begin(seq)

def make_begin(seq):
    return pair.cons(typedef.Symbol('begin'), seq)


# application
def is_application(exp):
    return pair.is_pair(exp)

def get_application_opr(exp):
    return pair.car(exp)

def get_application_opd(exp):
    return pair.cdr(exp)


# cond
def is_cond(exp):
    return is_tagged_list(exp, typedef.Symbol('cond'))

def get_cond_clauses(exp):
    return pair.cdr(exp)

def get_cond_predicate(clause):
    return pair.car(clause)

def get_cond_action(clause):
    return pair.cdr(clause)

def is_cond_else(clause):
    return get_cond_predicate(clause) == typedef.Symbol('else')

def cond_to_if(exp):
    return expand_clauses(get_cond_clauses(exp))

def expand_clauses(clauses):
    cls = list(reversed(pair.to_python_list(clauses)))

    if is_cond_else(cls[0]):
        alter = seq_to_exp(get_cond_action(cls[0]))
        cls = cls[1:]
    else:
        alter = typedef.Boolean(False)

    for c in cls:
        alter = make_if(get_cond_predicate(c), seq_to_exp(get_cond_action(c)), alter)

    return alter


# let
def is_let(exp):
    return is_tagged_list(exp, typedef.Symbol('let'))

def get_let_bindings(exp):
    return pair.cadr(exp)

def get_let_body(exp):
    return pair.cddr(exp)

def get_binding_var(b):
    return pair.car(b)

def get_binding_val(b):
    return pair.cadr(b)

def let_to_application(exp):
    """Convert a let form to application of a lambda."""
    bds = get_let_bindings(exp)
    var_lst = []
    val_lst = []

    while bds != pair.NIL:
        var_lst.append(get_binding_var(pair.car(bds)))
        val_lst.append(get_binding_val(pair.car(bds)))
        bds = pair.cdr(bds)

    lambda_exp = make_lambda(pair.make_list(*var_lst), get_let_body(exp))
    return pair.cons(lambda_exp, pair.make_list(*val_lst))

