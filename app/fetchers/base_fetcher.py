import abc


class BaseFetcher(abc.ABC):
    @abc.abstractmethod
    def fetch_story(self):
        pass

    @abc.abstractmethod
    def fetch_chapters(self):
        pass
