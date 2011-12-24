# -*- coding: utf-8 -*-

class SchemeError(Exception):
    pass

class SchemeParseError(SchemeError):
    pass




# assasin list
# class SchemeSysError(Exception):
#     def __init__(self, msg=''):
#         self.msg = msg
#     def __str__(self):
#         return self.msg
# 
# class SchemeParseError(Exception):
#     def __init__(self, lineno, expr, msg=''):
#         self.expr = expr
#         self.msg = msg
#         self.lineno = lineno
#     def __str__(self):
#         return 'Parse error: {0} in line {1}, near: {2}'.format(self.msg, self.lineno, self.expr)
# 
# class SchemeBadSyntaxError(Exception):
#     def __init__(self, expr, msg=''):
#         self.expr = utils.get_clean_code(expr)
#         self.msg = msg
#     def __str__(self):
#         return 'Bad syntax in {0}: {1}'.format(self.expr, self.msg)
# 
# class SchemeUnboundError(Exception):
#     def __init__(self, var):
#         self.var = var
#     def __str__(self):
#         return self.var + ' is unbound'
# 
# class SchemeEvalError(Exception):
#     def __init__(self, expr, msg=''):
#         self.expr = utils.get_clean_code(expr)
#         self.msg = msg
#     def __str__(self):
#         if self.expr != '':
#             return 'Evaluation error: {0} in expression {1}'.format(self.msg, self.expr)
#         return 'Evaluation error: {0}'.format(self.msg)
# 
# class SchemeDivByZeroError(Exception):
#     def __init__(self, expr):
#         self.expr = expr
#     def __str__(self):
#         return 'Division by zero: ' + self.expr
# 
# class SchemeTypeError(Exception):
#     def __init__(self, expr, msg):
#         self.expr = expr
#         self.msg = msg
#     def __str__(self):
#         return 'Type error in {0}: {1}'.format(self.expr, self.msg)
