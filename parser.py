# -*- coding: utf-8 -*-

"""Tokenizer for lexical analysis and parser for syntax analysis."""

import re

from trampoline import pogo_stick, Bounce
from pair_lib import make_list, cons, NIL
from basic_type import Boolean, Symbol, String, is_true
from number_type import Rational, Real, Complex
from errors import *

# Delimiter characters. If we see these, we have found
# a token and need to add it to the token list.
DELIMS = '"\'\n\t;( )'

# Token types
token_patterns = [
    ('string',   re.compile(r'^".*"$', flags=re.DOTALL)), \
    ('integer',  re.compile(r'^[+-]?\d+$')), \
    ('float',    re.compile(r'^[+-]?(\d+\.\d*|\.\d+)$')), \
    ('fraction', re.compile(r'^[+-]?\d+/\d+$')), \
    ('complex',  re.compile(r'''(
                                ^( ([+-]?\d+              
                                    |
                                    [+-]?(\d+\.\d*|\.\d+) 
                                    |
                                    [+-]?\d+/\d+)          

                                   ([+-]                 
                                    |
                                    [+-]\d+              
                                    |
                                    [+-](\d+\.\d*|\.\d+) 
                                    |
                                    [+-]\d+/\d+)i$ )
                                 |
                                 ^ ([+-]                  
                                    |
                                    [+-]?\d+              
                                    |
                                    [+-]?(\d+\.\d*|\.\d+) 
                                    |
                                    [+-]?\d+/\d+)i$ 
                                )
                            ''', flags=re.VERBOSE)), \
    ('boolean',  re.compile(r'^#[tf]$')), \
    ('(',        re.compile(r'^\($')), \
    (')',        re.compile(r'^\)$')), \
    ("'",        re.compile(r"^'$")), \
    ('.',        re.compile(r'^\.$')), \
    ('symbol',   re.compile(r'^[\w!$%&*+-./:<=>?@^_~]+$'))
]

def get_token_type(tok):
    for t in token_patterns:
        mobj = t[1].match(tok)
        if mobj:
            return (tok, t[0])
    raise SchemeError('unknown token ' + tok)

class Tokenizer(object):
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
        """\
        Return the tokens found, get ready for the next round, 
        should only be called when need_more_code() returns False.
        """ 
        tokens = self._tokens
        self._tokens = []
        self._cur_token = ''
        return [get_token_type(tok) for tok in tokens]

    def tokenize_single(self, code):
        self._tokens = []
        self._cur_token = ''
        self.tokenize(code)

        if self.need_more_code():
            raise SchemeError('bad single line expression ' + code)

        return self.get_tokens()

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

            if char in DELIMS:
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
                    self.quote_not_end = False
                    self.paren_count += 1
                    self._tokens.append(char)
                elif char == ')':
                    self.paren_count -= 1
                    if self.paren_count < 0:
                        raise SchemeError('Unexpected ) at line ' + str(self.lineno))
                    self._tokens.append(char)

            else:
                self._cur_token += char

def consume(tokens, exp_type):
    """\
    Pop the first token from the token list with
    the expected token type.
    """
    if len(tokens) == 0:
        raise SchemeError('meet empty token list')
    if tokens[0][1] != exp_type:
        raise SchemeError('expect %s, given %s' % (exp_type, tokens[0][0]))
    return tokens.pop(0)

def parse_lexeme_datum(tokens, cont):
    token = tokens[0]
    token_type = token[1]

    if token_type == 'boolean':
        consume(tokens, 'boolean')
        if token[0] == '#t':
            return Bounce(cont, Boolean(True))
        else:
            return Bounce(cont, Boolean(False))

    elif token_type == 'string':
        consume(tokens, 'string')
        # strip the quotes
        return Bounce(cont, String(token[0][1:-1]))

    elif token_type == 'symbol':
        consume(tokens, 'symbol')
        return Bounce(cont, Symbol(token[0]))

    elif token_type == 'integer':
        consume(tokens, 'integer')
        return Bounce(cont, Rational(int(token[0]), 1))

    elif token_type == 'float':
        consume(tokens, 'float')
        return Bounce(cont, Real(float(token[0])))

    elif token_type == 'fraction':
        consume(tokens, 'fraction')
        numer, denom = token[0].split('/')
        return Bounce(cont, Rational(int(numer), int(denom)))

    elif token_type == 'complex':
        consume(tokens, 'complex')
        part = token_patterns[4][1].search(token[0]).groups()

        # fetch the two parts
        if part[2] and part[4]:
            real, imag = part[2], part[4]
        else:
            real, imag = '0', part[6]

        # if imaginary is +1 or -1
        if imag in '+-':
            imag = '-1' if imag == '-' else '+1'

        real = parse(Tokenizer().tokenize_single(real + '\n'))[0]
        imag = parse(Tokenizer().tokenize_single(imag + '\n'))[0]

        if is_true(imag == Rational(0, 1)):
            return Bounce(cont, real)
        return Bounce(cont, Complex(real, imag))

    else:
        raise SchemeError(token, 'is not a lexeme datum')

def parse_rest_sexps(tokens, cont):
    """\
    Parse the S-expressions in the list. The list may 
    be a Scheme list or a dotted partial list.
    """
    token_type = tokens[0][1]
    
    if token_type == '.':
        consume(tokens, '.')
        return Bounce(parse_sexp, tokens, cont)
    elif token_type != ')':
        def done_first(first):
            def done_rest(rest):
                return Bounce(cont, cons(first, rest))
            return Bounce(parse_rest_sexps, tokens, done_rest)
        return Bounce(parse_sexp, tokens, done_first)
    else:
        return Bounce(cont, NIL)

def parse_list(tokens, cont):
    """Parse a Scheme list."""
    def done_rest(rest):
        consume(tokens, ')')
        return Bounce(cont, rest)

    consume(tokens, '(')
    return Bounce(parse_rest_sexps, tokens, done_rest)

def parse_sexp(tokens, cont):
    """Parse a single S-expression."""
    token_type = tokens[0][1]

    if token_type in ('boolean', 'integer', 'float', 'fraction', 'complex', 'string', 'symbol'):
        return Bounce(parse_lexeme_datum, tokens, cont)
    elif token_type == "'":
        def make_quote(word):
            return Bounce(cont, make_list(Symbol('quote'), word))
        consume(tokens, "'")
        return Bounce(parse_sexp, tokens, make_quote)
    elif token_type == '(':
        return Bounce(parse_list, tokens, cont)
    else:
        raise SchemeError('bad expression syntax')

def parse(tokens):
    """\
    The interface. Returns the list of S-expressions
    generated from the given token list.
    """
    sexps = []
    while True:
        if len(tokens) == 0:
            return sexps
        sexps.append(pogo_stick(Bounce(parse_sexp, tokens, lambda d:d)))
