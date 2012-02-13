# -*- coding: utf-8 -*-

import unittest
<<<<<<< HEAD
import evalu
from typedef import Symbol
=======
import analyzer
import typedef
from pair import to_str
>>>>>>> d747456fe310a8ccd52fb3557096888f2381a5cf
from parser import Tokenizer, parse 
from pair import to_str

class AnalyzerTest(unittest.TestCase):
    def setUp(self):
        self.tk = Tokenizer()

    def tearDown(self):
        self.tk = None

    def p(self, code):
        """Taste sweet? >_< """
        return parse(self.tk.tokenize_single(code + "\n"))[0]

    def testDefine(self):
        exp = self.p("(define foo bar)")
        self.assertEqual(analyzer.get_define_var(exp), typedef.Symbol('foo'))
        self.assertEqual(analyzer.get_define_val(exp), typedef.Symbol('bar'))

        exp = self.p("(define (inc x) (+ x 1))")
        self.assertEqual(analyzer.get_define_var(exp), typedef.Symbol('inc'))
        self.assertEqual(to_str(analyzer.get_define_val(exp)), "(lambda (x) (+ x 1))")

    def testCond(self):
        exp = self.p("""(cond ((x1 x2) x3)
                              (y1 (y2 y3)
                                  (y4 y5)))""")
        self.assertEqual(to_str(analyzer.cond_to_if(exp)), \
                "(if (x1 x2) x3 (if y1 (begin (y2 y3) (y4 y5)) #f))")

        exp = self.p("""(cond (x1 x2)
                              (y1 y2)
                              (else z1))""")
        self.assertEqual(to_str(analyzer.cond_to_if(exp)), \
                "(if x1 x2 (if y1 y2 z1))")

    def testLet(self):
        exp = self.p("""(let ((x1 y1)
                              (x2 y2)
                              (x3 y3))
                           (foo bar)
                           (bar baz))""")
        self.assertEqual(to_str(analyzer.let_to_application(exp)), \
                "((lambda (x1 x2 x3) (foo bar) (bar baz)) y1 y2 y3)")

        exp = self.p("""(let () 1)""")
        self.assertEqual(to_str(analyzer.let_to_application(exp)), \
                "((lambda () 1))")

def suite():
    suite = unittest.TestSuite()
    #suite.addTest(AnalyzerTest('testDefine'))
    #suite.addTest(AnalyzerTest('testCond'))
    suite.addTest(AnalyzerTest('testLet'))

    return suite

if __name__ == '__main__':
    s = suite()
    runner = unittest.TextTestRunner()
    runner.run(s)
