import abc


class Chapter(abc.ABC):
    """
    A single installment of a series. Possibly the only installment.

    This is an abstract class.
    """

    @abc.abstractmethod
    def get_text(self):
        pass
