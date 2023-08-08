from dodona.dodona_config import AssemblyLanguage, DodonaConfig
from evaluation.arguments import format_arguments
from exceptions.evaluation_exceptions import ValidationError
from mako.template import Template
from types import SimpleNamespace
from os import path
import subprocess
import random

from utils.file_loaders import text_loader


def determine_compile_command_and_options(assembly_language: AssemblyLanguage):
    compile_options = ["-std=c11", "-O1", "-no-pie", "-fno-pie", "-fno-stack-protector"]
    match assembly_language:
        case AssemblyLanguage.X86_32_ATT:
            compile_command = "gcc"
            compile_options.append("-m32")
        case AssemblyLanguage.X86_32_INTEL:
            compile_command = "gcc"
            compile_options.append("-m32")
        case AssemblyLanguage.X86_64_ATT:
            compile_command = "gcc"
        case AssemblyLanguage.X86_64_INTEL:
            compile_command = "gcc"
        case AssemblyLanguage.ARM_32:
            compile_command = "arm-linux-gnueabihf-gcc"
            compile_options.append("-static")
        case AssemblyLanguage.ARM_64:
            compile_command = "aarch64-linux-gnu-gcc"
            compile_options.append("-static")
        case _:
            raise NotImplementedError(f"Assembly language {assembly_language} is not implemented")
    return compile_command, compile_options


def random_magic_number_generator():
    return random.randint(-2 ** 63, 2 ** 63 - 1)


def write_main_file(config: DodonaConfig, plan: SimpleNamespace):
    """Writes the main.c file responsible as a wrapper for the submission code."""
    template = Template(text_loader(path.join(config.judge, "templates/main.c.mako")))

    with open(path.join(config.workdir, "main.c"), "w") as main_file:
        main_file.write(template.render(
            tested_function=config.tested_function,
            tested_arguments=config.tested_arguments,
            test_iterations=config.test_iterations,
            format_arguments=format_arguments,
            random_magic_number_generator=random_magic_number_generator,
            check_calling_convention=config.check_calling_convention,
            plan=plan
        ))


def run_compilation(config: DodonaConfig, plan: SimpleNamespace, submission_file_path: str) -> str:
    """Writes the necessary files for compilation and invokes the (C) compiler."""
    write_main_file(config, plan)

    compile_command, compile_options = determine_compile_command_and_options(config.assembly)
    compile_options += [submission_file_path, path.join(config.workdir, "main.c"), "-o", "program"]

    compile_result = subprocess.run(
        [compile_command] + compile_options,
        cwd=config.workdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    if compile_result.returncode != 0:
        raise ValidationError(config.translator, compile_result.stderr, 0, -1)

    return path.join(config.workdir, "program")
