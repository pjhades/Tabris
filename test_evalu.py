# -*- coding: utf-8 -*-

import unittest
import evalu
import enviro
from parser import Tokenizer, parse 
from pair import to_str

class EvaluatorTest(unittest.TestCase):
    def setUp(self):
        self.tk = Tokenizer()
        self.env = enviro.init_global()


    def tearDown(self):
        self.tk = None
        self.env = None


    def p(self, code):
        return parse(self.tk.tokenize_single(code + "\n"))[0]


    def testSelfEvaluating(self):
        exp = self.p('"foo"')
        self.assertEqual('foo', evalu.eval(exp, self.env))

        exp = self.p('#f')
        self.assertEqual(False, evalu.eval(exp, self.env))


    def testQuote(self):
        exp = self.p("'''x")
        self.assertEqual('(quote (quote x))', to_str(evalu.eval(exp, self.env)))

        exp = self.p("'(quote 'x quote)")
        self.assertEqual('(quote (quote x) quote)', to_str(evalu.eval(exp, self.env)))


    def testDefine(self):
        evalu.eval(self.p('(define foo 111)'), self.env)
        exp = self.p('foo')
        self.assertEqual(111, evalu.eval(exp, self.env))


    def testSet(self):
        evalu.eval(self.p('(define bar 111)'), self.env)
        exp = self.p('bar')
        self.assertEqual(111, evalu.eval(exp, self.env))
        evalu.eval(self.p('(set! bar 999)'), self.env)
        exp = self.p('bar')
        self.assertEqual(999, evalu.eval(exp, self.env))


    def testPrims(self):
        cases = (
            ('(+)', 0),
            ('(+ 1 2 3)', 6),
            ('(+ 4/5 1/5)', 1.0),
            ('(- +i +i)', 0),
            ('(*)', 1),
            ('(* 1 2 3)', 6),
            ('(* 1 1 1 0)', 0),
            ('(/ 5)', 1/5),
            ('(/ 1 2 3)', 1/6),
            ('(= 2/4 1/2)', True),
            ('(> 1.3 1.299999)', True),
            ('(= 0.0001 (* 0.00005 2))', True)
        )
        for case in cases:
            self.assertEqual(case[1], evalu.eval(self.p(case[0]), self.env))


    def testIf(self):
        cases = (
            ('(if #t 1 2)', 1),
            ('(if #f 1)', False),
            ('(if #f 1 (if #t 2 3))', 2)
        )
        for case in cases:
            self.assertEqual(case[1], evalu.eval(self.p(case[0]), self.env))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(EvaluatorTest('testSelfEvaluating'))
    suite.addTest(EvaluatorTest('testQuote'))
    suite.addTest(EvaluatorTest('testDefine'))
    suite.addTest(EvaluatorTest('testSet'))
    suite.addTest(EvaluatorTest('testPrims'));

    return suite


if __name__ == '__main__':
    s = suite()
    runner = unittest.TextTestRunner()
    runner.run(s)
