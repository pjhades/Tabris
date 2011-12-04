#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import sys
    sys.path.append('../')
    from tokens import Tokenizer
    from syntax import parse
    from evalscm import eval
    from env import init_env, global_env

    code = ["(define (even? x) (if (= x 0) #t (odd? (- x 1))))", \
            "(define (odd? x) (if (= x 0) #f (even? (- x 1))))", \
            "(even? 0)", \
            "(odd? 0)", \
            "(even? 100)", \
            "(odd? 300)", \
            "(even? 1000)"]

    init_env()
    for c in code:
        print(' in: ', c)
        t = Tokenizer(c + '\n')
        t.tokenize()
        print('out:', eval(parse(t.token_list)[0], global_env))

        print('-' * 50)
