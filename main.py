#!/usr/bin/env python
# -*- coding: utf-8 -*-

import repl
import env

if __name__ == '__main__':
    #def handler(signal, frame):
    #    print('call (exit) to quit')

    #signal.signal(signal.SIGINT, handler)
    #signal.signal(signal.SIGQUIT, handler)

    #environment.init_env()
    #environment.add_binding('foo', 5, environment.global_env)
    #environment.add_binding('bar', 6, environment.global_env)
    #environment.add_binding('baz', 7, environment.global_env)

    #environment.extend_env(['x', 'y'], [111, 222], environment.global_env)
    #environment.extend_env(['foo', 'baz'], [123, 456], environment.all_envs[0])

    #print(environment.lookup_variable('foo', environment.all_envs[0]))
    #environment.add_binding('fuck', 555, environment.all_envs[0])
    #environment.set_variable('x', 100000, environment.all_envs[0])

    #print(environment.all_envs)

    # interactive mode
    #repl.repl_stdin()
    # normal mode
    #repl.repl_file('./test/test_env.scm')

    repl.setup()
    prompt = repl.Prompt()
    prompt.loop()

