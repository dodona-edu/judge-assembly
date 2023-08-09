import os
import sys
from typing import List, Optional
from types import SimpleNamespace

from dodona.dodona_command import Judgement, Message, ErrorType, Tab, Context, TestCase, Test, Annotation, MessageFormat
from dodona.dodona_config import DodonaConfig, AssemblyLanguage
from dodona.translator import Translator
from exceptions.utils import InvalidTranslation
from utils.evaluation_module import EvaluationModule
from utils.file_loaders import html_loader, text_loader
from exceptions.evaluation_exceptions import ValidationError
from exceptions.evaluation_exceptions import TestRuntimeError
from validators import checks
from validators.checks import TestSuite
from utils.render_ready import prep_render
from utils.messages import invalid_suites, invalid_evaluator_file, missing_create_suite, missing_evaluator_file, no_suites_found, compile_error
from evaluation.compilation import run_compilation
from evaluation.run import run_test
import json


def main():
    """
    Main judge method
    """
    # Read config JSON from stdin
    config = DodonaConfig.from_json(sys.stdin)

    with Judgement() as judge:
        # Counter for failed tests because this judge works a bit differently
        # Allows nicer feedback on Dodona (displays amount of failed tests)
        failed_tests = 0

        # Perform sanity check
        config.sanity_check()

        # Initiate translator
        config.translator = Translator.from_str(config.natural_language)

        # Prepend the global annotation for the submission entry point
        submission_content = text_loader(config.source)
        # TODO: size will be wrong if there are multiple functions?
        # TODO: fn=... doesn't work with multiple functions?
        submission_content = f".globl {config.tested_function}\n.type {config.tested_function}, @function\n{submission_content}\n.size {config.tested_function}, .-{config.tested_function}\n"
        line_shift = 3
        submission_file = os.path.join(config.workdir, "submission.s")
        with open(submission_file, "w") as modified_submission_file:
            modified_submission_file.write(submission_content)

        # Load test plan
        # TODO: validate arg types?
        with open(os.path.join(config.resources, config.plan_name), "r") as plan_file:
            plan = json.load(plan_file, object_hook=lambda d: SimpleNamespace(**d))

        # Compile code
        try:
            test_program_path = run_compilation(config.translator, submission_file, config.judge, config.workdir, plan, config)
        except ValidationError as validation_error:
            compile_error(judge, config, validation_error.msg, line_shift)
            return

        # Run the tests
        with Tab('Feedback'):
            # Put each testcase in a separate context
            for test_id, test in enumerate(plan.tests):
                test_name = f"{config.tested_function}({', '.join(map(str, test.arguments))})"
                with Context() as test_context, TestCase(test_name, format="code") as test_case:
                    expected = str(test.expected_return_value)
                    accepted = False
                    try:
                        test_result = run_test(config.translator, config.workdir, test_program_path, test_id, test, config)
                        accepted = test_result.generated == expected
                        with Test(
                            description=config.translator.translate(Translator.Text.RETURN_VALUE),
                            expected=expected
                        ) as dodona_test:
                            dodona_test.generated = test_result.generated
                            dodona_test.accepted = accepted
                            dodona_test.status = {"enum": ErrorType.CORRECT if accepted else ErrorType.WRONG}
                    except TestRuntimeError as e:
                        with Message(str(e)):
                            pass

                    test_context.accepted = accepted
                    test_case.accepted = accepted
                    if not accepted:
                        failed_tests += 1

        status = ErrorType.CORRECT if failed_tests == 0 else ErrorType.WRONG
        judge.status = config.translator.error_status(status, amount=failed_tests)


if __name__ == "__main__":
    main()
