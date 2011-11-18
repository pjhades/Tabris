# -*- coding: utf-8 -*-

import utils
from errors import *

# Additions
def _add_complex_complex(a, b):
    new_real = _op_table['add'][a.real.tag + b.real.tag](a.real, b.real)
    new_imag = _op_table['add'][a.imag.tag + b.imag.tag](a.imag, b.imag)

    if Boolean.true(new_imag == Rational(0, 1)):
        return new_real

    return Complex(new_real, new_imag)

def _add_complex_real(a, b):
    if a.tag == 'Real':
        a, b = b, a
    return a + Complex(b, Real(0.0))

def _add_complex_rational(a, b):
    if a.tag == 'Rational':
        a, b = b, a
    return a + Complex(b, Rational(0, 1))

    return Complex(op(a.real, b), a.imag)

def _add_real_real(a, b):
    return Real(a.value + b.value)

def _add_real_rational(a, b):
    if a.tag == 'Rational':
        a, b = b, a

    r = Real(b.numer / b.denom)

    return Real(a.value + r.value)

def _add_rational_rational(a, b):
    new_numer = a.numer * b.denom + b.numer * a.denom
    new_denom = a.denom * b.denom
    gcd = Rational._gcd(new_numer, new_denom)
    new_numer //= gcd
    new_denom //= gcd
    if new_denom < 0:
        new_numer, new_denom = -new_numer, -new_denom

    return Rational(new_numer, new_denom)


# Subtractions
def _sub_complex_complex(a, b):
    new_real = _op_table['sub'][a.real.tag + b.real.tag](a.real, b.real)
    new_imag = _op_table['sub'][a.imag.tag + b.imag.tag](a.imag, b.imag)

    if Boolean.true(new_imag == Rational(0, 1)):
        return new_real

    return Complex(new_real, new_imag)

def _sub_complex_real(a, b):
    return a - Complex(b, Real(0.0))

def _sub_real_complex(a, b):
    return Complex(a, Real(0.0)) - b

def _sub_complex_rational(a, b):
    return a - Complex(b, Rational(0, 1))

def _sub_rational_complex(a, b):
    return Complex(a, Rational(0, 1)) - b

def _sub_real_real(a, b):
    return Real(a.value - b.value)

def _sub_real_rational(a, b):
    r = Real(b.numer / b.denom)
    return Real(a.value - r.value)

def _sub_rational_real(a, b):
    r = Real(a.numer / a.denom)
    return Real(r.value - b.value)

def _sub_rational_rational(a, b):
    new_numer = a.numer * b.denom - b.numer * a.denom
    new_denom = a.denom * b.denom
    gcd = Rational._gcd(new_numer, new_denom)
    new_numer //= gcd
    new_denom //= gcd
    if new_denom < 0:
        new_numer, new_denom = -new_numer, -new_denom

    return Rational(new_numer, new_denom)

# Multiplications
def _mul_complex_complex(a, b):
    op_rr = _op_table['mul'][a.real.tag + b.real.tag]
    op_ri = _op_table['mul'][a.real.tag + b.imag.tag]
    op_ir = _op_table['mul'][a.imag.tag + b.real.tag]
    op_ii = _op_table['mul'][a.imag.tag + b.imag.tag]

    new_real = op_rr(a.real, b.real) + op_ii(a.imag, b.imag)
    new_imag = op_ri(a.real, b.imag) + op_ir(a.imag, b.real)

    if Boolean.true(new_imag == Rational(0, 1)):
        return new_real
    return Complex(new_real, new_imag)

def _mul_complex_real(a, b):
    if a.tag == 'Real':
        a, b = b, a

    if a.real.tag != 'Real':
        a.real = Real(a.real.numer / a.real.denom)
        a.imag = Real(a.imag.numer / a.imag.denom)

    op = _op_table['mul']['RealReal']

    return Complex(op(a.real, b), op(a.imag, b))

