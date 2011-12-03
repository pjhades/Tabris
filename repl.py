# -*- coding: utf-8 -*-
"""
    Read-Evaluate-Print Loop
"""

import tokens
import syntax
import evalscm
import env
import utils

import signal

from errors import *

def setup():
    env.init_env()
    #TODO: other initializations here

def repl_stdin():
    setup()
    tk = tokens.Tokenizer()

    # TODO: capture SIGINT and SIGQUIT for C-c and C-\ hotkeys
    while True:
        while tk.more_expr:
            tk.read_new_line()
            tk.tokenize()
        ##########################
        # TODO: call eval here
        exprs = syntax.parse(tk.token_list)
        for expr in exprs:
            print('syntax:', expr)
            print('  code:', utils.get_clean_code(expr))
            print('output:', evalscm.eval(expr, env.global_env))
            print()
        #print(' in:', syntax.parse(tk.token_list))
        #print('out:', evalscm.eval(syntax.parse(tk.token_list), env.global_env))
        #print('env:')
        #for env in env.all_envs:
        #    print(env)
        ##########################
        tk.reset()

def repl_file(infile):
    setup()
    tk = tokens.Tokenizer(infile=infile)
    while not tk.eof:
        while not tk.eof and tk.more_expr:
            tk.read_new_line()
            tk.tokenize()
        if tk.eof:
            tk.close()
        if tk.more_expr and tk.token_list != [] and tk.eof:
            raise SchemeSysError('incomplete source file')
        elif not tk.more_expr:
            ##########################
            # TODO: all eval here
            exprs = syntax.parse(tk.token_list)
            for expr in exprs:
                print(' in:', expr)
                print('  code:', utils.get_clean_code(expr))
                print('out:', evalscm.eval(expr, env.global_env))
                print()
            #print(tokens.get_clean_code(tk.token_list))
            #print('out:', evalscm.eval(syntax.parse(tk.token_list), env.global_env))
            ##########################
            tk.reset()
