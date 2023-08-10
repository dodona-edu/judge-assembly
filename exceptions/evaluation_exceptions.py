from dodona.translator import Translator
from exceptions.utils import FeedbackException
from dodona.dodona_command import ErrorType


class ValidationError(FeedbackException):
    """Base class for evaluation related exceptions in this module."""

    def __init__(self, trans: Translator, msg: str, line: int, pos: int):
        super(ValidationError, self).__init__(trans=trans, msg=msg, line=line, pos=pos)


class LocatableValidationError(ValidationError):
    """Exceptions that can be located"""

    def __init__(self, trans: Translator, msg: str, line: int, pos: int):
        super(LocatableValidationError, self).__init__(trans=trans, msg=msg, line=line, pos=pos)


class TestRuntimeError(ValidationError):
    """Exception that indicates that the test had a runtime error, e.g. crashed"""

    def __init__(self, trans: Translator, line: int, pos: int):
        msg = trans.human_error(ErrorType.RUNTIME_ERROR)
        super(TestRuntimeError, self).__init__(trans=trans, msg=msg, line=line, pos=pos)
