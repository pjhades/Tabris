# -*- coding: utf-8 -*-

import vm
from pair import to_str
from prims import prim_mappings
from parser import Tokenizer, parse
from compiler import tcompile
from environment import Frame
from errors import *

# TODO: capture C-c C-\ signals, add (exit) to exit

PS1 = 'Tabris >>> '
PS2 = '       ... '

class Repl(object):
    def __init__(self, filename=None):
        self.ps = PS1
        self.tker = Tokenizer()
        self.env = Frame(prim_mappings.keys(), 
                         [None]*len(prim_mappings.keys()), 
                         None)
        self.vm = vm.VM()
        try:
            if filename is None:
                self.infile = None
            else:
                self.infile = open(filename, 'r')
        except IOError:
            raise SchemeError('cannot open source file: ' + infile)

    def loop_stdin(self):
        while True:
            try:
                while self.tker.need_more_code():
                    self.tker.tokenize(input(self.ps) + '\n')
                    self.ps = PS2
            except SchemeError as e:
                print(e)
                self.ps = PS2
                if self.tker.need_more_code():
                    continue

            try:
                tokens = self.tker.get_tokens()
                exps = parse(tokens)
                for exp in exps:
                    codes = tcompile(exp, self.env)
                    self.vm.run(codes)
                    if self.vm.result is not None:
                        print(self.vm.result)
            except SchemeError as e:
                print(e)

            self.ps = PS1

    def loop_file(self):
        reach_eof = False
        while not reach_eof:
            try:
                while self.tker.need_more_code():
                    line = self.infile.readline()
                    if line == '':
                        reach_eof = True
                        break
                    self.tker.tokenize(line)
                
                tokens = self.tker.get_tokens()
                exps = parse(tokens)
                for exp in exps:
                    codes = tcompile(exp, self.env)
                    self.vm.run(codes)
                    if self.vm.result is not None:
                        print(self.vm.result)
            except SchemeError as e:
                print(e)
                break
        self.infile.close()

    def loop(self):
        if self.infile is None:
            self.loop_stdin()
        else:
            self.loop_file()

