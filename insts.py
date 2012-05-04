# -*- coding: utf-8 -*-

REG_PC = 0
REG_VAL = 1
REG_ENV = 2
REG_SP = 3


def inst_loadi(vm, idx, val):
    """Load an immediate to register."""
    vm.regs[idx] = val
    vm.regs[REG_PC] += 1


def inst_refvar(vm, var):
    """Reference a variable."""
    val = vm.regs[REG_ENV].refvar(var)
    vm.regs[REG_VAL] = val
    vm.regs[REG_PC] += 1


def inst_bindvar(vm, var):
    """Add a new binding of variable and the value in VAL."""
    val = vm.regs[REG_VAL]
    vm.regs[REG_ENV].bindvar(var, val)
    vm.regs[REG_VAL] = Symbol('ok')
    vm.regs[REG_PC] += 1


def inst_setvar(vm, var):
    """Set a variable to the value in VAL register."""
    val = vm.regs[REG_VAL]
    vm.regs[REG_ENV].setvar(var, val)
    vm.regs[REG_VAL] = Symbol('ok')
    vm.regs[REG_PC] += 1


def inst_jt(vm, label):
    """Jump to label if VAL is true."""
    if vm.regs[REG_VAL] is not False:
        vm.regs[REG_PC] = vm.labels[label]
    else:
        vm.regs[REG_PC] += 1


def inst_jf(vm, label):
    """Jump to label if VAL is false."""
    if vm.regs[REG_VAL] is False:
        vm.regs[REG_PC] = vm.labels[label]
    else:
        vm.regs[REG_PC] += 1


def inst_j(vm, label):
    """Unconditional jump."""
    vm.regs[REG_PC] = vm.labels[label]


def inst_extenv(vm):
    """Create a new empty frame."""
    frm = Frame(outer=vm.regs[REG_ENV])
    vm.regs[REG_ENV] = frm
    vm.regs[REG_PC] += 1


def inst_killenv(vm):
    """Kill the current frame and get to its parent."""
    vm.regs[REG_ENV] = vm.regs[REG_ENV].outer
    vm.regs[REG_PC] += 1


def inst_pushr(vm, idx):
    """Push reg `idx' onto the stack."""
    vm.regs[REG_SP] += 1
    vm.stack[vm.regs[REG_SP]] = vm.regs[idx]
    vm.regs[REG_PC] += 1


def inst_pushi(vm, val):
    """Push an immediate onto the stack."""
    vm.regs[REG_SP] += 1
    vm.stack[vm.regs[REG_SP]] = val
    vm.regs[REG_PC] += 1


def inst_pop(vm, idx):
    """Pop a value, save it in register `idx'."""
    vm.regs[idx] = vm.stack[REG_SP]
    vm.regs[REG_SP] -= 1
    vm.regs[REG_PC] += 1

