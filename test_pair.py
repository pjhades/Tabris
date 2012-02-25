# -*- coding: utf-8 -*-

import unittest
from pair import Pair, to_python_list
from pair_lib import *

class PairTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPairCreating(self):
        self.assertEqual(Pair([1, 2]), [1, 2])
        self.assertEqual(Pair([[1, 2], [3, 4]]), [[1, 2], [3, 4]])

    def testConsing(self):
        self.assertEqual(cons(1, 2), [1, 2])
        self.assertEqual(cons(1, [2, 3]), [1, [2, 3]])
        self.assertEqual(cons([1, 2], [3, 4]), [[1, 2], [3, 4]])

    def testListMaking(self):
        self.assertEqual(make_list(1, 2), [1, [2, []]])
        self.assertEqual(make_list(1, [2, 3]), [1, [[2, 3], []]])
        self.assertEqual(make_list([1, 2], [3, 4]), [[1, 2], [[3, 4], []]])

    def testCarCdr(self):
        p = cons(1,2)
        self.assertEqual(car(p), 1)
        self.assertEqual(cdr(p), 2)

        p = cons([1,2], [3,4])
        self.assertEqual(caar(p), 1)
        self.assertEqual(cadr(p), 3)
        self.assertEqual(cdar(p), 2)
        self.assertEqual(cddr(p), 4)

        p = cons([[1,2],[3,4]], [[5,6],[7,8]])
        self.assertEqual(caaar(p), 1)
        self.assertEqual(caadr(p), 5)
        self.assertEqual(cadar(p), 3)
        self.assertEqual(caddr(p), 7)
        self.assertEqual(cdaar(p), 2)
        self.assertEqual(cdadr(p), 6)
        self.assertEqual(cddar(p), 4)
        self.assertEqual(cdddr(p), 8)

        p = cons([[[1,2],[3,4]], [[5,6],[7,8]]], \
                 [[[9,10],[11,12]], [[13,14],[15,16]]])
        self.assertEqual(caaaar(p), 1)
        self.assertEqual(caaadr(p), 9)
        self.assertEqual(caadar(p), 5)
        self.assertEqual(caaddr(p), 13)
        self.assertEqual(cadaar(p), 3)
        self.assertEqual(cadadr(p), 11)
        self.assertEqual(caddar(p), 7)
        self.assertEqual(cadddr(p), 15)
        self.assertEqual(cdaaar(p), 2)
        self.assertEqual(cdaadr(p), 10)
        self.assertEqual(cdadar(p), 6)
        self.assertEqual(cdaddr(p), 14)
        self.assertEqual(cddaar(p), 4)
        self.assertEqual(cddadr(p), 12)
        self.assertEqual(cdddar(p), 8)
        self.assertEqual(cddddr(p), 16)

    def testLength(self):
        self.assertEqual(get_length(make_list(1, 2, 3)), 3)
        self.assertEqual(get_length(make_list(1, (2, 2), 3)), 3)
        self.assertEqual(get_length(make_list()), 0)
        self.assertEqual(get_length(NIL), 0)

        try:
            get_length(cons(1,2))
        except SchemeError:
            pass

    def testAppend(self):
        p1 = make_list(1, 2, 3)
        p2 = make_list(4, 5)
        p3 = cons(6, 7)
        p4 = make_list(1, cons(2, 3), 4)

        self.assertEqual(append_lst(p1, p2), make_list(1, 2, 3, 4, 5))
        self.assertEqual(append_lst(p1, p3), cons(1, cons(2, cons(3, p3))))
        self.assertEqual(append_lst(NIL, 123), 123)
        self.assertEqual(append_lst(NIL, p4), p4)
        self.assertEqual(append_lst(p4, p2), cons(1, cons(cons(2, 3), cons(4, cons(4, cons(5, NIL))))))
        self.assertEqual(append_lst(), NIL)

        try:
            append_lst(p1, 123, p2)
        except SchemeError:
            pass

    def testReverse(self):
        p1 = make_list(1, 2, 3, 4, 5)
        p2 = make_list(1, cons(2, 3), 4)
        
        self.assertEqual(reverse_lst(p1), make_list(5, 4, 3, 2, 1))
        self.assertEqual(reverse_lst(p2), make_list(4, cons(2, 3), 1))
        self.assertEqual(reverse_lst(NIL), NIL)

    def testListTail(self):
        p1 = make_list(1, 2, 3, 4)
        p2 = cons(1, 2)
        p3 = cons(1, cons(2, cons(3, 4)))

        self.assertEqual(get_list_tail(p1, 2), make_list(3, 4))
        self.assertEqual(get_list_tail(p1, 3), make_list(4))
        self.assertEqual(get_list_tail(p1, 4), NIL)
        self.assertEqual(get_list_tail(p2, 0), cons(1, 2))
        self.assertEqual(get_list_tail(p2, 1), 2)
        self.assertEqual(get_list_tail(p3, 2), cons(3, 4))

        try:
            get_list_tail(p1, 100)
        except SchemeError:
            pass

    def testToPythonList(self):
        self.assertEqual(to_python_list(make_list(1,2,3)), [1,2,3])


def suite():
    suite = unittest.TestSuite()
    suite.addTest(PairTest('testPairCreating'))
    suite.addTest(PairTest('testConsing'))
    suite.addTest(PairTest('testListMaking'))
    suite.addTest(PairTest('testCarCdr'))
    suite.addTest(PairTest('testLength'))
    suite.addTest(PairTest('testAppend'))
    suite.addTest(PairTest('testReverse'))
    suite.addTest(PairTest('testListTail'))
    suite.addTest(PairTest('testToPythonList'))

    return suite

if __name__ == '__main__':
    s = suite()
    runner = unittest.TextTestRunner()
    runner.run(s)
