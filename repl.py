# -*- coding: utf-8 -*-

"""Read-Evaluate-Print Loop"""

import profile

import parser
import evalu
import environment
from errors import *
from pair import to_str
from compiler import tcompile

class Repl(object):
    def __init__(self, infile=''):
        #self.ps1 = "秋裤党你要努力，不然会被看不起 >>> "
        self.ps1 = "第三次冲击 >>> "
        self.ps2 = "       ... "
        self.tokenizer = parser.Tokenizer()
        self.env = environment.init_global()
        try:
            self.infile = '' if infile == '' else open(infile, 'r')
        except IOError:
            raise SchemeError('cannot open source file: ' + infile)

    # TODO: capture C-c C-\ signals, add (exit) to exit
    def loop(self):
        reach_eof = False
        while not reach_eof:
            if self.infile == '':
                self.tokenizer.tokenize(input(self.ps1) + '\n')
            else:
                self.tokenizer.tokenize(self.infile.readline())

            while self.tokenizer.need_more_code():
                if self.infile == '':
                    self.tokenizer.tokenize(input(self.ps2) + '\n')
                else:
                    line = self.infile.readline()
                    if line == '':
                        reach_eof = True
                        break
                    self.tokenizer.tokenize(line)

            tokens = self.tokenizer.get_tokens()

            #print('tokens:')
            #print('-' * 50)
            #for token in tokens:
            #    print(token)
            #print()

            #print('env:')
            #print('-' * 50)
            #for var in self.env.bindings:
            #    print(var, type(var), '--->', self.env.bindings[var], type(self.env.bindings[var]))
            #print()

            exps = parser.parse(tokens)

            for exp in exps:
                #print('str form:')
                #print('-' * 50)
                #print(to_str(exp))
                #print()
                #print('result ---_')
                #print('           \\')
                #print('            V')

                codes = tcompile(exp, self.env)
                for code in codes:
                    print(code)

                #print(evalu.eval(exp, self.env))
                #print()
        
        self.infile.close()
