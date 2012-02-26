# -*- coding: utf-8 -*-

from errors import *
from pair import *
from pair_lib import *
from enviro import extend_env
from prims import prim_ops
from trampoline import pogo_stick, Bounce
from basic_type import Boolean, Symbol, Procedure, is_true, \
                       is_boolean, is_string, is_symbol
from number_type import is_number

# save the original versions
python_eval = eval
python_apply = apply

def is_self_evaluating(exp):
    return is_number(exp) or is_boolean(exp) or is_string(exp)

def eval_self_evaluating(exp, env, cont):
    return Bounce(cont, exp)

def is_variable(exp):
    return is_symbol(exp)

def eval_variable(exp, env, cont):
    return Bounce(cont, env.get_var(exp))

def get_quote_text(exp):
    return cadr(exp)

def eval_quote(exp, env, cont):
    print 'exp is:', exp
    print 'length is:', get_length(exp)
    if get_length(exp) != 2:
        raise SchemeError('bad syntax: ' + to_str(exp))
    return Bounce(cont, get_quote_text(exp))

def get_set_var(exp):
    return cadr(exp)

def get_set_val(exp):
    return caddr(exp)

def eval_set(exp, env, cont):
    def done_value(value):
        env.set_var(get_set_var(exp), value)
        return Bounce(cont, Symbol('ok'))

    if get_length(exp) != 3:
        raise SchemeError('bad syntax: ' + to_str(exp))

    val = get_set_val(exp)
    # evaluate the value expression first, and set
    # the variable to that value
    return Bounce(_eval, val, env, done_value)

def get_define_var(exp):
    x = cadr(exp)
    if is_symbol(x):
        return x
    return car(x)

def get_define_val(exp):
    x = cadr(exp)
    if is_symbol(x):
        return caddr(exp)
    return make_lambda(cdadr(exp), cddr(exp))

def eval_define(exp, env, cont):
    def done_value(value):
        env.add_var(get_define_var(exp), value)
        return Bounce(cont, Symbol('ok'))

    if get_length(exp) < 3:
        raise SchemeError('bad syntax: ' + to_str(exp))

    val = get_define_val(exp)
    # evaluate the value or lambda expression first, and
    # add a new variable in the environment
    return Bounce(_eval, val, env, done_value)

def get_lambda_params(exp):
    return cadr(exp)

def get_lambda_body(exp):
    return cddr(exp)

def make_lambda(params, body):
    return cons(Symbol('lambda'), cons(params, body))

def eval_lambda(exp, env, cont):
    body = get_lambda_body(exp)
    params = get_lambda_params(exp)

    if is_list(params):
        params = to_python_list(params)

    return Bounce(cont, Procedure(params, body, env))

def get_if_predicate(exp):
    return cadr(exp)

def get_if_consequent(exp):
    return caddr(exp)

def get_if_alternate(exp):
    x = cdddr(exp)
    if not is_null(x):
        return car(x)
    return Boolean(False)

def make_if(predicate, consequent, alternative):
    return make_list(Symbol('if'), predicate, consequent, alternative)

def eval_if(exp, env, cont):
    def take_action(pred):
        if is_true(pred):
            return Bounce(_eval, get_if_consequent(exp), env, cont)
        else:
            return Bounce(_eval, get_if_alternate(exp), env, cont)
    return Bounce(_eval, get_if_predicate(exp), env, take_action)

def get_begin_actions(exp):
    return cdr(exp)

def seq_to_exp(seq):
    if is_null(seq):
        return seq
    elif is_null(cdr(seq)):
        return car(seq)
    else:
        return make_begin(seq)

def make_begin(seq):
    return cons(Symbol('begin'), seq)

def eval_sequence(exps, env, cont):
    "evaluate the sequence, return only the last as final result"
    def done_first(first):
        return Bounce(eval_sequence, cdr(exps), env, cont)
    if is_null(cdr(exps)):
        return Bounce(_eval, car(exps), env, cont)
    return Bounce(_eval, car(exps), env, done_first)

def eval_begin(exp, env, cont):
    return Bounce(eval_sequence, cdr(exp), env, cont)

def is_application(exp):
    return is_pair(exp)

def get_application_opr(exp):
    return car(exp)

