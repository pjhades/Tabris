# -*- coding: utf-8 -*-

#class bounce(object):
#    def __init__(self, func, *args, **kwargs):
#        self.func = func
#        self.args = args
#        self.kwargs = kwargs
#    def __call__(self):
#        return self.func(*self.args, **self.kwargs)

def bounce(func, *args, **kwargs):
    return (func, args, kwargs)

def pogo_stick(thread):
    while isinstance(thread, tuple):
        thread = thread[0](*thread[1], **thread[2])
    return thread
    #while isinstance(thread, bounce):
    #    thread = thread()
    #return thread

