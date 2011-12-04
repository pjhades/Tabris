#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import sys
    sys.path.append('../')
    from tokens import Tokenizer
    from syntax import parse
    from evalscm import eval
    from env import init_env, global_env

    code = ["(define a 5)", \
            "(define (addx x) (lambda (n) (+ n x)))", \
            "(define func (addx 10))", \
            "func", \
            "(func 101)", \
            "((addx 1) 99)"]

    init_env()
    for c in code:
        print(' in: ', c)
        t = Tokenizer(c + '\n')
        t.tokenize()
        print('out:', eval(parse(t.token_list)[0], global_env))

        print('-' * 50)
