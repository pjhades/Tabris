# -*- coding: utf-8 -*-

"""
    Analyzer that checks if the forms are valid according to 
    Scheme's syntax rules and the evalution funtions.
"""

import trampoline

from number import is_number
from enviro import extend_env
from pair import *
from typedef import *
from errors import *

def is_tagged_list(exp, tag):
    return is_list(exp) and car(exp) == tag


def is_self_evaluating(exp):
    return is_number(exp) or is_boolean(exp) or is_string(exp)

def analyze_self_evaluating(exp):
    def f(env):
        return trampoline.fall(exp)
    return trampoline.fall(f)


def is_variable(exp):
    return is_symbol(exp)

def analyze_variable(exp):
    def f(env):
        return trampoline.fall(env.get_var(exp))

    return trampoline.fall(f)


def is_quote(exp):
    return is_tagged_list(exp, Symbol('quote'))

def get_quote_text(exp):
    return cadr(exp)

def analyze_quote(exp):
    def f(env):
        return trampoline.fall(get_quote_text(exp))

    if get_length(exp) != 2:
        raise SchemeError('bad syntax: ' + to_str(exp))
    return trampoline.fall(f)


def is_assignment(exp):
    return is_tagged_list(exp, Symbol('set!'))

def get_assignment_var(exp):
    return cadr(exp)

def get_assignment_val(exp):
    return caddr(exp)

def analyze_assignment(exp):
    def f(env):
        env.set_var(var, trampoline.pogo_stick(val(env)))
        return trampoline.fall(Symbol('ok'))

    if get_length(exp) != 3:
        raise SchemeError('bad syntax: ' + to_str(exp))

    var, val = get_assignment_var(exp), analyze(get_assignment_val(exp))
    return trampoline.fall(f)


def is_definition(exp):
    return is_tagged_list(exp, Symbol('define'))

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

def analyze_definition(exp):
    def f(env):
        env.add_var(var, trampoline.pogo_stick(val(env)))
        return trampoline.fall(Symbol('ok'))

    if get_length(exp) < 3:
        raise SchemeError('bad syntax: ' + to_str(exp))

    var, val = get_define_var(exp), analyze(get_define_val(exp))
    return trampoline.fall(f)


def is_lambda(exp):
    return is_tagged_list(exp, Symbol('lambda'))

def get_lambda_params(exp):
    return cadr(exp)

def get_lambda_body(exp):
    return cddr(exp)

def make_lambda(params, body):
    return cons(Symbol('lambda'), cons(params, body))

def analyze_lambda(exp):
    def f(env):
        nonlocal params
        if is_list(params):
            params = to_python_list(params)
        return trampoline.fall(Procedure(params, body, env))

    params, body = get_lambda_params(exp), \
                   trampoline.pogo_stick(analyze_sequence(get_lambda_body(exp)))
    return trampoline.fall(f)


def is_if(exp):
    return is_tagged_list(exp, Symbol('if'))

def get_if_predicate(exp):
    return cadr(exp)

def get_if_consequent(exp):
    return caddr(exp)

def get_if_alternative(exp):
    x = cdddr(exp)
    if not is_null(x):
        return car(x)
    return Boolean(False)

def make_if(predicate, consequent, alternative):
    return make_list(Symbol('if'), predicate, consequent, alternative)

def analyze_if(exp):
    predi, conse, alter = analyze(get_if_predicate(exp)), \
                          analyze(get_if_consequent(exp)), \
                          analyze(get_if_alternative(exp))

    def f(env):
        if is_true(trampoline.pogo_stick(predi(env))):
            return trampoline.pogo_stick(conse(env))
        else:
            return trampoline.pogo_stick(alter(env))

    return trampoline.fall(f)


def is_begin(exp):
    return is_tagged_list(exp, Symbol('begin'))

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

def analyze_sequence(exps):
    exp_list = [analyze(x) for x in to_python_list(exps)]

    def f(env):
        for exp in exp_list[:-1]:
            trampoline.pogo_stick(exp(env))
        return exp_list[-1](env)

    return trampoline.fall(f)


def is_application(exp):
    return is_pair(exp)

def get_application_opr(exp):
    return car(exp)

def get_application_opd(exp):
    return cdr(exp)

def analyze_application(exp):
    def f(env):
        nonlocal func, args
        proc = trampoline.pogo_stick(func(env))
        arg_list = [trampoline.pogo_stick(arg(env)) for arg in args]

        if not isinstance(proc, Procedure):
            raise SchemeError('no procedure to apply: ' + to_str(exp))

        if proc.is_prim:
            # TODO: add prim procedures to the initial env
            return apply_prim(proc, arg_list)
        else:
            # 检查是否是代表列表的单个参数，扩展环境
            if proc.is_var_args:
                var_list = [proc.params]
                val_list = make_list(arg_list)
            else:
                var_list = proc.params
                val_list = arg_list

            new_env = extend_env(var_list, val_list, env)
            return proc.body(new_env)

    func, args = analyze(get_application_opr(exp)), \
                 [analyze(x) for x in to_python_list(get_application_opd(exp))]
    return trampoline.fall(f)


def is_cond(exp):
    return is_tagged_list(exp, Symbol('cond'))

def get_cond_clauses(exp):
    return cdr(exp)

def get_cond_predicate(clause):
    return car(clause)

def get_cond_action(clause):
    return cdr(clause)

def is_cond_else(clause):
    return get_cond_predicate(clause) == Symbol('else')

def cond_to_if(exp):
    return expand_clauses(get_cond_clauses(exp))

def expand_clauses(clauses):
    cls = list(reversed(to_python_list(clauses)))

    if is_cond_else(cls[0]):
        alter = seq_to_exp(get_cond_action(cls[0]))
        start = 1
    else:
        alter = Boolean(False)
        start = 0

    for c in cls[start:]:
        alter = make_if(get_cond_predicate(c), seq_to_exp(get_cond_action(c)), alter)

    return alter


def is_let(exp):
    return is_tagged_list(exp, Symbol('let'))

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


def analyze_exp(exp):
    #TODO: unit test to be added
    if is_self_evaluating(exp):
        return trampoline.bounce(analyze_self_evaluating, exp)
    elif is_quote(exp):
        return trampoline.bounce(analyze_quote, exp)
    elif is_variable(exp):
        return trampoline.bounce(analyze_variable, exp)
    elif is_assignment(exp):
        return trampoline.bounce(analyze_assignment, exp)
    elif is_definition(exp):
        return trampoline.bounce(analyze_definition, exp)
    elif is_lambda(exp):
        return trampoline.bounce(analyze_lambda, exp)
    #elif is_if(exp):
    #    return trampoline.bounce(analyze_if, exp)
    #elif is_begin(exp):
    #    return trampoline.bounce(analyze_sequence, get_begin_actions(exp))
    #elif is_cond(exp):
    #    return trampoline.bounce(analyze_exp, cond_to_if(exp))
    elif is_application(exp):
        return trampoline.bounce(analyze_application, exp)
    else:
        raise SchemeError('unknown expression: ' + to_str(exp))

def analyze(exp):
    return trampoline.pogo_stick(analyze_exp(exp))

python_eval = eval

def eval(exp, env):
    # TODO (define foo (lambda x x)) (foo 1 2 3) 返回的是list，不是List
    # 测sequence的执行、函数定义、不定参数和定参数的函数定义
    #trampoline.pogo_stick(analyze(exp)(env))
    #return result
    return trampoline.pogo_stick(analyze(exp)(env))
