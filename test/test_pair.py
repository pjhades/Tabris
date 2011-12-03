#!/usr/bin/env python
# -*- codint: utf-8 -*-

if __name__ == '__main__':
    import sys
    sys.path.append('../')
    from syntax import parse
    from tokens import Tokenizer
    from utils import get_clean_code
    from evalscm import eval

    testcase = {
        "'((a . b) e (quote x) quote '(x . y))" : "'((a . b) e 'x quote '(x . y))",
        "'(a . b)"                              : "'(a . b)",
        "'(a b c)"                              : "'(a b c)",
        "'()"                                   : "'()",
        "'(a)"                                  : "'(a)",
        "'(1 2 3 . (4 . 5))"                    : "'(1 2 3 4 . 5)",
        "'''x"                                  : "'''x",
        "'(quote (quote x) x . (quote y))"      : "'(quote 'x x quote y)"
    }

    for line in testcase:
        t = Tokenizer(line + '\n')
        t.tokenize()
        s1 = eval(parse(t.token_list)[0], '')
        t.expr = testcase[line]
        t.tokenize()
        s2 = get_clean_code(parse(t.token_list)[0])
        print('  case:', s2)
        print('result:', s1)
        assert(str(s1) == s2)
        print()