def _mul_complex_rational(a, b):
    if a.tag == 'Rational':
        a, b = b, a

    if a.real.tag == 'Real':
        b = Real(b.numer / b.denom)

    op = _op_table['mul'][a.real.tag + b.tag]

    return Complex(op(a.real, b), op(a.imag, b))

def _mul_real_real(a, b):
    return Real(a.value * b.value)

def _mul_real_rational(a, b):
    if a.tag == 'Rational':
        a, b = b, a
    r = Real(b.numer / b.denom)
    return Real(a.value * r.value)

def _mul_rational_rational(a, b):
    new_numer = a.numer * b.numer
    new_denom = a.denom * b.denom
    gcd = Rational._gcd(new_numer, new_denom)
    new_numer //= gcd
    new_denom //= gcd
    if new_denom < 0:
        new_numer, new_denom = -new_numer, -new_denom

    return Rational(new_numer, new_denom)

# Divisions
def _div_complex_complex(a, b):
    factor = b.real * b.real + b.imag * b.imag

    return a * b._conjugate() / factor

def _div_complex_real(a, b):
    if a.real.tag != 'Real':
        a.real = Real(a.real.numer / a.real.denom)
        a.imag = Real(a.imag.numer / a.imag.denom)

    op = _op_table['div']['RealReal']

    return Complex(op(a.real, b), op(a.imag, b))

def _div_real_complex(a, b):
    if b.real.tag != 'Real':
        b.real = Real(b.real.numer / b.real.denom)
        b.imag = Real(b.imag.numer / b.imag.denom)

    factor = b.real * b.real + b.imag * b.imag

    return a * b._conjugate() / factor

def _div_complex_rational(a, b):
    if a.real.tag == 'Real':
        b = Real(b.numer / b.denom)

    op = _op_table['div'][a.real.tag + b.tag]

    return Complex(op(a.real, b), op(a.imag, b))

def _div_rational_complex(a, b):
    if b.real.tag == 'Real':
        a = Real(a.numer / a.denom)

    factor = b.real * b.real + b.imag * b.imag

    return a * b._conjugate() / factor

def _div_real_real(a, b):
    return Real(a.value / b.value)

def _div_real_rational(a, b):
    r = Real(b.numer / b.denom)
    return Real(a.value / r.value)

def _div_rational_real(a, b):
    r = Real(a.numer / a.denom)
    return Real(r.value / b.value)

def _div_rational_rational(a, b):
    new_numer = a.numer * b.denom
    new_denom = a.denom * b.numer
    gcd = Rational._gcd(new_numer, new_denom)
    new_numer //= gcd
    new_denom //= gcd
    if new_denom < 0:
        new_numer, new_denom = -new_numer, -new_denom

    return Rational(new_numer, new_denom)


# Comparisons
def _eq_complex_complex(a, b):
    return Boolean((a.real == b.real) * (a.imag == b.imag))

def _eq_complex_real(a, b):
    return Boolean(False)

def _eq_complex_rational(a, b):
    return Boolean(False)

def _ne_complex_complex(a, b):
    return Boolean((a.real != b.real) + (a.imag != b.imag))


def _lt_real_real(a, b):
    return Boolean(a.value < b.value)

def _le_real_real(a, b):
    return Boolean(a.value <= b.value)

def _gt_real_real(a, b):
    return Boolean(a.value > b.value)

def _ge_real_real(a, b):
    return Boolean(a.value >= b.value)

def _eq_real_real(a, b):
    return Boolean(a.value == b.value)

def _ne_real_real(a, b):
    return Boolean(a.value != b.value)


def _lt_real_rational(a, b):
    return Boolean(a.value < b.numer / b.denom)

def _lt_rational_real(a, b):
    return Boolean(a.numer / a.denom < b.value)

def _le_real_rational(a, b):
    return Boolean(a.value <= b.numer / b.denom)

def _le_rational_real(a, b):
    return Boolean(a.numer / a.denom <= b.value)

def _gt_real_rational(a, b):
    return Boolean(a.value > b.numer / b.denom)

def _gt_rational_real(a, b):
    return Boolean(a.numer / a.denom > b.value)

