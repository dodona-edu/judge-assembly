from typing import Optional
from dodona.dodona_config import DodonaConfig
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


def run_test(translator: Translator, test_program_path: str, test_id: int, config: DodonaConfig):
    command = [test_program_path, str(test_id)]

    if config.measure_performance:
        # TODO: depends on arch
        command = ["valgrind",
                   "--tool=cachegrind",
                   "--cache-sim=yes",
                   "--log-file=/dev/null",
                   "--cachegrind-out-file=timing.out",
                   "--quiet"] + command

    # TODO: depends on arch
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
