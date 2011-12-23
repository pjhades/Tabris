# -*- coding: utf-8 -*-

class Thread(list):
    pass

def bounce(proc, *args):
    return Thread(['thunk', proc, args])

def fall_death(value):
    return Thread(['value', value])

def pogo_stick(thread):
    while True:
        if not isinstance(thread, Thread):
            raise TypeError('not a trampline thread')

        if thread[0] == 'value':
            return thread[1]
        else:
            thread = thread[1](*thread[2])
