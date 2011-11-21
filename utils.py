# -*- coding: utf-8 -*-

def get_clean_code(expr):
    """
        Return a string representation of the original code from 
        the syntax tree, removing useless whitespaces.

        @param expr: list represented syntax tree
        @return: single-line code string
    """
    if not isinstance(expr, list):
        return expr

    if expr == []:
        return '()'

    if expr[0] == 'quote' or expr[0] == 'quote\'':
        return '\'' + get_clean_code(expr[1])

    s = '(' + get_clean_code(expr[0])
    for exp in expr[1:]:
        s += ' ' + get_clean_code(exp)
    s += ')'

    return s

