"""report judge's results to Dodona using Dodona commands (partial JSON output)"""

import json
import sys
from abc import ABC
from enum import StrEnum
from types import SimpleNamespace, TracebackType

MIXED_MESSAGE_ARGS = "Message takes one positional argument or keyword arguments, not both"


class ErrorType(StrEnum):
    """Dodona error type"""

    INTERNAL_ERROR = "internal error"
    COMPILATION_ERROR = "compilation error"
    MEMORY_LIMIT_EXCEEDED = "memory limit exceeded"
    TIME_LIMIT_EXCEEDED = "time limit exceeded"
    OUTPUT_LIMIT_EXCEEDED = "output limit exceeded"
    RUNTIME_ERROR = "runtime error"
    WRONG = "wrong"
    WRONG_ANSWER = "wrong answer"
    CORRECT = "correct"
    CORRECT_ANSWER = "correct answer"


class MessagePermission(StrEnum):
    """Dodona permission for a message"""

    EDUCATOR = "educator"


class MessageFormat(StrEnum):
    """Dodona format for a message"""

    TEXT = "text"
    CODE = "code"


class DodonaCommand(ABC):
    """abstract class, parent of all Dodona commands
    This class provides all shared functionality for the Dodona commands. These commands
    should be used in a Python 'with' block.
    Example:
    >>> with Judgement() as judgement:
    ...     with Tab("example tab"):
    ...         pass
    A JSON message will be printed to stdout when entering the 'with' block. The contents of
    the message are the parameters passed to the constructor to the class.
    When exiting the 'with' block, a close JSON message will be printed to stdout. The contents
    of that message are set dynamically on the object that was returned when entering.
    Example:
    >>> with Tab("example tab") as tab:
    ...     tab.badgeCount = 43
    When entering the 'with' block, prints:
    {
        "command": "start-tab",
        "title": "example tab"
    }
    When exiting the 'with' block, prints:
    {
        "command": "close-tab",
        "badgeCount": 43
    }
    """

    def __init__(self, **kwargs):
        self.start_args = SimpleNamespace(**kwargs)
        self.close_args = SimpleNamespace()

    def name(self) -> str:
        """name used in start and close messages, defaults to the lowercase version of the classname"""
        return self.__class__.__name__.lower()

    def start_msg(self) -> dict | None:
        """start message that is printed as JSON to stdout when entering the 'with' block"""
        return {"command": f"start-{self.name()}", **self.start_args.__dict__}

    def close_msg(self) -> dict | None:
        """close message that is printed as JSON to stdout when exiting the 'with' block"""
        return {"command": f"close-{self.name()}", **self.close_args.__dict__}

    @staticmethod
    def __print_command(result: dict | None) -> None:
        """print the provided to stdout as JSON
        :param result: dict that will be JSON encoded and printed to stdout
        """
        if result is None:
            return
        json.dump(result, sys.stdout, indent=1, sort_keys=True)
        sys.stdout.write("\n")  # Next JSON fragment should be on new line

    def __enter__(self) -> SimpleNamespace:
        """print the start message when entering the 'with' block"""
        self.__print_command(self.start_msg())
        return self.close_args

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        """print the close message when exiting the 'with' block, exceptions are propagated"""
        self.__print_command(self.close_msg())
        return False


class Judgement(DodonaCommand):
    """Dodona Judgement"""


class Tab(DodonaCommand):
    """Dodona Tab"""

    def __init__(self, title: str, **kwargs):
        super().__init__(title=title, **kwargs)


class Context(DodonaCommand):
    """Dodona Context"""


class TestCase(DodonaCommand):
    """Dodona TestCase"""

    def __init__(self, **kwargs):
        """create TestCase, the keyword arguments are the content of its description
        Example:
        >>> with TestCase(
        ...     format=MessageFormat.CODE,
        ...     description="This is the message"
        ... ):
        ...     pass
        """
        super().__init__(description=kwargs)


class Test(DodonaCommand):
    """Dodona Test"""

    def __init__(self, description: str, expected: str, **kwargs):
        super().__init__(description=description, expected=expected, **kwargs)


class Message(DodonaCommand):
    """Dodona Message"""

    def __init__(self, *args: str, **kwargs):
        """create Message from a single positional message or from keyword arguments, not both
        Example:
        >>> with Message("This is the message"):
        ...     pass
        >>> with Message(
        ...     format=MessageFormat.CODE,
        ...     description="This is the message"
        ... ):
        ...     pass
        """
        if len(args) > 1 or (args and kwargs):
            raise TypeError(MIXED_MESSAGE_ARGS)
        super().__init__(message=args[0] if args else kwargs)

    def start_msg(self) -> dict:
        """print the "append-message" command and parameters when entering the 'with' block"""
        return {"command": "append-message", **self.start_args.__dict__}

    def close_msg(self) -> None:
        """don't print anything when exiting the 'with' block"""


class Annotation(DodonaCommand):
    """Dodona Annotation"""

    def __init__(self, row: int, text: str, **kwargs):
        super().__init__(row=row, text=text, **kwargs)

    def start_msg(self) -> dict | None:
        """print the "annotate-code" command and parameters when entering the 'with' block"""
        return {"command": "annotate-code", **self.start_args.__dict__}

    def close_msg(self) -> None:
        """don't print anything when exiting the 'with' block"""
