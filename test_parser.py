# -*- coding: utf-8 -*-

import unittest
import parser

class TokenizerTest(unittest.TestCase):
    def setUp(self):
        self.tokenizer = parser.Tokenizer()

    def tearDown(self):
        self.tokenizer = None

    def testTokenizer(self):
        cases = [("lambda", [("lambda", "symbol")]), \

                 ("12345", [("12345", "integer")]), \

                 ("-4/56", [("-4/56", "fraction")]), \

                 ("0.", [("0.", "float")]), \

                 ("-6.2350-0i", [("-6.2350-0i", "complex")]), \

                 ("+i", [("+i", "complex")]), \

                 ("-i", [("-i", "complex")]), \

                 ("\"this is a string\"", [("\"this is a string\"", "string")]), \

                 ("""\"a string
spans multiple
lines\"""", [("\"a string\nspans multiple\nlines\"", "string")]), \

                 ("'''x", [("'", "'"), ("'", "'"), ("'", "'"), ("x", "symbol")]), \

                 ("""'
                     '
                     '
                     x""", [("'", "'"), ("'", "'"), ("'", "'"), ("x", "symbol")]), \

                 ("'(a . (b . ()))", [("'", "'"), ("(", "("), ("a", "symbol"), \
                                      (".", "."), ("(", "("), ("b", "symbol"), \
                                      (".", "."), ("(", "("), (")", ")"), \
                                      (")", ")"), (")", ")")]), \

                 ("; this is \"comm\"ent", []), \

                 ('";not comment"', [('";not comment"', "string")])]

        for case in cases:
            self.tokenizer.tokenize(case[0] + '\n')
            self.assertEqual(self.tokenizer.get_tokens(), case[1])

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TokenizerTest('testTokenizer'))
    return suite

if __name__ == '__main__':
    s = suite()
    runner = unittest.TextTestRunner()
    runner.run(s)
