class AmbiguousIdError(Exception):
    """An ID can't be mapped to a reddit object—they're all six characters long"""
    pass


class AmbiguousNextError(Exception):
    """A submission has more than one "next" link, so we don't know which one to follow."""
    pass


class UnknownModeError(Exception):
    """The user specified an unrecognized fetch mode"""
    pass
