from app.archive import Archive
from app.models.story import Story
from app import fetchers


class Fetcher:
    """Calls an appropriate fetcher and returns a Story."""

    def fetch_from_reddit_next(self, url_or_id):
        """Fetch story from reddit by following 'next' links."""
        chapters = fetchers.Reddit().submissions_following_next_links(url_or_id)
        story = Story(chapters=chapters)

        Archive.store(story)

        return story

    def fetch_from_reddit_author():
        pass

    def fetch_from_reddit_mentions():
        pass

    def fetch_from_archive(self, id):
        """
        Fetch a story from the archive.
        Note that ID can be partial, as long as it is unique.
        """
        return Archive.get(id)
