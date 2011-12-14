# -*- coding: utf-8 -*-

from errors import *


# Delimiter characters. If we see these, we have found
# a token and need to add it to the token list.
delim_char = '"\'\n\t;( )'


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
        """Return the tokens found, get ready for the next round"""
        tokens = self._tokens
        self._tokens = []
        self._cur_token = ''
        return tokens

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

