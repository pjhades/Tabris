# -*- coding: utf-8 -*-

import unittest
from trampoline import bounce, pogo_stick

class TramplineTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTrampoline(self):
        # trampolined factorial
        def fact(n, ans, cont):
            if n < 2:
                return bounce(cont, ans)
            else:
                return bounce(fact, n-1, n*ans, cont)

        ans = pogo_stick(bounce(fact, 5, 1, lambda d:d))
        self.assertEqual(ans, 120)

        ans = pogo_stick(bounce(fact, 1, 1, lambda d:d))
        self.assertEqual(ans, 1)


        # member search
        def memq(target, lst, cont):
            if lst == []:
                return bounce(cont, False)
            elif target == lst[0]:
                return bounce(cont, True)
            else:
                return bounce(memq, target, lst[1:], cont)

        ans = pogo_stick(bounce(memq, 3, [1, 2, 3, 4, 5], lambda d:d))
        self.assertEqual(ans, True)

        ans = pogo_stick(bounce(memq, 3, [1, 2, 4, 5, 6], lambda d:d))
        self.assertEqual(ans, False)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TramplineTest('testTrampoline'))
    return suite

if __name__ == '__main__':
    s = suite()
    runner = unittest.TextTestRunner()
    runner.run(s)
