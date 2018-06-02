class AmbiguousIdError(Exception):
    """An ID can't be mapped to a reddit object—they're all six characters long"""
    pass


class UnknownModeError(Exception):
    """The user specified an unrecognized fetch mode"""
    pass
