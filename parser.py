# -*- coding: utf-8 -*-

import re
from trampoline import pogo_stick, bounce
from scmlib import *
from tsymbol import tsym
from errors import *

# Delimiter characters. If we see these, we have found
# a token and need to add it to the token list.
DELIMS = '"\'\n\t;( )'


TOKEN_TYPE_STRING = 0
TOKEN_TYPE_INTEGER = 1
TOKEN_TYPE_FLOAT = 2
TOKEN_TYPE_FRACTION = 3
TOKEN_TYPE_COMPLEX = 4
TOKEN_TYPE_BOOLEAN = 5
TOKEN_TYPE_LPAREN = 6
TOKEN_TYPE_RPAREN = 7
TOKEN_TYPE_SINGLE_QUOTE = 8
TOKEN_TYPE_DOT = 9
TOKEN_TYPE_SYMBOL = 10


token_patterns = (
    (TOKEN_TYPE_STRING,   re.compile(r'^".*"$', flags=re.DOTALL)), \
    (TOKEN_TYPE_INTEGER,  re.compile(r'^[+-]?\d+$')), \
    (TOKEN_TYPE_FLOAT,    re.compile(r'^[+-]?(\d+\.\d*|\.\d+)$')), \
    (TOKEN_TYPE_FRACTION, re.compile(r'^[+-]?\d+/\d+$')), \
    (TOKEN_TYPE_COMPLEX,  re.compile(r'''(^(([+-]?\d+|[+-]?(\d+\.\d*|\.\d+))          
                                            ([+-]|[+-]\d+|[+-](\d+\.\d*|\.\d+))i$)
                                           |
                                          ^([+-]|[+-]?\d+|[+-]?(\d+\.\d*|\.\d+))i$ 
                                          )
                                      ''', flags=re.VERBOSE)), \
    (TOKEN_TYPE_BOOLEAN,       re.compile(r'^#[tf]$')), \
    (TOKEN_TYPE_LPAREN,        re.compile(r'^\($')), \
    (TOKEN_TYPE_RPAREN,        re.compile(r'^\)$')), \
    (TOKEN_TYPE_SINGLE_QUOTE,  re.compile(r"^'$")), \
    (TOKEN_TYPE_DOT,           re.compile(r'^\.$')), \
    (TOKEN_TYPE_SYMBOL,        re.compile(r'^[\w!$%&*+-./:<=>?@^_~]+$'))
)


def get_token_type(tok):
    for t in token_patterns:
        mobj = t[1].match(tok)
        if mobj is not None:
            return (tok, t[0])
    raise SchemeError('unknown token ' + tok)