def _ge_real_rational(a, b):
    return Boolean(a.value <= b.numer / b.denom)

def _ge_rational_real(a, b):
    return Boolean(a.numer / a.denom <= b.value)

def _eq_real_rational(a, b):
    if a.tag == 'Rational':
        a, b = b, a
    return Boolean(a.value == b.numer / b.denom)

def _ne_real_rational(a, b):
    if a.tag == 'Rational':
        a, b = b, a
    return Boolean(a.value != b.numer / b.denom)


def _lt_rational_rational(a, b):
    return Boolean(a.numer * b.denom < a.denom * b.numer)

def _le_rational_rational(a, b):
    return Boolean(a.numer * b.denom <= a.denom * b.numer)

def _gt_rational_rational(a, b):
    return Boolean(a.numer * b.denom > a.denom * b.numer)

def _ge_rational_rational(a, b):
    return Boolean(a.numer * b.denom >= a.denom * b.numer)

def _eq_rational_rational(a, b):
    return Boolean(a.numer * b.denom == a.denom * b.numer)

def _ne_rational_rational(a, b):
    return Boolean(a.numer * b.denom != a.denom * b.numer)


_op_table = {'add': {'ComplexComplex': _add_complex_complex, \
                    'ComplexReal': _add_complex_real, \
                    'RealComplex': _add_complex_real, \
                    'ComplexRational': _add_complex_rational, \
                    'RationalComplex': _add_complex_rational, \
                    'RealReal': _add_real_real, \
                    'RealRational': _add_real_rational, \
                    'RationalReal': _add_real_rational, \
                    'RationalRational': _add_rational_rational
                   }, \
            'sub': {'ComplexComplex': _sub_complex_complex, \
                    'ComplexReal': _sub_complex_real, \
                    'RealComplex': _sub_real_complex, \
                    'ComplexRational': _sub_complex_rational, \
                    'RationalComplex': _sub_rational_complex, \
                    'RealReal': _sub_real_real, \
                    'RealRational': _sub_real_rational, \
                    'RationalReal': _sub_rational_real, \
                    'RationalRational': _sub_rational_rational
                   }, \
            'mul': {'ComplexComplex': _mul_complex_complex, \
                    'ComplexReal': _mul_complex_real, \
                    'RealComplex': _mul_complex_real, \
                    'ComplexRational': _mul_complex_rational, \
                    'RationalComplex': _mul_complex_rational, \
                    'RealReal': _mul_real_real, \
                    'RealRational': _mul_real_rational, \
                    'RationalReal': _mul_real_rational, \
                    'RationalRational': _mul_rational_rational
                   }, \
            'div': {'ComplexComplex': _div_complex_complex, \
                    'ComplexReal': _div_complex_real, \
                    'RealComplex': _div_real_complex, \
                    'ComplexRational': _div_complex_rational, \
                    'RationalComplex': _div_rational_complex, \
                    'RealReal': _div_real_real, \
                    'RealRational': _div_real_rational, \
                    'RationalReal': _div_rational_real, \
                    'RationalRational': _div_rational_rational 
                   }, \
             'lt': {'RealReal': _lt_real_real, \
                    'RealRational': _lt_real_rational, \
                    'RationalReal': _lt_rational_real, \
                    'RationalRational': _lt_rational_rational
                   }, \
             'le': {'RealReal': _le_real_real, \
                    'RealRational': _le_real_rational, \
                    'RationalReal': _le_rational_real, \
                    'RationalRational': _le_rational_rational
                   }, \
             'gt': {'RealReal': _gt_real_real, \
                    'RealRational': _gt_real_rational, \
                    'RationalReal': _gt_rational_real, \
                    'RationalRational': _gt_rational_rational
                   }, \
             'ge': {'RealReal': _ge_real_real, \
                    'RealRational': _ge_real_rational, \
                    'RationalReal': _ge_rational_real, \
                    'RationalRational': _ge_rational_rational
                   }, \
             'eq': {'ComplexComplex': _eq_complex_complex, \
                    'ComplexReal': _eq_complex_real, \
                    'RealComplex': _eq_complex_real, \
                    'ComplexRational': _eq_complex_rational, \
                    'RationalComplex': _eq_complex_rational, \
                    'RealReal': _eq_real_real, \
                    'RealRational': _eq_real_rational, \
                    'RationalReal': _eq_real_rational, \
                    'RationalRational': _eq_rational_rational
                   }, \
             'ne': {'ComplexComplex': _ne_complex_complex, \
                    'RealReal': _ne_real_real, \
                    'RealRational': _ne_real_rational, \
                    'RationalReal': _ne_real_rational, \
                    'RationalRational': _ne_rational_rational
                   } \
           }


