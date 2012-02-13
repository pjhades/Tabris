# -*- coding: utf-8 -*-

import unittest
from pair import *

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
        self.assertEqual(car(cons(1, 2)), 1)
        self.assertEqual(car(cons([1, 2], 3)), [1, 2])
        self.assertEqual(cdr(cons(1, 2)), 2)
        self.assertEqual(cdr(cons(1, [2, 3])), [2, 3])

    def testLength(self):
        self.assertEqual(get_length(make_list(1, 2, 3)), 3)
        self.assertEqual(get_length(make_list(1, (2, 2), 3)), 3)
        self.assertEqual(get_length(make_list()), 0)
        self.assertEqual(get_length(NIL), 0)

    def testAppend(self):
        p1 = make_list(1, 2, 3)
        p2 = make_list(4, 5)
        p3 = cons(6, 7)
        p4 = make_list(1, cons(2, 3), 4)

        self.assertEqual(append_lst(p1, p2), make_list(1, 2, 3, 4, 5))
        self.assertEqual(append_lst(p1, p3), \
                cons(1, cons(2, cons(3, p3))))
        self.assertEqual(append_lst(NIL, 123), 123)
        self.assertEqual(append_lst(NIL, p4), p4)
        self.assertEqual(append_lst(p4, p2), \
                cons(1, cons(cons(2, 3), \
                cons(4, cons(4, cons(5, NIL))))))
        self.assertEqual(append_lst(), NIL)

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
    return suite

if __name__ == '__main__':
    s = suite()
    runner = unittest.TextTestRunner()
    runner.run(s)
