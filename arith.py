# -*- coding: utf-8 -*-

from stypes import *
from errors import *

_COMPLEX = 4
_REAL = 2
_RATIONAL = 1

# Additions
def _add_complex(a, b):
    new_real = a.real + b.real
    new_imag = a.imag + b.imag
    if Boolean.true(new_imag == Rational(0, 1)):
        return new_real
    return Complex(new_real, new_imag)

def _add_real(a, b):
    return Real(a.value + b.value)

def _add_rational(a, b):
    new_numer = a.numer * b.denom + b.numer * a.denom
    new_denom = a.denom * b.denom
    gcd = Rational._gcd(new_numer, new_denom)
    new_numer //= gcd
    new_denom //= gcd
    if new_denom < 0:
        new_numer, new_denom = -new_numer, -new_denom
    return Rational(new_numer, new_denom)


# Subtractions
def _sub_complex(a, b):
    new_real = a.real - b.real
    new_imag = a.imag - b.imag
    if Boolean.true(new_imag == Rational(0, 1)):
        return new_real
    return Complex(new_real, new_imag)

def _sub_real(a, b):
    return Real(a.value - b.value)

def _sub_rational(a, b):
    new_numer = a.numer * b.denom - b.numer * a.denom
    new_denom = a.denom * b.denom
    gcd = Rational._gcd(new_numer, new_denom)
    new_numer //= gcd
    new_denom //= gcd
    if new_denom < 0:
        new_numer, new_denom = -new_numer, -new_denom
    return Rational(new_numer, new_denom)

# Multiplications
def _mul_complex(a, b):
    new_real = a.real * b.real - a.imag * b.imag
    new_imag = a.real * b.imag + a.imag * b.real
    if Boolean.true(new_imag == Rational(0, 1)):
        return new_real
    return Complex(new_real, new_imag)

def _mul_real(a, b):
    return Real(a.value * b.value)

def _mul_rational(a, b):
    new_numer = a.numer * b.numer
    new_denom = a.denom * b.denom
    gcd = Rational._gcd(new_numer, new_denom)
    new_numer //= gcd
    new_denom //= gcd
    if new_denom < 0:
        new_numer, new_denom = -new_numer, -new_denom
    return Rational(new_numer, new_denom)

# Divisions
def _div_complex(a, b):
    factor = b.real * b.real + b.imag * b.imag
    c = a * b._conjugate()
    return Complex(c.real / factor, c.imag / factor)

def _div_real(a, b):
    return Real(a.value / b.value)

def _div_rational(a, b):
    new_numer = a.numer * b.denom
    new_denom = a.denom * b.numer
    gcd = Rational._gcd(new_numer, new_denom)
    new_numer //= gcd
    new_denom //= gcd
    if new_denom < 0:
        new_numer, new_denom = -new_numer, -new_denom
    return Rational(new_numer, new_denom)


# Comparisons
def _eq_complex(a, b):
    return (a.real == b.real) * (a.imag == b.imag)

def _ne_complex(a, b):
    return (a.real != b.real) + (a.imag != b.imag)


def _lt_real(a, b):
    return Boolean(a.value < b.value)

def _le_real(a, b):
    return Boolean(a.value <= b.value)

def _gt_real(a, b):
    return Boolean(a.value > b.value)

def _ge_real(a, b):
    return Boolean(a.value >= b.value)

def _eq_real(a, b):
    return Boolean(a.value == b.value)

def _ne_real(a, b):
    return Boolean(a.value != b.value)


def _lt_rational(a, b):
    return Boolean(a.numer * b.denom < a.denom * b.numer)

def _le_rational(a, b):
    return Boolean(a.numer * b.denom <= a.denom * b.numer)

def _gt_rational(a, b):
    return Boolean(a.numer * b.denom > a.denom * b.numer)

def _ge_rational(a, b):
    return Boolean(a.numer * b.denom >= a.denom * b.numer)

def _eq_rational(a, b):
    return Boolean(a.numer * b.denom == a.denom * b.numer)

def _ne_rational(a, b):
    return Boolean(a.numer * b.denom != a.denom * b.numer)


def _rational_to_complex(a):
    return Complex(a, Rational(0, 1))

def _rational_to_real(a):
    return Real(a.numer / a.denom)

def _real_to_complex(a):
    return Complex(a, Real(0.0))

_op_table = {'+': {_COMPLEX: _add_complex, \
                   _REAL: _add_real, \
                   _RATIONAL: _add_rational}, \

             '-': {_COMPLEX: _sub_complex, \
                   _REAL: _sub_real, \
                   _RATIONAL: _sub_rational}, \

             '*': {_COMPLEX: _mul_complex, \
                   _REAL: _mul_real, \
                   _RATIONAL: _mul_rational}, \
             
             '/': {_COMPLEX: _div_complex, \
                   _REAL: _div_real, \
                   _RATIONAL: _div_rational}, \
              
             '>': {_REAL: _gt_real, \
                   _RATIONAL: _gt_rational}, \

             '>=': {_REAL: _ge_real, \
                    _RATIONAL: _ge_rational}, \
                   
             '<': {_REAL: _lt_real, \
                   _RATIONAL: _lt_rational}, \

             '<=': {_REAL: _le_real, \
                    _RATIONAL: _lt_rational}, \

             '==': {_COMPLEX: _eq_complex, \
                    _REAL: _eq_real, \
                    _RATIONAL: _eq_rational}, \

             '!=': {_COMPLEX: _ne_complex, \
                    _REAL: _ne_real, \
                    _RATIONAL: _ne_rational}, \

             '->': {_RATIONAL + _COMPLEX: _rational_to_complex, \
                    _RATIONAL + _REAL: _rational_to_real, \
                    _REAL + _COMPLEX: _real_to_complex}
            }

