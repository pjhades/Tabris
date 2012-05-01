# -*- coding: utf-8 -*-

from scmtypes import Symbol

REG_PC = 0
REG_VAL = 1
REG_ENV = 2
REG_FLAG = 3


def inst_loadi(vm, idx, val):
    """Load an immediate to register."""
    vm.regs[idx] = val


def inst_refvar(vm, var):
    """Reference a variable."""
    val = vm.regs[REG_ENV].refvar(var)
    vm.regs[REG_VAL] = val


def inst_bindvar(vm, var):
    """Add a new binding of variable and the value in VAL"""
    val = vm.regs[REG_VAL]
    vm.regs[REG_ENV].bindvar(var, val)
    vm.regs[REG_VAL] = Symbol('ok')


def inst_setvar(vm, var):
    """Set a variable to the value in VAL register"""
    val = vm.regs[REG_VAL]
    vm.regs[REG_ENV].setvar(var, val)
    vm.regs[REG_VAL] = Symbol('ok')


class VM(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.regs = [0]*4
        self.code = []
        self.codelen = 0
        self.stack = []
        self.lables = {}


def main():
    vm = VM()


if __name__ == '__main__':
    main()
