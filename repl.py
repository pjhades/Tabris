# -*- coding: utf-8 -*-
"""
    Read-Evaluate-Print Loop
"""

import parser
import evalu
import enviro

from errors import *
from pair import to_str

class Repl:
    def __init__(self):
        self.tokenizer = parser.Tokenizer()
        self.env = enviro.init_global()
        self.ps1 = "秋裤党 >>> "
        self.ps2 = "       ... "

    # TODO: capture C-c C-\ signals, add (exit) to exit
    def loop(self):
        while True:
            self.tokenizer.tokenize(input(self.ps1) + '\n')

            while self.tokenizer.need_more_code():
                self.tokenizer.tokenize(input(self.ps2) + '\n')

            tokens = self.tokenizer.get_tokens()
            print('tokens:')
            print('-' * 50)
            for token in tokens:
                print(token)
            print()

            print('env:')
            print('-' * 50)
            for var in self.env.bindings:
                print(var, type(var), '--->', self.env.bindings[var], type(self.env.bindings[var]))
            print()

            exps = parser.parse(tokens)

            for exp in exps:
                print('str form:')
                print('-' * 50)
                print(to_str(exp))
                print()
                print('result ---_')
                print('           \\')
                print('            V')
                print(evalu.eval(exp, self.env))
                print()
