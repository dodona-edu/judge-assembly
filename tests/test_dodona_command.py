"""Unit tests for the Dodona command enums."""

import unittest

from dodona.dodona_command import AnnotationSeverity, ErrorType, MessageFormat, MessagePermission


class EnumStrTest(unittest.TestCase):
    def test_str_and_format_give_the_value(self):
        for enum in (ErrorType, MessagePermission, MessageFormat, AnnotationSeverity):
            for member in enum:
                with self.subTest(member=member):
                    self.assertEqual(str(member), member.value)
                    self.assertEqual(f"{member}", member.value)


if __name__ == "__main__":
    unittest.main()
