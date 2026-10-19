import json

from exceptions.config_exceptions import UnknownArgumentTypeError


def format_argument(argument):
    if isinstance(argument, (int, float)):
        return str(argument)
    if isinstance(argument, bool):
        return str(argument).lower()
    if isinstance(argument, str):
        return json.dumps(argument)
    raise UnknownArgumentTypeError(argument)


def format_arguments(arguments):
    return ", ".join(map(format_argument, arguments))
