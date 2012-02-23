# -*- coding: utf-8 -*-

from number_type import is_number
from basic_type import is_string, is_symbol, is_boolean, Boolean

def number_query(v):
    return Boolean(is_number(v))

def string_query(v):
    return Boolean(is_string(v))

def symbol_query(v):
    return Boolean(is_symbol(v))

def boolean_query(v):
    return Boolean(is_boolean(v))