def _convert(orig, target):
    return _op_table['->'][orig.tag + target.tag](orig)

def check_operand(f):
    def func(a, b):
        try:
            if a.tag > b.tag:
                return f(a, _convert(b, a))
            elif a.tag < b.tag:
                return f(_convert(a, b), b)
            else:
                return f(a, b)
        except AttributeError:
            raise SchemeTypeError('', 'expects numbers as arguments')
        except KeyError:
            raise SchemeTypeError('', 'operation is not supported')
    return func


# Separate the detail of arithmic operations from use
@check_operand
def _add(a, b):
    return _op_table['+'][a.tag](a, b)

@check_operand
def _sub(a, b):
    return _op_table['-'][a.tag](a, b)

@check_operand
def _mul(a, b):
    return _op_table['*'][a.tag](a, b)

@check_operand
def _div(a, b):
    return _op_table['/'][a.tag](a, b)

@check_operand
def _lt(a, b):
    return _op_table['<'][a.tag](a, b)

@check_operand
def _le(a, b):
    return _op_table['<='][a.tag](a, b)

@check_operand
def _gt(a, b):
    return _op_table['>'][a.tag](a, b)

@check_operand
def _ge(a, b):
    return _op_table['>='][a.tag](a, b)

@check_operand
def _eq(a, b):
    return _op_table['=='][a.tag](a, b)

@check_operand
def _ne(a, b):
    return _op_table['!='][a.tag](a, b)


# Number types
class Complex:
    """Real and imaginary parts are guaranteed to be the same type"""
    def __init__(self, real, imag):
        if real.tag > imag.tag:
            imag = _convert(imag, real)
        elif real.tag < imag.tag:
            real = _convert(real, imag)
        self.real = real
        self.imag = imag
        self.tag = _COMPLEX

    def _conjugate(self):
        return Complex(self.real, -self.imag)

    def __add__(self, other):
        return _add(self, other)
    def __sub__(self, other):
        return _sub(self, other)
    def __mul__(self, other):
        return _mul(self, other)
    def __truediv__(self, other):
        return _div(self, other)
    def __neg__(self):
        return Complex(-self.real, -self.imag)

    def __lt__(self, other):
        return _lt(self, other)
    def __le__(self, other):
        return _le(self, other)
    def __gt__(self, other):
        return _gt(self, other)
    def __ge__(self, other):
        return _ge(self, other)
    def __eq__(self, other):
        return _eq(self, other)
    def __ne__(self, other):
        return _ne(self, other)

    def __str__(self):
        if Boolean.true(self.imag == Rational(0, 1)):
            return str(self.real)

        if Boolean.true(self.real == Rational(0, 1)):
            if Boolean.true(self.imag == Rational(1, 1)):
                return 'i'
            elif Boolean.true(self.imag == Rational(-1, 1)):
                return '-i'
            return '{0}i'.format(self.imag)
        elif Boolean.true(self.imag > Rational(0, 1)):
            if Boolean.true(self.imag == Rational(1, 1)):
                return '{0}+i'.format(self.real)
            return '{0}+{1}i'.format(self.real, self.imag)
        else:
            if Boolean.true(self.imag == Rational(-1, 1)):
                return '{0}-i'.format(self.real, self.imag)
            return '{0}{1}i'.format(self.real, self.imag)

class Real:
    def __init__(self, value):
        self.value = value
        self.tag = _REAL

    def __add__(self, other):
        return _add(self, other)
    def __sub__(self, other):
        return _sub(self, other)
    def __mul__(self, other):
        return _mul(self, other)
    def __truediv__(self, other):
        return _div(self, other)
    def __neg__(self):
        return Real(-self.value)

    def __lt__(self, other):
        return _lt(self, other)
    def __le__(self, other):
        return _le(self, other)
    def __gt__(self, other):
        return _gt(self, other)
    def __ge__(self, other):
        return _ge(self, other)
    def __eq__(self, other):
        return _eq(self, other)
    def __ne__(self, other):
        return _ne(self, other)

    def __str__(self):
        return str(self.value)

class Rational:
    def __init__(self, numer, denom):
        if denom == 0:
            raise SchemeDivByZeroError(str(numer) + '/' + str(denom))
        
        gcd = Rational._gcd(numer, denom)
        self.numer = numer // gcd
        self.denom = denom // gcd
        if self.denom < 0:
            self.numer = -self.numer
            self.denom = -self.denom
        self.tag = _RATIONAL

    @staticmethod
    def _gcd(a, b):
        if a < b:
            a, b = b, a
        while b != 0:
            a, b = b, a % b
        return a

    def __add__(self, other):
        return _add(self, other)
    def __sub__(self, other):
        return _sub(self, other)
    def __mul__(self, other):
        return _mul(self, other)
    def __truediv__(self, other):
        return _div(self, other)
    def __neg__(self):
        return Rational(-self.numer, self.denom)

    def __lt__(self, other):
        return _lt(self, other)
    def __le__(self, other):
        return _le(self, other)
    def __gt__(self, other):
        return _gt(self, other)
    def __ge__(self, other):
        return _ge(self, other)
    def __eq__(self, other):
        return _eq(self, other)
    def __ne__(self, other):
        return _ne(self, other)

    def __str__(self):
        if self.numer == 0:
            return '0'
        elif self.denom == 1:
            return str(self.numer)
        else:
            return '{0}/{1}'.format(self.numer, self.denom)
