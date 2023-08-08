import json

from exceptions.config_exceptions import UnknownArgumentTypeError


def format_argument(argument):
    if isinstance(argument, (int, float)):
        return str(argument)
    elif isinstance(argument, bool):
        return str(argument).lower()
    elif isinstance(argument, str):
        return json.dumps(argument)
    else:
        raise UnknownArgumentTypeError(argument)


def format_arguments(arguments):
    return ', '.join(map(format_argument, arguments))

