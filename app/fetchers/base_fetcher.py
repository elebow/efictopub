import abc


class BaseFetcher(abc.ABC):
    @abc.abstractmethod
    def fetch_chapters(self):
        pass
