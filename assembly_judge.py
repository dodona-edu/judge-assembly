import os
import sys
from types import SimpleNamespace

from dodona.dodona_command import Judgement, Message, ErrorType, Tab, Context, TestCase, MessageFormat
from dodona.dodona_config import DodonaConfig, AssemblyLanguage
from dodona.translator import Translator
from evaluation.arguments import format_arguments
from exceptions.config_exceptions import UnknownArgumentTypeError
from utils.file_loaders import text_loader
from exceptions.evaluation_exceptions import ValidationError, TestRuntimeError
from utils.messages import compile_error, report_test, config_error, unknown_argument_type
from evaluation.compilation import run_compilation
from evaluation.run import run_test
import json


def amend_submission(config: DodonaConfig):
    """
    Adds the assembly directives necessary for generating the debug and linker information used in later staged.
    """

    submission_content = text_loader(config.source)

    modified_submission_content = []

    if config.assembly == AssemblyLanguage.X86_32_INTEL or config.assembly == AssemblyLanguage.X86_64_INTEL:
        modified_submission_content.append(".intel_syntax noprefix")

    if config.assembly == AssemblyLanguage.ARM_32 or config.assembly == AssemblyLanguage.ARM_64:
        global_directive = "global"
        function_type = "%function"
    else:
        global_directive = "globl"
        function_type = "@function"

    # Note: we surround everything with .type & .size, as if it is one function, such that all the student's
    #       code will be under a single entry in the Valgrind output (as if it were one function).
    modified_submission_content.extend((
        f".{global_directive} {config.tested_function}",
        f".type {config.tested_function}, {function_type}",
    ))
    line_shift = len(modified_submission_content) + 1
    modified_submission_content.extend((
        submission_content,
        f".size {config.tested_function}, .-{config.tested_function}\n", # newline to prevent warning
    ))

    submission_file = os.path.join(config.workdir, "submission.s")
    with open(submission_file, "w") as modified_submission_file:
        modified_submission_file.write("\n".join(modified_submission_content))

    return submission_file, line_shift


def main():
    """
    Main judge method
    """
    # Read config JSON from stdin
    config = DodonaConfig.from_json(sys.stdin)

    with Judgement() as judge:
        # Perform sanity check
        config.sanity_check()

        # Initiate translator
        config.translator = Translator.from_str(config.natural_language)

        try:
            config.process_judge_specific_options()
        except ValueError as e:
            config_error(judge, config.translator, str(e))
            return

        # Counter for failed tests because this judge works a bit differently
        # Allows nicer feedback on Dodona (displays amount of failed tests)
        failed_tests = 0

        submission_file, line_shift = amend_submission(config)

        # Load test plan
        with open(os.path.join(config.resources, config.plan_name), "r") as plan_file:
            plan = json.load(plan_file, object_hook=lambda d: SimpleNamespace(**d))

        # Compile code
        try:
            test_program_path = run_compilation(config, plan, submission_file)
        except ValidationError as validation_error:
            compile_error(judge, config, validation_error.msg, line_shift)
            return

        # Run the tests
        with Tab('Feedback'):
            # Put each testcase in a separate context
            for test_id, test in enumerate(plan.tests):
                try:
                    formatted_arguments = format_arguments(test.arguments)
                except UnknownArgumentTypeError as e:
                    unknown_argument_type(judge, config.translator, e.argument)
                    continue
                test_name = f"{config.tested_function}({formatted_arguments})"
                with Context() as test_context, TestCase(test_name, format=MessageFormat.CODE) as test_case:
                    expected = str(test.expected_return_value)
                    accepted = False
                    try:
                        test_result = run_test(config.translator, test_program_path, test_id, config)
                        accepted = test_result.generated == expected

                        # Return value test
                        report_test(
                            config.translator.translate(Translator.Text.RETURN_VALUE),
                            expected,
                            test_result.generated,
                            accepted,
                        )

                        # Time measurement test
                        if test_result.performance:
                            # Combine the performance counters into a total number of cycles
                            simulated_total_cycles = config.performance_cycle_factor_instructions * test_result.performance.instruction_count \
                                                     + config.performance_cycle_factor_data_reads * test_result.performance.data_read_count \
                                                     + config.performance_cycle_factor_data_writes * test_result.performance.data_write_count
                            accepted_cycles = simulated_total_cycles <= test.max_cycles
                            accepted = accepted and accepted_cycles
                            report_test(
                                config.translator.translate(Translator.Text.MEASURED_CYCLES),
                                config.translator.translate(Translator.Text.EXECUTED_IN_CYCLES, msg=f"<= {str(test.max_cycles)}"),
                                config.translator.translate(Translator.Text.EXECUTED_IN_CYCLES, msg=str(simulated_total_cycles)),
                                accepted_cycles,
                            )

                        # Calling convention test
                        if test_result.calling_convention_error is not None:
                            accepted_calling_convention = not bool(test_result.calling_convention_error)
                            if not accepted_calling_convention:
                                accepted = False
                                report_test(
                                    config.translator.translate(Translator.Text.CALLING_CONVENTION_VIOLATION),
                                    "",
                                    config.translator.translate(Translator.Text.CALLING_CONVENTION_MSG, msg=test_result.calling_convention_error),
                                    accepted_calling_convention,
                                )
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
