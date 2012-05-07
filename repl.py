# -*- coding: utf-8 -*-

import vm
from pair import to_str
from prims import prim_mappings
from parser import Tokenizer, parse
from compiler import tcompile
from environment import Frame
from errors import *

# TODO: capture C-c C-\ signals, add (exit) to exit

class Repl(object):
    def __init__(self, filename=None):
        self.ps1 = 'Tabris >>> '
        self.ps2 = '       ... '
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
                self.tker.tokenize(input(self.ps1) + '\n')
                while self.tker.need_more_code():
                    self.tker.tokenize(input(self.ps2) + '\n')

                tokens = self.tker.get_tokens()
                exps = parse(tokens)

                for exp in exps:
                    codes = tcompile(exp, self.env)
                    self.vm.load(codes)
                    self.vm.run()
                    print(self.vm.result)
            except SchemeError as e:
                print(e)

    def loop_file(self):
        reach_eof = False
        while not reach_eof:
            line = self.infile.readline()
            self.tker.tokenize(line + '\n')
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
                self.vm.load(codes)
                self.vm.run()
                print(self.vm.result)

        self.infile.close()


    def loop(self):
        if self.infile is None:
            self.loop_stdin()
        else:
            self.loop_file()

