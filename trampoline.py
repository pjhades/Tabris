# -*- coding: utf-8 -*-

def bounce(proc, *args):
    print('>>> bounce(),', proc, args)
    return ['thunk', proc, args]

def fall(value):
    return ['value', value]

def sequence(f, thread):
    """Run thread first then apply f to the result"""

    # 这里应该返回给调度器一个thread

    def ret():
        print('>>> ret()')
        return sequence(f, thread[1](*thread[2]))

    if not isinstance(thread, list) or \
            (thread[0] != 'value' and thread[0] != 'thunk'):
        raise TypeError('not a trampoline thread')

    print('>>> sequence(), thread:', thread)
    if thread[0] == 'value':
        return bounce(f, thread[1])
    else: 
        return bounce(ret)

def pogo_stick(thread):
    while True:
        if not isinstance(thread, list) or \
                (thread[0] != 'value' and thread[0] != 'thunk'):
            raise TypeError('not a trampoline thread')

        if thread[0] == 'value':
            return thread[1]
        else:
            print('>>> pogo_stick() loop, thread:', thread)
            thread = thread[1](*thread[2])
            print('<<< pogo_stick() loop')
