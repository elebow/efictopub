class AmbiguousIdError(Exception):
    """Raised when an ID can't be mapped to a reddit object—they're all six characters long"""
    pass
