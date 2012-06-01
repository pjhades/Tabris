# -*- coding: utf-8 -*-

import vm
from tpair import to_str, from_python_list
from toplevel import top_bindings, init_compiletime_env
from parser import Tokenizer, Parser
from compiler import Compiler, define_dumb
from environment import Frame
from errors import *

# TODO: capture C-c C-\ signals, add (exit) to exit

PS1 = 'Tabris >>> '
PS2 = '       ... '

class Repl(object):
    def __init__(self, filename=None):
        self.ps = PS1
        self.toker = Tokenizer()
        self.parser = Parser()
        self.compiler = Compiler()
        self.vm = vm.VM()
        self.env = init_compiletime_env()
        if filename is None:
            self.infile = None
        else:
            self.infile = open(filename, 'r')

    def loop_stdin(self):
        #self.vm.set_dbgflag(vm.DBG_STEPDUMP | vm.DBG_SHOWCODE | vm.DBG_SHOWINST)
        while True:
            try:
                while self.toker.need_more_code():
                    self.toker.tokenize_piece(input(self.ps) + '\n')
                    self.ps = PS2
            except SchemeError as e:
                print(e)
                self.ps = PS2
                if self.toker.need_more_code():
                    continue

            try:
                tokens = self.toker.get_tokens()
                exps = self.parser.parse(tokens)
                for exp in exps:
                    codes = self.compiler.compile(exp, self.env)
                    self.vm.run(codes)
                    if self.vm.result is not None:
                        print(self.vm.result)
            except SchemeError as e:
                print(e)

            self.ps = PS1

    def loop_file(self):
        #self.vm.set_dbgflag(vm.DBG_SHOWINST | vm.DBG_STEPDUMP | vm.DBG_SHOWCODE)
        reach_eof = False
        exps = []
        while not reach_eof:
            try:
                while self.toker.need_more_code():
                    line = self.infile.readline()
                    if line == '':
                        reach_eof = True
                        break
                    self.toker.tokenize_piece(line)
                
                tokens = self.toker.get_tokens()
                exps.extend(self.parser.parse(tokens))
            except SchemeError as e:
                print(e)
                break

        try:
            code = define_dumb(exps, self.env)
            self.vm.run(code)
            for exp in exps:
                code = self.compiler.compile(exp, self.env)
                self.vm.run(code)
                if self.vm.result is not None:
                    print(self.vm.result)
        except SchemeError as e:
            print(e)
        
        self.infile.close()

    def loop(self):
        if self.infile is None:
            self.loop_stdin()
        else:
            self.loop_file()

    def runcode(self, code):
        try:
            exps = self.parser.parse(self.toker.tokenize(code))
            for exp in exps:
                codes = self.compiler.compile(exp, self.env)
                self.vm.run(codes)
                if self.vm.result is not None:
                    print(self.vm.result)
        except SchemeError as e:
            print(e)

