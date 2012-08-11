# -*- coding: utf-8 -*-

# TODO: distinguish different types of errors

class SchemeError(Exception):
    pass

class SchemeKeyboardInterrupt(SchemeError):
    pass
