import json

from exceptions.config_exceptions import UnknownArgumentTypeError


def format_argument(argument):
    # C11 has no true or false without stdbool.h, and bool is a subclass of int.
    if isinstance(argument, bool):
        return str(int(argument))
    if isinstance(argument, (int, float)):
        return str(argument)
    if isinstance(argument, str):
        return json.dumps(argument)
    raise UnknownArgumentTypeError(argument)


def format_arguments(arguments):
    return ", ".join(map(format_argument, arguments))
