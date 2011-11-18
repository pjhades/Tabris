#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

if __name__ == '__main__':
    sys.path.append('../')

    from scm_types import *

    a = Rational(1, 3)
    b = Rational(2, 3)
    assert(a + b == Rational(1, 1))

    a = Rational(0, 3)
    b = Rational(4, 5)
    assert(a + b == Rational(4, 5))

    a = Rational(45, 1)
    b = Rational(-45, 1)
    assert(a + b == Rational(0, 4))

    a = Rational(6, 4)
    b = Rational(2, 3)
    assert(a + b == Rational(13, 6))

    a = Rational(3, 4)
    b = Complex(Rational(2, 1), Rational(3, 1))
    assert(a + b == Complex())
