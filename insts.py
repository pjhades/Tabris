# -*- coding: utf-8 -*-

from scmtypes import ActivationRecord, Closure
from environment import Frame

REG_PC = 0
REG_VAL = 1
REG_ENV = 2
REG_ARGS = 3

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
    vm.regs[REG_PC] += 1


def inst_setvar(vm, var):
    """Set a variable to the value in VAL register."""
    val = vm.regs[REG_VAL]
    vm.regs[REG_ENV].setvar(var, val)
    vm.regs[REG_PC] += 1


def inst_jt(vm, offset):
    """Jump to label if VAL is true."""
    if vm.regs[REG_VAL] is not False:
        #vm.regs[REG_PC] = vm.labels[label]
        vm.regs[REG_PC] += offset
    else:
        vm.regs[REG_PC] += 1


def inst_jf(vm, offset):
    """Jump to label if VAL is false."""
    if vm.regs[REG_VAL] is False:
        #vm.regs[REG_PC] = vm.labels[label]
        vm.regs[REG_PC] += offset
    else:
        vm.regs[REG_PC] += 1


def inst_j(vm, offset):
    """Unconditional jump."""
    #vm.regs[REG_PC] = vm.labels[label]
    vm.regs[REG_PC] += offset


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
    vm.stack.append(vm.regs[idx])
    vm.regs[REG_PC] += 1


def inst_pushi(vm, val):
    """Push an immediate onto the stack."""
    vm.stack.append(val)
    vm.regs[REG_PC] += 1


def inst_pop(vm, idx):
    """Pop a value, save it in register `idx'."""
    vm.regs[idx] = vm.stack.pop()
    vm.regs[REG_PC] += 1


def inst_addarg(vm):
    """Append VAL to ARGS."""
    vm.regs[REG_ARGS].append(vm.regs[REG_VAL])
    vm.regs[REG_PC] += 1


def inst_call(vm):
    """Call closure in VAL with ARGS."""
    closure = vm.regs[REG_VAL]
    if closure.isprim:
        vm.regs[REG_VAL] = closure(*vm.regs[REG_ARGS])
        vm.regs[REG_PC] += 1
    else:
        # save current ENV, code and PC
        record = ActivationRecord(vm.regs[REG_ENV], vm.code, vm.regs[REG_PC] + 1)
        vm.stack.append(record)

        # bind parameters to arguments
        if closure.isvararg:
            # the last parameter is bound to a list
            args = vm.regs[REG_ARGS][:len(closure.params) - 1] + \
                   [vm.regs[REG_ARGS][len(closure.params) - 1:]]
            frm =Frame(closure.params, args, closure.env)
        else:
            frm = Frame(closure.params, vm.regs[REG_ARGS], closure.env)
        vm.regs[REG_ENV] = frm

        # jump to the closure code
        vm.code = closure.body
        vm.regs[REG_PC] = 0


def inst_ret(vm):
    """Return from a procedure call."""
    record = vm.stack.pop()
    vm.regs[REG_ENV] = record.env
    vm.regs[REG_PC] = record.retaddr
    vm.code = record.code


def inst_clrargs(vm):
    """Clear ARGS."""
    vm.regs[REG_ARGS] = []
    vm.regs[REG_PC] += 1


def inst_closure(vm, params, body_code, isvararg):
    """Create a new closure and save it in VAL."""
    closure = Closure(params, body_code, vm.regs[REG_ENV], isvararg=isvararg)
    vm.regs[REG_VAL] = closure
    vm.regs[REG_PC] += 1
