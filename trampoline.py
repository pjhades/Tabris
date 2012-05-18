# -*- coding: utf-8 -*-

class bounce(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
    def __call__(self):
        return self.func(*self.args, **self.kwargs)

def pogo_stick(thread):
    while isinstance(thread, bounce):
        thread = thread()
    return thread

