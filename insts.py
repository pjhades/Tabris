# -*- coding: utf-8 -*-

from tsymbol import Symbol, tsym
from tpair import from_python_list
from control import ActivationRecord, Continuation
from closure import Closure
from environment import Frame
from errors import *

def inst_loadi(vm, idx, val):
    """Load an immediate to register.
    """
    vm.regs[idx] = val
    vm.regs[vm.REG_PC] += 1


def inst_refvar(vm, lexaddr):
    """Reference a variable.
    """
    if not isinstance(lexaddr, tuple):
        val = vm.toplevel[lexaddr]
    else:
        val = vm.regs[vm.REG_ENV].refvar(lexaddr)
    vm.regs[vm.REG_VAL] = val
    vm.regs[vm.REG_PC] += 1


def inst_setvar(vm, lexaddr):
    """Set a variable to the value in VAL register.
    """
    if not isinstance(lexaddr, tuple):
        vm.toplevel[lexaddr] = vm.regs[vm.REG_VAL]
    else:
        vm.regs[vm.REG_ENV].setvar(lexaddr, vm.regs[vm.REG_VAL])
    vm.regs[vm.REG_VAL] = None
    vm.regs[vm.REG_PC] += 1


def inst_bindvar(vm, lexaddr):
    """Add a new binding for variable and the value in VAL.
    """
    if isinstance(lexaddr, tuple):
        lexaddr = lexaddr[1]
    vm.regs[vm.REG_ENV].bindvar(lexaddr, vm.regs[vm.REG_VAL])
    vm.regs[vm.REG_VAL] = None
    vm.regs[vm.REG_PC] += 1


def inst_jt(vm, offset):
    """Jump to label if VAL is true.
    """
    if vm.regs[vm.REG_VAL] is not False:
        vm.regs[vm.REG_PC] += offset
    else:
        vm.regs[vm.REG_PC] += 1


def inst_jf(vm, offset):
    """Jump to label if VAL is false.
    """
    if vm.regs[vm.REG_VAL] is False:
        vm.regs[vm.REG_PC] += offset
    else:
        vm.regs[vm.REG_PC] += 1


def inst_j(vm, offset):
    """Unconditional jump.
    """
    vm.regs[vm.REG_PC] += offset


def inst_extenv(vm):
    """Create a new empty frame.
    """
    frm = Frame([], outer=vm.regs[vm.REG_ENV])
    vm.regs[vm.REG_ENV] = frm
    vm.regs[vm.REG_PC] += 1


def inst_killenv(vm):
    """Kill the current frame and get to its parent.
    """
    vm.regs[vm.REG_ENV] = vm.regs[vm.REG_ENV].outer
    vm.regs[vm.REG_PC] += 1


def inst_pushr(vm, idx):
    """Push reg `idx' onto the stack.
    """
    vm.stack.append(vm.regs[idx])
    vm.regs[vm.REG_PC] += 1


def inst_pushi(vm, val):
    """Push an immediate onto the stack.
    """
    vm.stack.append(val)
    vm.regs[vm.REG_PC] += 1


def inst_pop(vm, idx):
    """Pop a value, save it in register `idx'.
    """
    vm.regs[idx] = vm.stack.pop()
    vm.regs[vm.REG_PC] += 1


def inst_addarg(vm):
    """Append VAL to ARGS.
    """
    vm.regs[vm.REG_ARGS].append(vm.regs[vm.REG_VAL])
    vm.regs[vm.REG_PC] += 1


