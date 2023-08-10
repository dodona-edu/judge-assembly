from dodona.dodona_config import AssemblyLanguage, DodonaConfig
from exceptions.evaluation_exceptions import ValidationError
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


def write_main_file(judge_path: str, workdir_path: str, tested_function: str, test_iterations: int,
                    plan: SimpleNamespace):
    with open(path.join(judge_path, "templates/main.c.mako"), "r") as template_file:
        template = Template(template_file.read())

    with open(path.join(workdir_path, "main.c"), "w") as main_file:
        main_file.write(template.render(
            tested_function=tested_function,
            test_iterations=test_iterations,
            plan=plan
        ))


def run_compilation(config: DodonaConfig, plan: SimpleNamespace) -> str:
    write_main_file(config.judge, config.workdir, config.tested_function, config.test_iterations, plan)

    compile_command, compile_options = determine_compile_command(config.assembly)
    compile_options += [path.join(config.workdir, "main.c"), "-o", "program", config.source]

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
