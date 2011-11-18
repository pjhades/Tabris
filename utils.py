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

    # add ' or ( for quote or list
    s = '\'' if expr[0] == 'quote\'' else '('
    # omit the first one for quote
    seq = expr[1:] if expr[0] == 'quote\'' else expr
    for exp in seq:
        if isinstance(exp, list):
            if exp != [] and exp[0] == 'quote\'':
                s += ('\'' if s == '' or s[-1] in '(\'' else ' \'') + get_clean_code(exp[1])
            else:
                s += ('' if s == '' or s[-1] in '(\'' else ' ') + get_clean_code(exp)
        else:
            s += exp if s == '' or s[-1] in '(\'' else ' ' + exp
    return s + ('' if expr[0] == 'quote\'' else ')')

