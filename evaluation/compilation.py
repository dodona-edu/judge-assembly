from dodona.dodona_config import AssemblyLanguage, DodonaConfig
from exceptions.evaluation_exceptions import ValidationError
from mako.template import Template
from types import SimpleNamespace
from os import path
import subprocess

from utils.file_loaders import text_loader


# TODO: documentation


def determine_compile_command(assembly_language: AssemblyLanguage):
    compile_options = ["-std=c11", "-O1", "-fno-pie", "-no-pie"]
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


def write_main_file(config: DodonaConfig, plan: SimpleNamespace):
    template = Template(text_loader(path.join(config.judge, "templates/main.c.mako")))

    with open(path.join(config.workdir, "main.c"), "w") as main_file:
        main_file.write(template.render(
            tested_function=config.tested_function,
            test_iterations=config.test_iterations,
            plan=plan
        ))


def run_compilation(config: DodonaConfig, plan: SimpleNamespace, submission_file_path: str) -> str:
    write_main_file(config, plan)

    compile_command, compile_options = determine_compile_command(config.assembly)
    compile_options += [path.join(config.workdir, "main.c"), "-o", "program", submission_file_path]

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
