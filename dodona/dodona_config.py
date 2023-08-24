"""Dodona Judge configuration"""

import json
import os
from types import SimpleNamespace
from typing import TextIO
from enum import Enum


class AssemblyLanguage(Enum):
    X86_32_ATT = "x86-32-at&t"
    X86_32_INTEL = "x86-32-intel"
    X86_64_ATT = "x86-64-at&t"
    X86_64_INTEL = "x86-64-intel"
    ARM_32 = "arm-32"
    ARM_64 = "arm-64"


# pylint: disable=too-many-instance-attributes
class DodonaConfig(SimpleNamespace):
    """a class for containing all Dodona Judge configuration
    Attributes:
        memory_limit:                           An integer, the memory limit in bytes. The docker container
                                                will be killed when it's internal processes exceed this limit. The judge
                                                can use this value to cut of the tests, so he might be able to give more
                                                feedback to the student than just the default "Memory limit exceeded."
        time_limit:                             An integer, the time limit in seconds. Just like the memory
                                                limit, the docker will be killed if the judging takes longer. Can be used
                                                to for instance specify the specific test case the limit would be exceeded,
                                                instead of just "Time limit exceeded."
        programming_language:                   The full name (e.g. "python", "haskell") of the
                                                programming language the student submitted his code for.
        natural_language:                       The natural language (e.g. "nl", "en") in which the
                                                student submitted his code.
        resources:                              Full path to a directory containing the resources for the evaluation.
                                                This is the "evaluation" directory of an exercise.
        source:                                 Full path to a file containing the code the user submitted.
        workdir:                                Full path to the directory in which all user code should be executed.
        plan_name:                              The test evaluation plan.
        assembly:                               The assembly language used by the exercise.
        tested_function:                        The name of the function that will be tested.
        tested_arguments:                       An array of argument types for the tested function.
        test_iterations:                        How many times each test will be run.
        measure_performance:                    Measure performance in cycles.
        performance_cycle_factor_instructions:  The multiplication factor to use in computing the cycles for the instructions.
        performance_cycle_factor_data_reads:    The multiplication factor to use in computing the cycles for the data reads.
        performance_cycle_factor_data_writes:   The multiplication factor to use in computing the cycles for the data writes.
        check_calling_convention:               Whether the calling convention should be checked.
    """

    def __init__(self, **kwargs):
        """store all parameters & set correct type for 'known' Dodona judge configuration fields
        :param kwargs: the named parameters in the form of a dict
        """
        super().__init__(**kwargs)
        self.memory_limit = int(self.memory_limit)
        self.time_limit = int(self.time_limit)
        self.programming_language = str(self.programming_language)
        self.natural_language = str(self.natural_language)
        self.resources = str(self.resources)
        self.source = str(self.source)
        self.workdir = str(self.workdir)
        self.plan_name = str(self.plan_name)

    def process_judge_specific_options(self):
        self.assembly = AssemblyLanguage(self.assembly)
        self.tested_function = str(self.tested_function)
        self.test_iterations = int(self.test_iterations)
        self.measure_performance = bool(self.measure_performance)
        if self.measure_performance:
            self.performance_cycle_factor_instructions = int(self.performance_cycle_factor_instructions)
            self.performance_cycle_factor_data_reads = int(self.performance_cycle_factor_data_reads)
            self.performance_cycle_factor_data_writes = int(self.performance_cycle_factor_data_writes)
        self.check_calling_convention = bool(self.check_calling_convention)

    @classmethod
    def from_json(cls, json_file: TextIO) -> "DodonaConfig":
        """decode json filestream into a DodonaConfig object
        :param json_file: input json-encoded filestream
        :return: decoded Dodona judge config
        """
        simple = json.load(json_file, object_hook=lambda d: SimpleNamespace(**d))
        return cls(**simple.__dict__)

    def sanity_check(self) -> None:
        """perform sanity checks
        This function checks if the Python file is executed correctly. The current working dir
        should be the same directory that is passed as the 'workdir' property in the Dodona config.
        Also, this Python file (and all other Python judge files) should be located in the 'judge' dir.
        """
        # Make sure that the current working dir is the workdir
        cwd = os.getcwd()
        assert os.path.realpath(cwd) == os.path.realpath(self.workdir)

        # Make sure that this file is located right below the judge folder
        script_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        assert os.path.realpath(script_path) == os.path.realpath(
            self.judge), f"{os.path.realpath(script_path)} | {os.path.realpath(self.judge)}"