def get_application_opd(exp):
    return cdr(exp)

def eval_each(opds, env, cont):
    """
    evaluate each operand in the Scheme list, make
    a new Scheme list.
    """
    def done_first(first):
        def have_rest(rest):
            return Bounce(cont, cons(first, rest))
        return Bounce(eval_each, cdr(opds), env, have_rest)
    
    if is_null(opds):
        return Bounce(cont, NIL)
    return Bounce(_eval, car(opds), env, done_first)

def eval_application(exp, env, cont):
    def done_opr(opr):
        def done_opds(opd):
            return Bounce(apply, opr, opd, cont)

        if not isinstance(opr, Procedure):
            raise SchemeError('not applicable: ' + to_str(exp))
        opds = get_application_opd(exp)
        return Bounce(eval_each, opds, env, done_opds)

    opr = get_application_opr(exp)
    # evaluate the operator first
    return Bounce(_eval, opr, env, done_opr)

def get_cond_clauses(exp):
    return cdr(exp)

def get_cond_predicate(clause):
    return car(clause)

def get_cond_action(clause):
    return cdr(clause)

def eval_cond(exp, env, cont):
    return Bounce(eval_if, expand_clauses(get_cond_clauses(exp)), env, cont)

def expand_clauses(clauses):
    cls = list(reversed(to_python_list(clauses)))

    if car(cls[0]) == Symbol('else'):
        alter = seq_to_exp(get_cond_action(cls[0]))
        start = 1
    else:
        alter = Boolean(False)
        start = 0

    for c in cls[start:]:
        alter = make_if(get_cond_predicate(c), seq_to_exp(get_cond_action(c)), alter)

    return alter

def get_let_bindings(exp):
    return cadr(exp)

def get_let_body(exp):
    return cddr(exp)

def get_binding_var_exp(bindings):
    "Return the variables and expressions in each binding."
    binding_list = to_python_list(bindings)
    return make_list(*[car(x) for x in binding_list]), \
           make_list(*[cadr(x) for x in binding_list])

def let_to_call(exp):
    var_list, exp_list = get_binding_var_exp(get_let_bindings(exp))
    return cons(make_lambda(var_list, get_let_body(exp)), exp_list)

special_form = {
    Symbol('quote'),
    Symbol('set!'),
    Symbol('define'),
    Symbol('lambda'),
    Symbol('if'),
    Symbol('begin'),
    Symbol('cond'),
}

act = {
    Symbol('quote'): eval_quote,
    Symbol('set!'): eval_set,
    Symbol('define'): eval_define,
    Symbol('lambda'): eval_lambda,
    Symbol('if'): eval_if,
    Symbol('begin'): eval_begin,
    Symbol('cond'): eval_cond,
}

def _eval(exp, env, cont):
    if is_list(exp):
        if car(exp) in special_form:
            return Bounce(act[car(exp)], exp, env, cont)
        elif is_pair(exp):
            return Bounce(eval_application, exp, env, cont)
    else:
        if is_symbol(exp):
            return Bounce(cont, env.get_var(exp))
        elif is_number(exp) or is_boolean(exp) or is_string(exp):
            return Bounce(cont, exp)
        else:
            raise SchemeError('unknown expression: ' + to_str(exp))

def apply_prim(prim_type, args, cont):
    return Bounce(cont, prim_ops[prim_type](*args))

def eval(exp, env):
    return pogo_stick(Bounce(_eval, exp, env, lambda d:d))

def apply(proc, args, cont):
    """apply `proc' on scheme list `args'"""
    if proc.is_prim:
        return Bounce(apply_prim, proc.body, to_python_list(args), cont)
    else:
        # if `proc' accepts arbitrary arguments, `proc.params' is a single
        # variable, put it into a python list, `args' remains a scheme list
        if proc.is_var_args:
            params = [proc.params]
            args = to_python_list(make_list(args))
        else:
            params = proc.params
            args = to_python_list(args)

        if len(proc.params) != len(args):
            raise SchemeError('expects %d arguments, given %d: %s' % \
                              (len(proc.params), len(args), ' '.join([str(x) for x in args])))

        new_env = extend_env(params, args, proc.env)
        body = proc.body
        return Bounce(eval_sequence, body, new_env, cont)
