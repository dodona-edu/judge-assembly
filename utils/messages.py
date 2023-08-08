from types import SimpleNamespace

from dodona.dodona_command import Message, MessageFormat, ErrorType, Annotation, Test, MessagePermission
from dodona.dodona_config import DodonaConfig
import re

from dodona.translator import Translator


def compile_error(judge: SimpleNamespace, config: DodonaConfig, compile_error_message: str, line_shift: int):
    """Show the students a message saying that the compilation failed"""
    for error_message in compile_error_message.split('\n'):
        if "Error: .size expression" in error_message:
            # Directive error: function not found, hence the size calculation fails
            with Message(
                    description=config.translator.translate(Translator.Text.MISSING_TEST_FUNCTION),
                    format=MessageFormat.TEXT
            ):
                pass
        else:
            # Code error
            matches = re.search(r"submission.s:(\d+): Error: (.*)$", error_message)
            if matches:
                with Message(description=matches.group(2), format=MessageFormat.CODE):
                    with Annotation(row=int(matches.group(1)) - line_shift, text=matches.group(2), type="error"):
                        pass
    else:
        # Every other error passed as-is
        with Message(
                description=compile_error_message,
                format=MessageFormat.TEXT
        ):
            pass

    judge.status = config.translator.error_status(ErrorType.COMPILATION_ERROR)
    judge.accepted = False


def report_test(description: str, expected: str, generated: str, accepted: bool):
    """Report test results to the student"""
    with Test(
            description=description,
            expected=expected,
    ) as dodona_test:
        dodona_test.generated = generated
        dodona_test.accepted = accepted
        dodona_test.status = {"enum": ErrorType.CORRECT if accepted else ErrorType.WRONG}


def config_error(judge: SimpleNamespace, translator: Translator, msg: str):
    """Show the teacher a configuration error"""
    with Message(
            permission=MessagePermission.STAFF,
            description=translator.translate(Translator.Text.CONFIG_ERROR, msg=msg),
            format=MessageFormat.TEXT
    ):
        pass

    judge.status = translator.error_status(ErrorType.INTERNAL_ERROR)


def unknown_argument_type(judge: SimpleNamespace, translator: Translator, ty: str):
    """Show the teacher an unknown argument type error"""
    with Message(
            permission=MessagePermission.STAFF,
            description=translator.translate(Translator.Text.UNKNOWN_ARGUMENT_TYPE, ty=ty),
            format=MessageFormat.TEXT
    ):
        pass

    judge.status = translator.error_status(ErrorType.INTERNAL_ERROR)
