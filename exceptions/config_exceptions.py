class UnknownArgumentTypeError(ValueError):
    """Unknown argument type error."""

    def __init__(self, argument):
        super(ValueError, self).__init__()
        self.argument = argument

