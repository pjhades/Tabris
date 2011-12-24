# -*- coding: utf-8 -*-

import re
from errors import *


# Delimiter characters. If we see these, we have found
# a token and need to add it to the token list.
delim_char = '"\'\n\t;( )'


# Token types
token_types = {
    'string':   re.compile(r'^".*"$', flags = re.DOTALL), \
    'integer':  re.compile(r'^[+-]?\d+$'), \
    'float':    re.compile(r'^[+-]?(\d+\.\d*|\.\d+)$'), \
    'fraction': re.compile(r'^[+-]?\d+/\d+$'), \
    'complex':  re.compile(r'''(# both real and imaginary part
                                ^( ([+-]?\d+              | # real is integer
                                    [+-]?(\d+\.\d*|\.\d+) | # real is decimal
                                    [+-]?\d+/\d+)           # real is fraction

                                   ([+-]                 |
                                    [+-]\d+              |
                                    [+-](\d+\.\d*|\.\d+) |
                                    [+-]\d+/\d+)i$ ) 
                                                         |
                                   # no real part
                                 ^ ([+-]                  | # imaginary==1 or -1
                                    [+-]?\d+              |
                                    [+-]?(\d+\.\d*|\.\d+) |
                                    [+-]?\d+/\d+)i$ 
                                )
                                  ''', flags=re.VERBOSE), \
    'symbol':   re.compile(r'^([+-]|[+-]?[a-hj-zA-Z!$%&*/:<=>?^_~@][\w!$%&*/:<=>?^_~@\.+-]*)$'), \
    'boolean':  re.compile(r'^#[tf]$'), \
    '(':        re.compile(r'^\($'), \
    ')':        re.compile(r'^\)$'), \
    "'":   re.compile(r"^'$"), \
    '.':      re.compile(r'^\.$')
}

def get_token_type(tok):
    for t in token_types:
        mobj = token_types[t].match(tok)
        if mobj:
            return (tok, t)
    raise SchemeParseError('unknown token ' + tok)

class Tokenizer:
    def __init__(self):
        self._tokens = []
        self._cur_token = ''

        self.string_not_end = False
        self.quote_not_end = False
        self.comment_not_end = False

        self.paren_count = 0;
        self.lineno = 0

    def need_more_code(self):
        """Check if current code is incomplete"""
        return self.paren_count > 0 or self.string_not_end or \
               self.quote_not_end or self._tokens == []

    def get_tokens(self):
        """
            Return the tokens found, get ready for the next round,
            should only be called when need_more_code() returns False
        """
        tokens = self._tokens
        self._tokens = []
        self._cur_token = ''
        return [get_token_type(tok) for tok in tokens]

    def tokenize(self, code):
        """Tokenize a given piece of code"""
        for char in code:
            # take everything inside a string
            if self.string_not_end:
                self._cur_token += char
                if char != '"':
                    continue

            # ignore everything inside a comment
            if self.comment_not_end:
                if char != '\n':
                    continue

            if char in delim_char:
                # meet a delimiter, save the token seen
                if self._cur_token != '':
                    self._tokens.append(self._cur_token)
                    self._cur_token = ''
                    self.quote_not_end = False

                if char == '"':
                    if not self.string_not_end:
                        self._cur_token += char
                    self.string_not_end = not self.string_not_end

                elif char == '\'':
                    self._tokens.append(char)
                    self.quote_not_end = True

                elif char == ';': 
                    self.comment_not_end = True
                elif char == '\n':
                    self.comment_not_end = False

                elif char == '(':
                    self.paren_count += 1
                    self._tokens.append(char)
                elif char == ')':
                    self.paren_count -= 1
                    if self.paren_count < 0:
                        raise SchemeParseError('Unexpected ) at line ' + str(self.lineno))
                    self._tokens.append(char)

            else:
                self._cur_token += char

