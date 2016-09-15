#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import repl

if __name__ == '__main__':
    if len(sys.argv) == 1:
        evaluator = repl.Repl()
    elif len(sys.argv) == 2:
        evaluator = repl.Repl(sys.argv[1])

    import profile
    import pstats

#    profile.run('evaluator.loop()', 'profile.dat')
#    p = pstats.Stats('profile.dat')
#    p.strip_dirs().sort_stats('time', 'cum').print_stats()
    evaluator.loop()
