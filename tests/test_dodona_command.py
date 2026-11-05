"""Unit tests for the Dodona commands."""

import contextlib
import io
import json
import unittest

from dodona.dodona_command import (
    Annotation,
    Context,
    ErrorType,
    Judgement,
    Message,
    MessageFormat,
    MessagePermission,
    Tab,
    Test,
    TestCase,
)


def fragments(output: str) -> list[dict]:
    decoder = json.JSONDecoder()
    result = []
    position = 0
    while position < len(output):
        if output[position].isspace():
            position += 1
            continue
        fragment, position = decoder.raw_decode(output, position)
        result.append(fragment)
    return result


def make_message(*args, **kwargs) -> Message:
    return Message(*args, **kwargs)


def fail_inside_test_case():
    with TestCase(description="failing"):
        message = "boom"
        raise ValueError(message)


class EnumStrTest(unittest.TestCase):
    def test_str_and_format_give_the_value(self):
        for enum in (ErrorType, MessagePermission, MessageFormat):
            for member in enum:
                with self.subTest(member=member):
                    self.assertEqual(str(member), member.value)
                    self.assertEqual(f"{member}", member.value)


class CommandOutputTest(unittest.TestCase):
    def test_nested_commands_print_start_and_close_messages(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), Judgement() as judgement:
            with Tab("tab") as tab:
                with Context() as context:
                    with TestCase(description="case", format=MessageFormat.CODE) as test_case:
                        with Test("check", "1") as test:
                            with Message("plain"):
                                pass
                            with Message(description="coded", format=MessageFormat.CODE):
                                pass
                            with Annotation(1, "note", type="error"):
                                pass
                            test.generated = "2"
                            test.accepted = False
                            test.status = {"enum": ErrorType.WRONG, "human": "Wrong"}
                        test_case.accepted = False
                    context.accepted = False
                tab.badgeCount = 1
            judgement.accepted = False
            judgement.status = {"enum": ErrorType.WRONG, "human": "Wrong"}

        wrong = {"enum": "wrong", "human": "Wrong"}
        self.assertEqual(
            fragments(output.getvalue()),
            [
                {"command": "start-judgement"},
                {"command": "start-tab", "title": "tab"},
                {"command": "start-context"},
                {"command": "start-testcase", "description": {"description": "case", "format": "code"}},
                {"command": "start-test", "description": "check", "expected": "1"},
                {"command": "append-message", "message": "plain"},
                {"command": "append-message", "message": {"description": "coded", "format": "code"}},
                {"command": "annotate-code", "row": 1, "text": "note", "type": "error"},
                {"command": "close-test", "generated": "2", "accepted": False, "status": wrong},
                {"command": "close-testcase", "accepted": False},
                {"command": "close-context", "accepted": False},
                {"command": "close-tab", "badgeCount": 1},
                {"command": "close-judgement", "accepted": False, "status": wrong},
            ],
        )

    def test_json_format_is_indented_and_sorted(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), Tab("tab"):
            pass
        self.assertEqual(
            output.getvalue(),
            '{\n "command": "start-tab",\n "title": "tab"\n}\n{\n "command": "close-tab"\n}\n',
        )


class MessageArgumentsTest(unittest.TestCase):
    def test_positional_argument_with_keywords_is_rejected(self):
        with self.assertRaises(TypeError):
            make_message("text", format=MessageFormat.CODE)

    def test_multiple_positional_arguments_are_rejected(self):
        with self.assertRaises(TypeError):
            make_message("one", "two")


class ExceptionPropagationTest(unittest.TestCase):
    def test_exception_propagates_and_close_message_is_printed(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), self.assertRaises(ValueError):
            fail_inside_test_case()
        self.assertEqual(
            [fragment["command"] for fragment in fragments(output.getvalue())],
            ["start-testcase", "close-testcase"],
        )


if __name__ == "__main__":
    unittest.main()
