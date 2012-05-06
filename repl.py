# -*- coding: utf-8 -*-

import vm
from pair import to_str
from prims import prim_mappings
from parser import Tokenizer, parse
from compiler import tcompile
from environment import Frame
from errors import *

class Repl(object):
    def __init__(self, infile=''):
        self.ps1 = "Tabris >>> "
        self.ps2 = "       ... "
        self.tker = Tokenizer()
        self.env = Frame(prim_mappings.keys(), [None]*len(prim_mappings.keys()), None)
        self.vm = vm.VM()
        try:
            self.infile = '' if infile == '' else open(infile, 'r')
        except IOError:
            raise SchemeError('cannot open source file: ' + infile)

    # TODO: capture C-c C-\ signals, add (exit) to exit
    def loop(self):
        reach_eof = False
        while not reach_eof:
            if self.infile == '':
                self.tker.tokenize(input(self.ps1) + '\n')
            else:
                self.tker.tokenize(self.infile.readline())

            while self.tker.need_more_code():
                if self.infile == '':
                    self.tker.tokenize(input(self.ps2) + '\n')
                else:
                    line = self.infile.readline()
                    if line == '':
                        reach_eof = True
                        break
                    self.tker.tokenize(line)

            tokens = self.tker.get_tokens()
            exps = parse(tokens)

            #self.vm.set_dbgflag(vm.DBG_STEPDUMP | vm.DBG_SHOWINST)
            #self.vm.set_dbgflag(vm.DBG_SHOWCODE)

            for exp in exps:
                codes = tcompile(exp, self.env)
                self.vm.load(codes)
                self.vm.run()
                #print(self.vm.regs[vm.REG_ENV].binds)
                print(self.vm.result)
        
        self.infile.close()
