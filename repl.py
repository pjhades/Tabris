# -*- coding: utf-8 -*-
"""
    Read-Evaluate-Print Loop
"""

import tokenizer
import syntax
import evalscm
import env
import utils

import signal

from errors import *


import parser


class Prompt:
    def __init__(self):
        self.tokenizer = parser.Tokenizer()
        self.PS1 = "scheme >>> "
        self.PS2 = "       ... "

    # TODO: capture C-c C-\ signals
    def loop(self):
        while True:
            self.tokenizer.tokenize(input(self.PS1) + '\n')
            while self.tokenizer.need_more_code():
                self.tokenizer.tokenize(input(self.PS2) + '\n')
            print('tokens:', self.tokenizer.get_tokens())

            


def setup():
    env.init_env()
    #TODO: other initializations here

def repl_stdin():
    setup()
    tk = tokenizer.Tokenizer()

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
    tk = tokenizer.Tokenizer(infile=infile)
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
                print('  in:', expr)
                print('code:', utils.get_clean_code(expr))
                print(' out:', evalscm.eval(expr, env.global_env))
                print()
            #print(tokenizer.get_clean_code(tk.token_list))
            #print('out:', evalscm.eval(syntax.parse(tk.token_list), env.global_env))
            ##########################
            tk.reset()
