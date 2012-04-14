# -*- coding: utf-8 -*-

from insts import *

class VM(object):
    def __init__(self):
        self.reset()
        #self.ops = insts_map
        self.funcs = funcs_map

    def reset(self):
        self.reg = [0] * NUM_REGS
        self.reg[REG_PC] = 0
        self.reg[REG_BP] = 0
        self.reg[REG_SP] = -1
        self.code = []
        self.codelen = 0
        self.data = []
        self.heap = []
        self.stack = []
        self.labels = {}
        self.flag = False

    def dump(self):
        for r in enumerate(self.reg[:-3]):
            print 'reg%2d: %d' % (r[0], r[1])
        print self.stack
        print 'BP:', self.reg[REG_BP]
        print 'SP:', self.reg[REG_SP]
        print 'PC:', self.code[self.reg[REG_PC]] \
                     if self.reg[REG_PC] < len(self.code) else ''

    def load(self, code):
        """Scan the instruction sequence, record all labels."""
        for line in code:
            if isinstance(line, tuple):
                self.code.append(line)
            else:
                self.labels[line] = len(self.code)
        self.codelen = len(self.code)

    def dispatch(self, inst):
        inst[0](self, inst)
        #self.ops[inst[0]](self, inst)

    def run(self):
        #while self.reg[REG_PC] < len(self.code):
        while self.reg[REG_PC] < self.codelen:
            inst = self.code[self.reg[REG_PC]]
            inst[0](self, inst)
            print 'executing:', inst
            self.dump()
            raw_input()
            #self.dispatch(self.code[self.reg[REG_PC]])


def main():
    vm = VM()

    fact_code = [
            (jmp_, 'main'),
        'fact',
            (push_, REG_BP),          
            (mov_, REG_BP, REG_SP),      
            (loadr_, 1, REG_BP, -2),  
            (movi_, 2, 1),         # if (n == 1)
            (test_, 'eq', 1, 2),   #     goto fact-done;
            (jt_, 'fact-done'),    
            (subi_, 3, 1, 1),      # int a = n-1;
            (push_, 1),
            (push_, 3),            
            (call_, 'fact'),       # int b = fact(a);
            (pop_, 1),
            (mul_, 0, 1, 0),       # b *= n;
            (mov_, REG_SP, REG_BP),      
            (pop_, REG_BP),           
            (ret_, 1),             # return b;
        'fact-done',
            (movi_, 0, 1),         # return 1;
            (mov_, REG_SP, REG_BP),      
            (pop_, REG_BP),           
            (ret_, 1),             
        'main',
            (pushi_, 10000),
            (call_, 'fact'),       # fact(5);
    ]

    fib_code = [
            (jmp_, 'main'),
        'fib',
            (push_, REG_BP),
            (mov_, REG_BP, REG_SP),
            (loadr_, 1, REG_BP, -2),
            (movi_, 2, 0),
            (test_, 'eq', 1, 2),
            (jt_, 'return-0'),
            (movi_, 2, 1),
            (test_, 'eq', 1, 2),
            (jt_, 'return-1'),
            (subi_, 3, 1, 1),
            (push_, 1),
            (push_, 3),
            (call_, 'fib'),
            (mov_, 4, 0),
            (pop_, 1),
            (subi_, 3, 1, 2),
            (push_, 3),
            (call_, 'fib'),
            (add_, 0, 4, 0),
            (mov_, REG_SP, REG_BP),
            (pop_, REG_BP),
            (ret_, 1),
        'return-0',
            (movi_, 0, 0),
            (mov_, REG_SP, REG_BP),
            (pop_, REG_BP),
            (ret_, 1),
        'return-1',
            (movi_, 0, 1),
            (mov_, REG_SP, REG_BP),
            (pop_, REG_BP),
            (ret_, 1),
        'main',
            (pushi_, 4),
            (call_, 'fib'),
    ]


    #vm.load(fact_code)
    vm.load(fib_code)
    vm.run()
    print vm.reg[0]


if __name__ == '__main__':
    import profile
    import pstats

    #profile.run('main()', 'profile.dat')
    #p = pstats.Stats('profile.dat')
    #p.strip_dirs().sort_stats('time', 'cum').print_stats()
    main()

