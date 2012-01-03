# -*- coding: utf-8 -*-

class Thread(list):
    pass

def bounce(proc, *args):
    return Thread(['thunk', proc, args])

def fall(value):
    return Thread(['value', value])

class Ret:
    """Record the functions to be applied in the sequence
    and the continuation. If we simply define:

    def ret():
        return sequence(f, thread[1](*thread[2]))

    there will be nested ret() because we call sequence()
    inside the scheduled functions. This class acts as a dirty 
    trick to prevent the ret() calls from exceeding the recursion
    limitation."""

    def __init__(self, funcs, proc, *args):
        self.funcs = funcs
        self.proc = proc
        self.args = args
    def __call__(self):
        return sequence(self.funcs, self.proc(*self.args))

def sequence(fs, thread):
    """Run thread first then apply f to the result"""

    if not isinstance(thread, Thread):
        raise TypeError('not a trampoline thread')

    if thread[0] == 'value':
        # If the thread is a value, apply all the functions
        # to it as long as the result is still a value thread.
        # This can avoid the nested Ret being called a lot of times
        # which will exceed the stack limitation. If the result is
        # not a value thread any more, we store the rest unapplied
        # functions in the Ret and return it to the scheduler.
        for i in range(len(fs) - 1):
            # thread[0] should be 'value'
            # thread[1] should be the real value, now it's the result
            thread[1] = fs[i](thread[1])

            # the result is ['thunk', <Ret>, ()]
            if thread[1][0] == 'thunk' and isinstance(thread[1][1], Ret):
                thread[1][1].funcs += fs[i+1:]
                return thread[1]

            thread[1] = thread[1][1]

        # the final hit
        return bounce(fs[-1], thread[1])
    else: 
        # If the thread is a thunk, give back a Ret object that
        # records the list of functions to apply and the continuation.
        if isinstance(thread[1], Ret):
            # If the thread is already a Ret, we do not create
            # a new one, just add the functions into it's function
            # list.
            thread[1].funcs += fs
            return thread

        return bounce(Ret(fs, thread[1], *thread[2]))

def pogo_stick(thread):
    while True:
        if not isinstance(thread, Thread):
            raise TypeError('not a trampoline thread')

        if thread[0] == 'value':
            return thread[1]
        else:
            thread = thread[1](*thread[2])
