#!/usr/bin/env python
# -*- codint: utf-8 -*-

if __name__ == '__main__':
    import sys
    sys.path.append('../')
    from syntax import parse
    from tokens import Tokenizer
    from utils import get_clean_code

    testcase = {"x"                             : "x",
                "'()"                           : "'()",
                "'x"					        : "'x",
                "''x"					        : "''x",
                "'''x"					        : "'''x",
                "(quote (quote x))"			    : "''x",
                "'(quote ''x)"					: "''''x",
                "'(quote (quote x) 'x)"		    : "'(quote 'x 'x)",
                "'(a . b)"					    : "'(a . b)",
                "'(a . (b . c))"				: "'(a b . c)",
                "'(a b c . d)"					: "'(a b c . d)",
                "'(a (b . (c . d)) x . y)"		: "'(a (b c . d) x . y)"
               }

    for line in testcase:
        t = Tokenizer(line + '\n')
        t.tokenize()
        s = get_clean_code(parse(t.token_list)[0])
        print('  case:', line)
        print('result:', s)
        assert(s == testcase[line])
        print()
