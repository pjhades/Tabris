# -*- coding: utf-8 -*-

from scmtypes import Symbol


class VM(object):
    def __init__(self):
        self.reset()
    def reset(self):
        self.regs = [0]*4
        self.code = []
        self.codelen = 0
        self.stack = []
        self.lables = {}

