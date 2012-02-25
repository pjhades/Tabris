# -*- coding: utf-8 -*-

import unittest
import evalu
import enviro
from basic_type import String, Boolean
from number_type import Rational, Real, Complex
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
        "Taste sweet? >_< "
        return parse(self.tk.tokenize_single(code + "\n"))[0]

    def testSelfEvaluating(self):
        exp = self.p('"foo"')
        self.assertEqual(String('foo'), evalu.eval(exp, self.env))

        exp = self.p('#f')
        self.assertEqual(Boolean(False), evalu.eval(exp, self.env))

        exp = self.p('7/6-8i')
        self.assertEqual(Complex(Rational(7, 6), Rational(-8, 1)), \
                         evalu.eval(exp, self.env))

    def testQuote(self):
        exp = self.p("'''x")
        self.assertEqual('(quote (quote x))', to_str(evalu.eval(exp, self.env)))

        exp = self.p("'(quote 'x quote)")
        self.assertEqual('(quote (quote x) quote)', to_str(evalu.eval(exp, self.env)))

    def testDefine(self):
        evalu.eval(self.p('(define foo 111)'), self.env)
        exp = self.p('foo')
        self.assertEqual(Rational(111, 1), evalu.eval(exp, self.env))

    def testSet(self):
        evalu.eval(self.p('(define bar 111)'), self.env)
        exp = self.p('bar')
        self.assertEqual(Rational(111, 1), evalu.eval(exp, self.env))
        evalu.eval(self.p('(set! bar 999)'), self.env)
        exp = self.p('bar')
        self.assertEqual(Rational(999, 1), evalu.eval(exp, self.env))

    def testPrims(self):
        cases = (
            ('(+)', Rational(0, 1)),
            ('(+ 1 2 3)', Rational(6, 1)),
            ('(+ 4/5 1/5)', Rational(1, 1)),
            ('(- +i +i)', Rational(0, 1)),
            ('(*)', Rational(1, 1)),
            ('(* 1 2 3)', Rational(6, 1)),
            ('(* 1 1 1 0)', Rational(0, 1)),
            ('(/ 5)', Rational(1, 5)),
            ('(/ 1 2 3)', Rational(1, 6)),
            ('(= 2/4 1/2)', Boolean(True)),
            ('(> 1.3 1.299999)', Boolean(True)),
            ('(= 0.0001 (* 0.00005 2))', Boolean(True))
        )
        for case in cases:
            self.assertEqual(case[1], evalu.eval(self.p(case[0]), self.env))

    def testIf(self):
        cases = (
            ('(if #t 1 2)', Rational(1, 1)),
            ('(if #f 1)', Boolean(False)),
            ('(if #f 1 (if #t 2 3))', Rational(2, 1))
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
