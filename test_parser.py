# -*- coding: utf-8 -*-

import unittest
import parser

class TokenizerTest(unittest.TestCase):
    def setUp(self):
        self.tokenizer = parser.Tokenizer()

    def tearDown(self):
        self.tokenizer = None

    def testTokenizer(self):
        cases = [("lambda", ["lambda"]), \
                 ("12345", ["12345"]), \
                 ("-4/56", ["-4/56"]), \
                 ("0.", ["0."]), \
                 ("-6.2350-0i", ["-6.2350-0i"]), \
                 ("+i", ["+i"]), \
                 ("\"this is a string\"", ["\"this is a string\""]), \
                 ("""\"a string
spans multiple
lines\"""", ["\"a string\nspans multiple\nlines\""]), \
                 ("'''x", ["'", "'", "'", "x"]), \
                 ("""'
                     '
                     '
                     x""", ["'", "'", "'", "x"]), \
                 ("'(a . (b . ()))", ["'", "(", "a", ".", "(", "b", ".", "(", ")", ")", ")"]), \
                 ("; this is \"comm\"ent", []), \
                 ('";not comment"', ['";not comment"'])]

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
