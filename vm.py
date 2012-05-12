# -*- coding: utf-8 -*-

from toplevel import init_global

# show each executing instruction
DBG_SHOWINST = 1
# stepping, pause after each instruction
DBG_STEPDUMP = 2
# show instruction sequence when loading code
DBG_SHOWCODE = 4

class VM(object):
    REG_PC = 0
    REG_VAL = 1
    REG_ENV = 2
    REG_ARGS = 3

    def __init__(self):
        self.reset()

    def reset(self):
        self.regs = [0] * 4
        self.regs[VM.REG_VAL] = 0
        self.regs[VM.REG_PC] = 0
        self.regs[VM.REG_ENV] = init_global()
        self.regs[VM.REG_ARGS] = []
        self.flags = 0
        self.code = []
        self.codelen = 0
        self.stack = []

    def run(self, code):
        self.code = code
        self.codelen = len(code)
        self.regs[VM.REG_PC] = 0

        if self.flags & DBG_SHOWCODE:
            for c in self.code:
                print(c)
            print()

        while self.regs[VM.REG_PC] < self.codelen:
            inst = self.code[self.regs[VM.REG_PC]]
            if self.flags & DBG_SHOWINST:
                print('exec:', inst)
                p = self.regs[VM.REG_PC]
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
        return self.regs[VM.REG_VAL]

    def set_dbgflag(self, flags=0):
        self.flags = flags

    def dump(self):
        print('<PC>', self.regs[VM.REG_PC], end='     ')
        print('<VAL>', self.regs[VM.REG_VAL], end='     ')
        print('<ARGS>', self.regs[VM.REG_ARGS])
        print('<ENV>')
        if self.regs[VM.REG_ENV].outer is None:
            print('global environment')
        else:
            for sym in self.regs[VM.REG_ENV].binds:
                print(sym, '=>', self.regs[VM.REG_ENV].binds[sym])
        print('<STACK>')
        print(self.stack)
        print()
