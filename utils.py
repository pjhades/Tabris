# -*- coding: utf-8 -*-

def get_clean_code(expr):
    """
        Return a string representation of the original code from 
        the syntax tree, removing useless whitespaces.

        @param expr: syntax tree
        @return: single-line code string
    """
    if not isinstance(expr, list):
        return expr

    if expr == []:
        return '()'

    if expr[0] == 'quote' or expr[0] == '\'':
        if len(expr) == 2:
            return '\'' + get_clean_code(expr[1])

    s = '(' + get_clean_code(expr[0])
    for i in range(1, len(expr)):
        if i < len(expr) - 1 and expr[i] == '.' and isinstance(expr[i + 1], list):
            s += ' ' + get_clean_code(expr[i + 1])
        else:
            s += ' ' + get_clean_code(expr[i])
    s += ')'

    return s

