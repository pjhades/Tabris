# -*- coding: utf-8 -*-

REG_PC = 32
REG_BP = 33
REG_SP = 34
NUM_REGS = 35


def mov_(vm, inst):
    dst, src = inst[1:]
    vm.reg[dst] = vm.reg[src]
    vm.reg[REG_PC] += 1



def movi_(vm, inst):
    r, x = inst[1:]
    vm.reg[r] = x
    vm.reg[REG_PC] += 1



def store_(vm, inst):
    m, r = inst[1:]
    vm.data[m] = vm.reg[r]
    vm.reg[REG_PC] += 1



def load_(vm, inst):
    r, m = inst[1:]
    vm.reg[r] = vm.data[m]
    vm.reg[REG_PC] += 1



def loadr_(vm, inst):
    r, base, offset = inst[1:]
    vm.reg[r] = vm.stack[vm.reg[base] + offset]
    vm.reg[REG_PC] += 1



def add_(vm, inst):
    rs, r1, r2 = inst[1:]
    vm.reg[rs] = vm.reg[r1] + vm.reg[r2]
    vm.reg[REG_PC] += 1



def sub_(vm, inst):
    rs, r1, r2 = inst[1:]
    vm.reg[rs] = vm.reg[r1] - vm.reg[r2]
    vm.reg[REG_PC] += 1



def mul_(vm, inst):
    rs, r1, r2 = inst[1:]
    vm.reg[rs] = vm.reg[r1] * vm.reg[r2]
    vm.reg[REG_PC] += 1



def div_(vm, inst):
    rs, r1, r2 = inst[1:]
    vm.reg[rs] = vm.reg[r1] / vm.reg[r2]
    vm.reg[REG_PC] += 1



def mod_(vm, inst):
    rs, r1, r2 = inst[1:]
    vm.reg[rs] = vm.reg[r1] % vm.reg[r2]
    vm.reg[REG_PC] += 1


def addi_(vm, inst):
    rs, r1, x = inst[1:]
    vm.reg[rs] = vm.reg[r1] + x
    vm.reg[REG_PC] += 1



def subi_(vm, inst):
    rs, r1, x = inst[1:]
    vm.reg[rs] = vm.reg[r1] - x
    vm.reg[REG_PC] += 1



def muli_(vm, inst):
    rs, r1, x = inst[1:]
    vm.reg[rs] = vm.reg[r1] * x
    vm.reg[REG_PC] += 1



def divi_(vm, inst):
    rs, r1, x = inst[1:]
    vm.reg[rs] = vm.reg[r1] / x
    vm.reg[REG_PC] += 1



def modi_(vm, inst):
    rs, r1, x = inst[1:]
    vm.reg[rs] = vm.reg[r1] % x
    vm.reg[REG_PC] += 1


def jmp_(vm, inst):
    vm.reg[REG_PC] = vm.labels[inst[1]]


def jt_(vm, inst):
    dst = inst[1]
    if vm.flag:
        vm.reg[REG_PC] = vm.labels[dst]
    else:
        vm.reg[REG_PC] += 1


def push_(vm, inst):
    r = inst[1]
    vm.stack.append(vm.reg[r])
    vm.reg[REG_SP] += 1
    vm.reg[REG_PC] += 1


def pushi_(vm, inst):
    x = inst[1]
    vm.stack.append(x)
    vm.reg[REG_SP] += 1
    vm.reg[REG_PC] += 1


def pop_(vm, inst):
    r = inst[1]
    vm.reg[r] = vm.stack.pop()
    vm.reg[REG_SP] -= 1
    vm.reg[REG_PC] += 1


def call_(vm, inst):
    addr = inst[1]
    vm.stack.append(vm.reg[REG_PC] + 1)
    vm.reg[REG_SP] += 1
    vm.reg[REG_PC] = vm.labels[addr]


def ret_(vm, inst):
    depth = inst[1]
    vm.reg[REG_PC] = vm.stack.pop()
    for i in range(depth):
        vm.stack.pop()
    vm.reg[REG_SP] -= depth + 1


def test_(vm, inst):
    f, args = inst[1], [vm.reg[x] for x in inst[2:]]
    vm.flag = vm.funcs[f](*args)
    vm.reg[REG_PC] += 1


def nop_(vm, inst):
    vm.reg[REG_PC] += 1
    pass


funcs_map = {
    'eq': lambda x,y: x == y, 
    'ne': lambda x,y: x != y,
    'gt': lambda x,y: x > y,
    'lt': lambda x,y: x < y,
    'ge': lambda x,y: x >= y,
    'le': lambda x,y: x >= y,
}
