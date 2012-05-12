# -*- coding: utf-8 -*-

from tpair import from_python_list
from environment import Frame
from errors import *

class Closure(object):
    def __init__(self, params, body, env, isprim=False, isvararg=False):
        self.params = params
        self.body = body
        self.env = env
        self.isprim = isprim
        self.isvararg = isvararg

    def __str__(self):
        return '<procedure>'

    def primcall(self, args):
        """Call a primitive procedure."""
        try:
            return self.body(*args)
        except TypeError:
            raise SchemeError('bad arguments')

    def call(self, vm):
        """Normal closure call."""
        # save current ENV, code and PC
        record = ActivationRecord(vm.regs[vm.REG_ENV], vm.code, vm.regs[vm.REG_PC] + 1)
        vm.stack.append(record)

        # bind parameters to arguments
        if self.isvararg:
            # the last parameter is bound to a list
            args = vm.regs[vm.REG_ARGS][:len(self.params) - 1]
            args.append(from_python_list(vm.regs[vm.REG_ARGS][len(self.params) - 1:]))
            if len(self.params) != len(args):
                raise SchemeError('bad arguments')
            frm = Frame(self.params, args, self.env)
        else:
            if len(self.params) != len(vm.regs[vm.REG_ARGS]):
                raise SchemeError('bad arguments')
            frm = Frame(self.params, vm.regs[vm.REG_ARGS], self.env)
        vm.regs[vm.REG_ENV] = frm

        # jump to the closure code
        vm.code = self.body
        vm.codelen = len(vm.code)
        vm.regs[vm.REG_PC] = 0

    def tailcall(self, vm):
        """Make a tail call, create no activation record."""
        # bind parameters to arguments
        if self.isvararg:
            # the last parameter is bound to a list
            args = vm.regs[vm.REG_ARGS][:len(self.params) - 1]
            args.append(from_python_list(vm.regs[vm.REG_ARGS][len(self.params) - 1:]))
            if len(self.params) != len(args):
                raise SchemeError('bad arguments')
            frm = Frame(self.params, args, self.env)
        else:
            if len(self.params) != len(vm.regs[vm.REG_ARGS]):
                raise SchemeError('bad arguments')
            frm = Frame(self.params, vm.regs[vm.REG_ARGS], self.env)
        vm.regs[vm.REG_ENV] = frm

        # jump to the closure code
        vm.code = self.body
        vm.codelen = len(vm.code)
        vm.regs[vm.REG_PC] = 0


class ActivationRecord(object):
    def __init__(self, env, code, retaddr):
        self.env = env
        self.code = code
        self.retaddr = retaddr

 
class Continuation(object):
    def __init__(self, vm):
        import copy
        self.stack = copy.deepcopy(vm.stack)

