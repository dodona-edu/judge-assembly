from types import SimpleNamespace

from dodona.dodona_command import Message, MessageFormat, ErrorType, MessagePermission, Annotation
from dodona.dodona_config import DodonaConfig
from dodona.translator import Translator
import traceback
import re


def invalid_suites(judge: SimpleNamespace, config: DodonaConfig):
    """Show the students a message saying that the suites were invalid"""
    with Message(
            description=config.translator.translate(Translator.Text.INVALID_TESTSUITE_STUDENTS),
            format=MessageFormat.TEXT
    ):
        pass

    judge.status = config.translator.error_status(ErrorType.RUNTIME_ERROR)
    judge.accepted = False


def compile_error(judge: SimpleNamespace, config: DodonaConfig, compile_error_message: str, line_shift: int):
    """Show the students a message saying that the compilation failed"""
    print(compile_error_message)
    for error_message in compile_error_message.split('\n'):
        matches = re.search(r"submission.s:(\d+): Error: (.*)$", error_message)
        if matches:
            with Message(description=matches.group(2), format=MessageFormat.CODE):
                with Annotation(row=int(matches.group(1)) - line_shift, text=matches.group(2), type="error"):
                    pass

    judge.status = config.translator.error_status(ErrorType.COMPILATION_ERROR)
    judge.accepted = False


def invalid_evaluator_file(exception: Exception):
    """Show the teacher a message saying that their evaluator file is invalid"""
    with Message(
            permission=MessagePermission.STAFF,
            description=traceback.format_exc(),
            format=MessageFormat.CODE
    ):
        pass


def missing_evaluator_file(translator: Translator):
    """Show the teacher a message saying that the evaluator file is missing"""
    with Message(
            permission=MessagePermission.STAFF,
            description=translator.translate(Translator.Text.MISSING_EVALUATION_FILE),
            format=MessageFormat.TEXT
    ):
        pass


def missing_create_suite(translator: Translator):
    with Message(
            permission=MessagePermission.STAFF,
            description=translator.translate(Translator.Text.MISSING_CREATE_SUITE),
            format=MessageFormat.TEXT
    ):
        pass

