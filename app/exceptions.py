class AmbiguousArchiveIdError(Exception):
    """The specified partial id matches more than one archived story"""

    def __init__(self, bad_id):
        self.message = bad_id


class AmbiguousIdError(Exception):
    """An ID can't be mapped to a reddit object—they're all six characters long"""
    pass


class AmbiguousNextError(Exception):
    """A submission has more than one "next" link, so we don't know which one to follow."""
    pass

class NoArchivedStoryError(Exception):
    """The specified id or file does not match any archived story"""

    def __init__(self, bad_id_or_file):
        self.bad_id_or_file = bad_id_or_file


class UnknownFetcherError(Exception):
    """The user specified an unrecognized fetcher"""
    pass
