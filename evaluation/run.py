from typing import Optional
from dodona.dodona_config import DodonaConfig, AssemblyLanguage
from dodona.translator import Translator
from exceptions.evaluation_exceptions import TestRuntimeError
from dataclasses import dataclass
from os import path
import subprocess


@dataclass
class TestPerformance:
    instruction_count: int
    data_read_count: int
    data_write_count: int


@dataclass
class TestResult:
    generated: str
    performance: Optional[TestPerformance]


def determine_emulator(assembly_language: AssemblyLanguage):
    match assembly_language:
        case AssemblyLanguage.ARM_32:
            return "qemu-arm"
        case AssemblyLanguage.ARM_64:
            return "qemu-aarch64"


def determine_valgrind(assembly_language: AssemblyLanguage):
    match assembly_language:
        case AssemblyLanguage.ARM_32:
            return "/opt/valgrind-arm32/bin/valgrind"
        case AssemblyLanguage.ARM_64:
            return "/opt/valgrind-aarch64/bin/valgrind"
        case _:
            return "valgrind"


def run_test(translator: Translator, test_program_path: str, test_id: int, config: DodonaConfig):
    command = [test_program_path, str(test_id)]

    # May need an emulator depending on the architecture
    emulator = determine_emulator(config.assembly)
    if emulator:
        command = [emulator, *command]

    if config.measure_performance:
        command = [determine_valgrind(config.assembly),
                   "--tool=cachegrind",
                   "--cache-sim=yes",
                   "--log-file=/dev/null",
                   "--cachegrind-out-file=timing.out",
                   "--quiet"] + command

    run_result = subprocess.run(
        command,
        cwd=config.workdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    if run_result.returncode != 0:
        raise TestRuntimeError(translator, 0, -1)

    performance = None
    if config.measure_performance:
        target = f"fn={config.tested_function}\n"
        # Find time measurement line for our tested function
        with open(path.join(config.workdir, "timing.out")) as cachegrind_out_file:
            for line in cachegrind_out_file:
                if line == target:
                    line = cachegrind_out_file.readline()
                    # Format: Ir I1mr ILmr Dr D1mr DLmr Dw D1mw DLmw 
                    parts = line.split(' ')
                    performance = TestPerformance(
                        instruction_count=int(parts[1]),
                        data_read_count=int(parts[4]),
                        data_write_count=int(parts[7])
                    )
                    break

    return TestResult(generated=run_result.stdout, performance=performance)