def inst_call(vm):
    """Call closure in VAL with ARGS.
    """
    closure = vm.regs[vm.REG_VAL]
    if not isinstance(closure, Closure):
        raise SchemeError('not a callable procedure')

    if closure.isprim:
        vm.regs[vm.REG_VAL] = closure.primcall(vm.regs[vm.REG_ARGS])
        vm.regs[vm.REG_PC] += 1
    else:
        # save current ENV, code and PC
        record = ActivationRecord(vm.regs[vm.REG_ENV], vm.code, vm.regs[vm.REG_PC] + 1)
        vm.stack.append(record)

        # bind parameters to arguments
        if closure.isvararg:
            # the last parameter is bound to a list
            args = vm.regs[vm.REG_ARGS][:closure.arity[0] - 1]
            args.append(from_python_list(vm.regs[vm.REG_ARGS][closure.arity[0] - 1:]))
            closure.check_arity(len(args))
            frm = Frame(args, closure.env)
        else:
            closure.check_arity(len(vm.regs[vm.REG_ARGS]))
            frm = Frame(vm.regs[vm.REG_ARGS], closure.env)

        vm.regs[vm.REG_ENV] = frm

        # jump to the closure code
        vm.code = closure.body
        vm.codelen = len(vm.code)
        vm.regs[vm.REG_PC] = 0


def inst_tailcall(vm):
    """Make a tail call to closure in VAL with ARGS.
    """
    closure = vm.regs[vm.REG_VAL]
    if not isinstance(closure, Closure):
        raise SchemeError('not a callable procedure')

    if closure.isprim:
        vm.regs[vm.REG_VAL] = closure.primcall(vm.regs[vm.REG_ARGS])
        vm.regs[vm.REG_PC] += 1
    else:
        # bind parameters to arguments
        if closure.isvararg:
            # the last parameter is bound to a list
            args = vm.regs[vm.REG_ARGS][:closure.arity[0] - 1]
            args.append(from_python_list(vm.regs[vm.REG_ARGS][closure.arity[0] - 1:]))
            closure.check_arity(len(args))
            frm = Frame(args, closure.env)
        else:
            closure.check_arity(len(vm.regs[vm.REG_ARGS]))
            frm = Frame(vm.regs[vm.REG_ARGS], closure.env)

        vm.regs[vm.REG_ENV] = frm

        # jump to the closure code
        vm.code = closure.body
        vm.codelen = len(vm.code)
        vm.regs[vm.REG_PC] = 0


def inst_ret(vm):
    """Return from a procedure call.
    """
    record = vm.stack.pop()
    vm.regs[vm.REG_ENV] = record.env
    vm.regs[vm.REG_PC] = record.retaddr
    vm.code = record.code
    vm.codelen = len(vm.code)


def inst_clrargs(vm):
    """Clear ARGS.
    """
    vm.regs[vm.REG_ARGS] = []
    vm.regs[vm.REG_PC] += 1


def inst_closure(vm, arity, body_code, isvararg):
    """Create a new closure and save it in VAL.
    """
    closure = Closure(arity, body_code, vm.regs[vm.REG_ENV], isvararg=isvararg)
    vm.regs[vm.REG_VAL] = closure
    vm.regs[vm.REG_PC] += 1


def inst_capture(vm):
    """Capture current continuation and save it in VAL.
    """
    vm.regs[vm.REG_VAL] = Continuation(vm)
    vm.regs[vm.REG_PC] += 1


def inst_restore(vm):
    """Restore the continuation in VAL.
    """
    cont = vm.regs[vm.REG_VAL]
    vm.stack = cont.stack
    vm.regs[vm.REG_PC] += 1


"""Implementation of call/cc, equivalent to the code:
 (define (call/cc func)
     (let ((cc (capture)))
         (func (lambda (value)
                   (restore cc)
                   value))))
"""
LIB_CALLCC_CLOSURE = Closure((1, 1), [
                         (inst_capture,),
                         (inst_extenv,),
                         (inst_bindvar, (0, 0)),
                         (inst_clrargs,),
                         (inst_closure, (1, 1), [
                             (inst_refvar, (1, 0)),
                             (inst_restore,),
                             (inst_refvar, (0, 0)),
                             (inst_ret,)
                             ], False),
                         (inst_addarg,),
                         (inst_refvar, (1, 0)),
                         (inst_tailcall,),
                         (inst_killenv,),
                         (inst_ret,)], None)

