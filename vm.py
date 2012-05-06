# -*- coding: utf-8 -*-

from scmtypes import Symbol
from environment import init_global
from insts import REG_PC, REG_VAL, REG_ENV, REG_ARGS

DBG_SHOWINST = 1
DBG_STEPDUMP = 2
DBG_SHOWCODE = 4

class VM(object):
    def __init__(self):
        self.reset()
        self.flags = 0

    def reset(self):
        self.regs = [0] * 4
        self.regs[REG_VAL] = 0
        self.regs[REG_PC] = 0
        self.regs[REG_ENV] = init_global()
        self.regs[REG_ARGS] = []
        self.code = []
        self.stack = []

    def load(self, code):
        self.code += code
        if self.flags & DBG_SHOWCODE:
            for c in self.code:
                print(c)

        #for i in range(len(code)):
        #    if isinstance(code[i], tuple):
        #        self.code.append(code[i])
        #    else:
        #        self.labels[code[i]] = len(self.code)
        #if self.flags & DBG_SHOWCODE:
        #    print('code:')
        #    for c in self.code:
        #        print(c)
        #    print('labels:')
        #    for l in self.labels:
        #        p = self.labels[l]
        #        if p < len(self.code):
        #            print('%s: %d %s' % (l, self.labels[l], self.code[self.labels[l]]))
        #        else:
        #            print('%s: %d %s' % (l, self.labels[l], '---'))

    def run(self):
        while self.regs[REG_PC] != len(self.code):
            inst = self.code[self.regs[REG_PC]]
            if self.flags & DBG_SHOWINST:
                print('exec:', inst)
                p = self.regs[REG_PC]
                if p+1 < len(self.code):
                    print('next:', self.code[p+1])
                else:
                    print('next:', '---')
            inst[0](self, *inst[1:])
            if self.flags & DBG_STEPDUMP:
                self.dump()
                input('press enter to continue ...') 

    @property
    def result(self):
        return self.regs[REG_VAL]

    def set_dbgflag(self, flags=0):
        self.flags = flags

    def dump(self):
        print('<PC>', self.regs[REG_PC], end='     ')
        print('<VAL>', self.regs[REG_VAL], end='     ')
        print('<ARGS>', self.regs[REG_ARGS])
        print('<ENV>')
        if self.regs[REG_ENV].outer is None:
            print('global environment')
        else:
            for sym in self.regs[REG_ENV].binds:
                print(sym, '=>', self.regs[REG_ENV].binds[sym])
        print('<STACK>')
        print(self.stack)
        print()