# Call this in each type
# add this layer to separate the modification on the table
def check_num(f):
    """Check if arguments are numbers"""
    def func(a, b):
        try:
            return f(a, b)
        except AttributeError:
            raise SchemeTypeError('', 'expects numbers as arguments')
    return func

def check_permit(f):
    """Check if operation is permitted"""
    def func(a, b):
        try:
            return f(a, b)
        except KeyError:
            raise SchemeTypeError('', 'cannot compare complex numbers')
    return func

@check_num
def _add(a, b):
    return _op_table['add'][a.tag + b.tag](a, b)

@check_num
def _sub(a, b):
    return _op_table['sub'][a.tag + b.tag](a, b)

@check_num
def _mul(a, b):
    return _op_table['mul'][a.tag + b.tag](a, b)

@check_num
def _div(a, b):
    return _op_table['div'][a.tag + b.tag](a, b)

@check_num
@check_permit
def _lt(a, b):
    return _op_table['lt'][a.tag + b.tag](a, b)

@check_num
@check_permit
def _le(a, b):
    return _op_table['le'][a.tag + b.tag](a, b)

@check_num
@check_permit
def _gt(a, b):
    return _op_table['gt'][a.tag + b.tag](a, b)

@check_num
@check_permit
def _ge(a, b):
    return _op_table['ge'][a.tag + b.tag](a, b)

@check_num
@check_permit
def _eq(a, b):
    return _op_table['eq'][a.tag + b.tag](a, b)

@check_num
def _ne(a, b):
    return _op_table['ne'][a.tag + b.tag](a, b)


# Number types
class Complex:
    """Real and imaginary parts are guaranteed to be the same type"""
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag
        if self.real.tag == 'Real':
            if self.imag.tag != 'Real':
                self.imag = Real(self.imag.numer / self.imag.denom)
        else:
            if self.imag.tag == 'Real':
                self.real = Real(self.real.numer / self.real.denom)
        self.tag = 'Complex'

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

    def __eq__(self, other):
        return _eq(self, other)
    def __ne__(self, other):
        return _ne(self, other)

    def __str__(self):
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
        self.tag = 'Real'

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
        self.tag = 'Rational'

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


class Boolean:
    def __init__(self, value):
        self.value = value

    # emulate !, && and ||
    def __mul__(self, other):
        return Boolean(self.value and other.value)
    def __add__(self, other):
        return Boolean(self.value or other.value)
    def __neg__(self, other):
        return Boolean(not self.value)

    @staticmethod
    def true(v):
        if isinstance(v, Boolean) and not v.value:
            return False
        return True

    def __str__(self):
        return '#t' if self.value else '#f'

class String:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

class Symbol:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return '\'' + str(self.value)

class Pair:
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr
    def __str__(self):
        return '({0} . {1})'.format(str(self.car), str(self.cdr))

class List:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return utils.get_clean_code(self.value)

class Procedure:
    def __init__(self, params, body, env, is_prim=False):
        self.params = params # name of params
        self.body = body
        self.env = env
        self.is_prim = is_prim # var arg list if not list
        self.is_var_args = not isinstance(params, list)

    def __str__(self):
        return '<procedure> ' + \
               ('params:{0}, body:{1}, env:{2}'.format(self.params, self.body, self.env) \
               if not self.is_prim else self.body)

