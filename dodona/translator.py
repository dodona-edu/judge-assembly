"""translate judge output towards Dodona"""

from enum import Enum, auto
from typing import Dict

from dodona.dodona_command import ErrorType


class Translator:
    """a class for translating all user feedback
    The Translator class provides translations for a set of Text
    messages and for the Dodona error types.
    """

    class Language(Enum):
        """Language"""

        EN = auto()
        NL = auto()

    class Text(Enum):
        """Text message content enum"""

        FAILED_TESTS = auto()
        CONFIG_ERROR = auto()
        UNKNOWN_ARGUMENT_TYPE = auto()
        # descriptions
        RETURN_VALUE = auto()
        MEASURED_CYCLES = auto()
        CALLING_CONVENTION_VIOLATION = auto()
        CALLING_CONVENTION_MSG = auto()
        MISSING_TEST_FUNCTION = auto()
        # normal text
        ERRORS = auto()
        WARNINGS = auto()
        LOCATED_AT = auto()
        LINE = auto()
        AT_LINE = auto()
        POSITION = auto()
        SUBMISSION = auto()

    def __init__(self, language: Language):
        self.language = language

    @classmethod
    def from_str(cls, language: str) -> "Translator":
        """created a Translator instance
        If the language is not detected correctly or not supported
        the translator defaults to English (EN).
        :param language: Dodona language string "nl" or "en"
        :return: translator
        """
        if language == "nl":
            return cls(cls.Language.NL)

        # default value is EN
        return cls(cls.Language.EN)

    def human_error(self, error: ErrorType) -> str:
        """translate an ErrorType enum into a human-readable string
        :param error: ErrorType enum
        :return: translated human-readable string
        """
        return self.error_translations[self.language][error]

    def error_status(self, error: ErrorType, **kwargs) -> Dict[str, str]:
        """translate an ErrorType enum into a status object
        :param error: ErrorType enum
        :return: Dodona status object
        """
        return {
            "enum": error,
            "human": self.human_error(error).format(**kwargs),
        }

    def translate(self, message: Text, **kwargs) -> str:
        """translate a Text enum into a string
        :param message: Text enum
        :param kwargs: parameters for message
        :return: translated text
        """
        return self.text_translations[self.language][message].format(**kwargs)

    error_translations = {
        Language.EN: {
            ErrorType.INTERNAL_ERROR: "Internal error",
            ErrorType.COMPILATION_ERROR: "The code is not valid",
            ErrorType.MEMORY_LIMIT_EXCEEDED: "Memory limit exceeded",
            ErrorType.TIME_LIMIT_EXCEEDED: "Time limit exceeded",
            ErrorType.OUTPUT_LIMIT_EXCEEDED: "Output limit exceeded",
            ErrorType.RUNTIME_ERROR: "Crashed while testing",
            ErrorType.WRONG: "Test failed",
            ErrorType.WRONG_ANSWER: "{amount} tests failed",
            ErrorType.CORRECT: "All tests succeeded",
            ErrorType.CORRECT_ANSWER: "All tests succeeded",
        },
        Language.NL: {
            ErrorType.INTERNAL_ERROR: "Interne fout",
            ErrorType.COMPILATION_ERROR: "Ongeldige code",
            ErrorType.MEMORY_LIMIT_EXCEEDED: "Geheugenlimiet overschreden",
            ErrorType.TIME_LIMIT_EXCEEDED: "Tijdslimiet overschreden",
            ErrorType.OUTPUT_LIMIT_EXCEEDED: "Outputlimiet overschreden",
            ErrorType.RUNTIME_ERROR: "Gecrasht bij testen",
            ErrorType.WRONG: "Test gefaald",
            ErrorType.WRONG_ANSWER: "{amount} testen gefaald",
            ErrorType.CORRECT: "Alle testen geslaagd",
            ErrorType.CORRECT_ANSWER: "Alle testen geslaagd",
        },
    }

    text_translations = {
        Language.EN: {
            Text.FAILED_TESTS: "{amount} test(s) failed.",
            Text.CONFIG_ERROR: "Configuration error: {msg}.",
            Text.UNKNOWN_ARGUMENT_TYPE: "Onbekend argumenttype: {type}.",
            # descriptions
            Text.RETURN_VALUE: "Return value",
            Text.MEASURED_CYCLES: "Number of clock cycles to execute your code",
            Text.CALLING_CONVENTION_VIOLATION: "Calling convention was violated",
            Text.CALLING_CONVENTION_MSG: "{msg} was/were not preserved",
            Text.MISSING_TEST_FUNCTION: "The to-be-tested function is missing (typo?).",
            # normal text
            Text.ERRORS: "Error(s)",
            Text.WARNINGS: "Warning(s)",
            Text.LOCATED_AT: "located at",
            Text.LINE: "line",
            Text.AT_LINE: "at line",
            Text.POSITION: "position",
            Text.SUBMISSION: "Submission"
        },
        Language.NL: {
            Text.FAILED_TESTS: "{amount} test(en) gefaald.",
            Text.CONFIG_ERROR: "Configuratiefout: {msg}.",
            Text.UNKNOWN_ARGUMENT_TYPE: "Unknown argument type: {ty}.",
            # descriptions
            Text.RETURN_VALUE: "Terugkeerwaarde",
            Text.MEASURED_CYCLES: "Aantal klokcycli om je code uit te voeren",
            Text.CALLING_CONVENTION_VIOLATION: "Oproepconventie werd geschonden",
            Text.CALLING_CONVENTION_MSG: "{msg} werd(en) niet behouden",
            Text.MISSING_TEST_FUNCTION: "De te testen functie werd niet gevonden (typo?).",
            # normal text
            Text.ERRORS: "Fout(en)",
            Text.WARNINGS: "Waarschuwing(en)",
            Text.LOCATED_AT: "gevonden op",
            Text.LINE: "regel",
            Text.AT_LINE: "op regel",
            Text.POSITION: "positie",
            Text.SUBMISSION: "Indiening"
        }
    }
