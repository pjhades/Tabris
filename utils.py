# -*- coding: utf-8 -*-

def get_clean_code(expr, paren=True):
    """
        Return a string representation of the original code from 
        the syntax tree, removing useless whitespaces.
    """
    if not isinstance(expr, list):
        return expr

    if expr == []:
        return '()' if paren else ''

    if expr[0] == 'quote':
        if len(expr) == 2:
            return "'" + get_clean_code(expr[1])

    s = get_clean_code(expr[0])
    need_paren = True
    for i in range(1, len(expr)):
        if expr[i] == '.':
            if isinstance(expr[i + 1], list):
                # omit the dot and following parenthesis
                need_paren = False
            else:
                s += ' .'
                need_paren = True
        else:
            rest = get_clean_code(expr[i], need_paren)
            s += (' ' + rest) if rest != '' else ''
            #s += ' ' + get_clean_code(expr[i], need_paren)
            need_paren = True

    return '(' + s + ')' if paren else s
