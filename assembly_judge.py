import os
import sys
from typing import List, Optional
from types import SimpleNamespace

from dodona.dodona_command import Judgement, Message, ErrorType, Tab, Context, TestCase, Test, MessageFormat
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
        submission_content = f".globl {config.tested_function}\n.type {config.tested_function}, @function\n{submission_content}\n.size {config.tested_function}, .-{config.tested_function}"
        submission_file = os.path.join(config.workdir, "submission.s")
        with open(submission_file, "w") as modified_submission_file:
            modified_submission_file.write(submission_content)

        # Load test plan
        # TODO: validate arg types?
        #raise Exception(str(config))
        import time
        time.sleep(9000)
        with open(os.path.join(config.resources, config.plan_name), "r") as plan_file:
            plan = json.load(plan_file, object_hook=lambda d: SimpleNamespace(**d))

        # Compile code
        try:
            test_program_path = run_compilation(config.translator, submission_file, config.judge, config.workdir, plan, config)
        except ValidationError as validation_error:
            compile_error(judge, config, validation_error.msg)
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
                    except TestRuntimeError as e:
                        # TODO
                        print(e)

                    test_context.accepted = accepted
                    test_case.accepted = accepted
                    if not accepted:
                        failed_tests += 1

                    with Test(
                        description=config.translator.translate(Translator.Text.RETURN_VALUE),
                        generated=test_result.generated,
                        expected=expected
                    ) as dodona_test:
                        dodona_test.accepted = accepted
                        dodona_test.status = {"enum": ErrorType.CORRECT if accepted else ErrorType.WRONG}

        status = ErrorType.CORRECT if failed_tests == 0 else ErrorType.WRONG
        judge.status = config.translator.error_status(status, amount=failed_tests)

        return

        # Compile evaluator code & create test suites
        # If anything goes wrong, show a detailed error message to the teacher
        # and a short message to the student
        try:
            evaluator: Optional[EvaluationModule] = EvaluationModule.build(config)
            if evaluator is not None:
                test_suites: List[TestSuite] = evaluator.create_suites(submitted_content)
            else:
                solution = html_loader(os.path.join(config.resources, "./solution.html"))
                if not solution:
                    missing_evaluator_file(config.translator)
                    invalid_suites(judge, config)
                    return
                # compare(sol, html_content, config.translator)
                suite = checks._CompareSuite(submitted_content, solution, config, check_recommended=getattr(config, "recommended", True))
                test_suites = [suite]
        except FileNotFoundError:
            # solution.html is missing
            missing_evaluator_file(config.translator)
            invalid_suites(judge, config)
            return
        except NotImplementedError:
            # Evaluator.py file doesn't implement create_suites
            missing_create_suite(config.translator)
            invalid_suites(judge, config)
            return
        except Exception as e:
            # Something else went wrong
            invalid_evaluator_file(e)
            invalid_suites(judge, config)
            return

        # No suites found, either no return or an empty list
        if test_suites is None or not test_suites:
            no_suites_found(config.translator)
            invalid_suites(judge, config)
            return

        # Has HTML been validated at least once?
        # Same HTML is used every time so once is enough
        html_validated: bool = False
        css_validated: bool = False
        aborted: bool = False

        # Run all test suites
        for suite in test_suites:
            suite.create_validator(config)

            with Tab(suite.name):
                try:
                    failed_tests += suite.evaluate(config.translator)
                except InvalidTranslation:
                    # One of the translations was invalid
                    invalid_suites(judge, config)

                    aborted = True
                    continue

            # This suite validated the HTML
            if suite.html_is_valid():
                html_validated = True

            # This suite validated the CSS
            if suite.css_is_valid():
                css_validated = True

        # Only render out valid HTML on Dodona
        if html_validated:
            title, html = prep_render(submitted_content, render_css=css_validated)
            with Tab(f"Rendered{f': {title}' if title else ''}"):
                with Message(format=MessageFormat.HTML, description=html):
                    pass

        if aborted:
            judge.status = config.translator.error_status(ErrorType.RUNTIME_ERROR)
            judge.accepted = False
        else:
            status = ErrorType.CORRECT_ANSWER if failed_tests == 0 else ErrorType.WRONG if failed_tests == 1 else ErrorType.WRONG_ANSWER
            judge.status = config.translator.error_status(status, amount=failed_tests)


if __name__ == "__main__":
    main()
