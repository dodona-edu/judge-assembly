from dodona.translator import Translator
from exceptions.utils import FeedbackException


class ValidationError(FeedbackException):
    """Base class for HTML related exceptions in this module."""
    def __init__(self, trans: Translator, msg: str, line: int, pos: int):
        super(ValidationError, self).__init__(trans=trans, msg=msg, line=line, pos=pos)


class LocatableValidationError(ValidationError):
    """Exceptions that can be located"""
    def __init__(self, trans: Translator, msg: str, line: int, pos: int):
        super(LocatableValidationError, self).__init__(trans=trans, msg=msg, line=line, pos=pos)
