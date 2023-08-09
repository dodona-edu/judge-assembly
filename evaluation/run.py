from types import SimpleNamespace
from dodona.dodona_config import DodonaConfig
from dodona.translator import Translator
from exceptions.evaluation_exceptions import TestRuntimeError
from dataclasses import dataclass
from os import path
import subprocess


@dataclass
class TestResult:
    generated: str


# TODO: I guess we should cleanup the arguments as we're passing the config anyway (idem for compilation)
def run_test(translator: Translator, workdir_path: str, test_program_path: str, test_id: int, config: DodonaConfig):
    # TODO: option to toggle on/off the time measurements?
    # TODO: option to choose your desired cycles for memory vs non-memory?

    command = [test_program_path, str(test_id)]

    if config.measure_performance:
        # TODO: depends on arch
        command = ["valgrind", "--tool=cachegrind", "--cache-sim=yes", "--log-file=/dev/null", "--cachegrind-out-file=timing.out", "--quiet"] + command

    # TODO: depends on arch
    run_result = subprocess.run(
        command,
        cwd=workdir_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    if run_result.returncode != 0:
        raise TestRuntimeError(translator, 0, -1)

    if config.measure_performance:
        target = f"fn={config.tested_function}\n"
        instruction_count = 0
        data_read_count = 0
        data_write_count = 0
        # Find time measurement line for our tested function
        with open(path.join(workdir_path, "timing.out")) as cachegrind_out_file:
            for line in cachegrind_out_file:
                if line == target:
                    line = cachegrind_out_file.readline()
                    # Format: Ir I1mr ILmr Dr D1mr DLmr Dw D1mw DLmw 
                    parts = line.split(' ')
                    instruction_count = int(parts[1])
                    data_read_count = int(parts[4])
                    data_write_count = int(parts[7])
                    break
        #print(instruction_count, data_read_count, data_write_count)

    return TestResult(generated=run_result.stdout)
