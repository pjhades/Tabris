#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import repl
# TODO: rewrite the file interface

if __name__ == '__main__':
    evaluator = repl.Repl()
    evaluator.loop()
    #evaluator = repl.Repl(sys.argv[1])
    #evaluator.loop()
