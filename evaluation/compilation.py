from dodona.dodona_config import AssemblyLanguage, JudgeSpecificConfigOptions
from exceptions.evaluation_exceptions import ValidationError
from dodona.translator import Translator
from mako.template import Template
from types import SimpleNamespace
from os import path
import subprocess

# TODO: documentation


def determine_compile_command(assembly_language: AssemblyLanguage):
    compile_options = ["-std=c11", "-O1"]
    match assembly_language:
        case AssemblyLanguage.X86_32_ATT:
            compile_command = "gcc"
            compile_options.append("-m32")
        case AssemblyLanguage.X86_32_INTEL:
            compile_command = "gcc"
            compile_options.extend(("-m32", "-masm=intel"))
        case AssemblyLanguage.X86_64_ATT:
            compile_command = "gcc"
        case AssemblyLanguage.X86_64_INTEL:
            compile_command = "gcc"
            compile_options.append("-masm=intel")
        # TODO: ARM
        case _:
            raise NotImplementedError(f"Assembly language {assembly_language} is not implemented")
    return compile_command, compile_options


def write_main_file(workdir_path: str, tested_function: str, test_iterations: int, plan: SimpleNamespace):
    with open(path.join(workdir_path, "main.c.mako"), "r") as template_file:
        template = Template(template_file.read())

    with open(path.join(workdir_path, "main.c"), "w") as main_file:
        main_file.write(template.render(
            tested_function = tested_function,
            test_iterations = test_iterations,
            plan = plan
        ))


def run_compilation(translator: Translator, source_file_name: str, workdir_path: str, plan: SimpleNamespace, options: JudgeSpecificConfigOptions) -> str:
    write_main_file(workdir_path, options.tested_function, options.test_iterations, plan)

    compile_command, compile_options = determine_compile_command(options.assembly)
    compile_options += [path.join(workdir_path, "main.c"), "-o", "program", source_file_name]

    compile_result = subprocess.run(
        [compile_command] + compile_options,
        cwd=workdir_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    if compile_result.returncode != 0:
        # TODO: more specific exception
        raise ValidationError(translator, compile_result.stderr, 0, 0)

    return path.join(workdir_path, "program")
