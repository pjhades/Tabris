# -*- coding: utf-8 -*-

import re
from errors import *

import pair
import number
import typedef
import trampoline


# Delimiter characters. If we see these, we have found
# a token and need to add it to the token list.
DELIMS = '"\'\n\t;( )'


# Token types
token_patterns = {
    'string':   re.compile(r'^".*"$', flags=re.DOTALL), \
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
    "'":        re.compile(r"^'$"), \
    '.':        re.compile(r'^\.$')
}

def get_token_type(tok):
    for t in token_patterns:
        mobj = token_patterns[t].match(tok)
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

    def tokenize_single(self, code):
        self._tokens = []
        self._cur_token = ''
        self.tokenize(code)
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
                    self.paren_count += 1
                    self._tokens.append(char)
                elif char == ')':
                    self.paren_count -= 1
                    if self.paren_count < 0:
                        raise SchemeParseError('Unexpected ) at line ' + str(self.lineno))
                    self._tokens.append(char)

            else:
                self._cur_token += char



def consume(tokens, exp_type):
    """Pop the first token from the token list with
    the expected token type."""

    if len(tokens) == 0:
        raise SchemeParseError('meet empty token list')

    if tokens[0][1] != exp_type:
        raise SchemeParseError('expect', expected, 'but see', tokens[0][0])

    return tokens.pop(0)

def parse_lexeme_datum(tokens):
    token = tokens[0]
    token_type = token[1]

    print('>>> parse_lexeme_datum(), tokens:', tokens)
    print('*** consume', tokens[0])

    if token_type == 'boolean':
        consume(tokens, 'boolean')
        if token[0] == '#t':
            return trampoline.fall(typedef.Boolean(True))
        else:
            return trampoline.fall(typedef.Boolean(False))

    elif token_type == 'string':
        consume(tokens, 'string')
        return trampoline.fall(typedef.String(token[0]))

    elif token_type == 'symbol':
        consume(tokens, 'symbol')
        return trampoline.fall(typedef.Symbol(token[0]))

    elif token_type == 'integer':
        consume(tokens, 'integer')
        return trampoline.fall(number.Rational(int(token[0]), 1))

    elif token_type == 'float':
        consume(tokens, 'float')
        return trampoline.fall(number.Real(float(token[0])))

    elif token_type == 'fraction':
        consume(tokens, 'fraction')
        numer, denom = token[0].split('/')
        return trampoline.fall(number.Rational(int(numer), int(denom)))

    elif token_type == 'complex':
        consume(tokens, 'complex')
        part = token_patterns['complex'].search(token[0]).groups()

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

        if typedef.is_true(imag == number.Rational(0, 1)):
            return trampoline.fall(real)
        return trampoline.fall(number.Complex(real, imag))

    else:
        raise SchemeParseError(token, 'is not a lexeme datum')

def parse_rest_sexps(tokens):
    """Parse the S-expressions in the list. The list may 
    be a Scheme list or a dotted partial list."""

    token_type = tokens[0][1]
    
    if token_type == '.':
        # dotted list
        #
        # 1. consume the dot
        # 2. parse_sexp() the final token
        # 3. return the parsed final token
        consume(tokens, '.')
        return trampoline.bounce(parse_sexp, tokens)
    elif token_type != ')':
        # normal list datum
        #
        # 1. parse the datum
        # 2. parse_rest_sexps() the rest tokens
        # 3. cons the result of 1. and 2.
        #TODO
        def f(v):
            def g(first):
                def h(rest):
                    return trampoline.fall(pair.cons(first, rest))
                return h
            return trampoline.sequence(g(v), trampoline.bounce(parse_rest_sexps, tokens))

        return trampoline.sequence(f, trampoline.bounce(parse_sexp, tokens))
    else:
        # closing )
        #
        # return NIL
        return trampoline.fall(pair.NIL)

def parse_list(tokens):
    # list
    #
    # 1. consume the opening (
    # 2. parse_rest_sexps() the content of the list
    # 3. consume the closing )
    # TODO
    def f(v):
        consume(tokens, ')')
        return trampoline.fall(v)
    consume(tokens, '(')
    return trampoline.sequence(f, trampoline.bounce(parse_rest_sexps, tokens))

def parse_sexp(tokens):
    """Parse a single S-expressions."""

    token_type = tokens[0][1]

    print('>>> parse_sexp(), tokens:', tokens)

    if token_type in ('boolean', 'integer', 'float', 'fraction', \
                      'complex', 'string', 'symbol'):
        #return parse_lexeme_datum(tokens)
        return trampoline.bounce(parse_lexeme_datum, tokens)

    elif token_type == "'":
        # quote abbreviation
        #
        # 1. consume the quote
        # 2. parse_sexp() the remaining tokens
        # 3. make_list the symbol 'quote' and the result of 2.

        def f(v):
            return trampoline.fall(pair.make_list('quote', v))
        print('*** consume', tokens[0])
        consume(tokens, "'")
        return trampoline.sequence(f, trampoline.bounce(parse_sexp, tokens))

        #TODO

    elif token_type == '(':
        return trampoline.bounce(parse_list, tokens)

    else:
        raise SchemeParseError('bad expression syntax')

def parse(tokens):
    """The interface. Returns the list of S-expressions
    generated from the given token list."""

    sexps = []
    while True:
        if len(tokens) == 0:
            return sexps
        sexps.append(trampoline.pogo_stick(parse_sexp(tokens)))