class Tokenizer(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.tokens = []
        self.cur_token = ''

        self.string_not_end = False
        self.quote_not_end = False
        self.comment_not_end = False

        self.paren_count = 0;
        self.lineno = 0

    def need_more_code(self):
        """Check if current code is incomplete.
        """
        return self.paren_count > 0 or self.string_not_end or \
                 self.quote_not_end or self.tokens == []

    def get_tokens(self):
        """Return the tokens found, get ready for the next round, 
        should only be called when need_more_code() returns False.
        """ 
        tokens = self.tokens
        self.tokens = []
        self.cur_token = ''
        return [get_token_type(tok) for tok in tokens]

    def tokenize(self, code):
        self.tokens = []
        self.cur_token = ''
        self.tokenize_piece(code)
        if self.need_more_code():
            raise SchemeError('bad single line expression ' + code)
        return self.get_tokens()

    def tokenize_piece(self, code):
        """Tokenize a given piece of code.
        """
        for char in code:
            if self.string_not_end:
                # take everything inside a string
                self.cur_token += char
                if char != '"':
                    continue

            if self.comment_not_end:
                # ignore everything inside a comment
                if char != '\n':
                    continue

            if char in DELIMS:
                # meet a delimiter, save the token seen
                if self.cur_token != '':
                    self.tokens.append(self.cur_token)
                    self.cur_token = ''
                    self.quote_not_end = False

                if char == '"':
                    if not self.string_not_end:
                        self.cur_token += char
                    self.string_not_end = not self.string_not_end

                elif char == "'":
                    self.tokens.append(char)
                    self.quote_not_end = True

                elif char == ';': 
                    self.comment_not_end = True
                elif char == '\n':
                    self.comment_not_end = False

                elif char == '(':
                    self.quote_not_end = False
                    self.paren_count += 1
                    self.tokens.append(char)
                elif char == ')':
                    if self.paren_count - 1 < 0:
                        raise SchemeError('unexpected ): ' + code.strip())
                    else:
                        self.paren_count -= 1
                        self.tokens.append(char)
            else:
                self.cur_token += char


class Parser(object):
    def __init__(self):
        self.reset()
        #self.sexps = []

    def reset(self):
        self.sexps = []

    def consume(self, tokens, exp_type):
        """Pop the first token from the token list with
        the expected token type.
        """
        if len(tokens) == 0:
            raise SchemeError('meet empty token list')
        if tokens[0][1] != exp_type:
            raise SchemeError('expect %s, given %s' % (exp_type, tokens[0][0]))
        return tokens.pop(0)
    
    def parse_lexeme_datum(self, tokens, cont):
        token = tokens[0]
        token_type = token[1]

        if token_type == TOKEN_TYPE_BOOLEAN:
            self.consume(tokens, TOKEN_TYPE_BOOLEAN)
            if token[0] == '#t':
                return bounce(cont, True)
            else:
                return bounce(cont, False)

        elif token_type == TOKEN_TYPE_STRING:
            self.consume(tokens, TOKEN_TYPE_STRING)
            return bounce(cont, token[0][1:-1])

        elif token_type == TOKEN_TYPE_SYMBOL:
            self.consume(tokens, TOKEN_TYPE_SYMBOL)
            return bounce(cont, tsym(token[0]))

        elif token_type == TOKEN_TYPE_INTEGER:
            self.consume(tokens, TOKEN_TYPE_INTEGER)
            return bounce(cont, int(token[0]))

        elif token_type == TOKEN_TYPE_FLOAT:
            self.consume(tokens, TOKEN_TYPE_FLOAT)
            return bounce(cont, float(token[0]))

        elif token_type == TOKEN_TYPE_FRACTION:
            self.consume(tokens, TOKEN_TYPE_FRACTION)
            numer, denom = token[0].split('/')
            return bounce(cont, float(numer) / float(denom))

        elif token_type == TOKEN_TYPE_COMPLEX:
            self.consume(tokens, TOKEN_TYPE_COMPLEX)
            return bounce(cont, complex(token[0].replace('i', 'j')))
    
        else:
            raise SchemeError(token, 'is not a lexeme datum')
    
    def parse_rest_sexps(self, tokens, cont):
        """Parse the S-expressions in the list. The list may 
        be a Scheme list or a dotted partial list.
        """
        token_type = tokens[0][1]
        if token_type == TOKEN_TYPE_DOT:
            self.consume(tokens, TOKEN_TYPE_DOT)
            return bounce(self.parse_sexp, tokens, cont)

        elif token_type != TOKEN_TYPE_RPAREN:
            def done_first(first):
                nonlocal saved_first_exp
                saved_first_exp = first
                return bounce(self.parse_rest_sexps, tokens, done_rest)

            def done_rest(rest):
                return bounce(cont, cons(saved_first_exp, rest))

            saved_first_exp = None
            return bounce(self.parse_sexp, tokens, done_first)

        else:
            return bounce(cont, NIL)
    
    def parse_list(self, tokens, cont):
        """Parse a Scheme list.
        """
        def done_rest(rest):
            self.consume(tokens, TOKEN_TYPE_RPAREN)
            return bounce(cont, rest)

        self.consume(tokens, TOKEN_TYPE_LPAREN)
        return bounce(self.parse_rest_sexps, tokens, done_rest)
    
    def parse_sexp(self, tokens, cont):
        """Parse a single S-expression.
        """
        token_type = tokens[0][1]
        if token_type in (TOKEN_TYPE_BOOLEAN, 
                          TOKEN_TYPE_INTEGER, 
                          TOKEN_TYPE_FLOAT, 
                          TOKEN_TYPE_FRACTION, 
                          TOKEN_TYPE_COMPLEX, 
                          TOKEN_TYPE_STRING, 
                          TOKEN_TYPE_SYMBOL,):
            return bounce(self.parse_lexeme_datum, tokens, cont)

        elif token_type == TOKEN_TYPE_SINGLE_QUOTE:
            def make_quote(word):
                return bounce(cont, lib_list(tsym('quote'), word))

            self.consume(tokens, TOKEN_TYPE_SINGLE_QUOTE)
            return bounce(self.parse_sexp, tokens, make_quote)

        elif token_type == TOKEN_TYPE_LPAREN:
            return bounce(self.parse_list, tokens, cont)

        else:
            raise SchemeError('bad expression syntax')
    
    def parse(self, tokens):
        """The interface. Returns the list of S-expressions
        generated from the given token list.
        """
        self.sexps = []
        while True:
            if len(tokens) == 0:
                return self.sexps
            self.sexps.append(pogo_stick(bounce(self.parse_sexp, tokens, lambda d:d)))
