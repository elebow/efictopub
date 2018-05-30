from app.archiver import Archive
from app.models.chapter import Chapter
from app.models.story import Story
from app import fetchers


class Controller:
    """Uses RedditFetcher and other classes to build Stories."""

    def fetch_from_reddit(self, url_or_id):
        """Fetch story from reddit by following 'next' links."""
        reddit_id = url_or_id  # TODO

        reddit_fetcher = fetchers.Reddit()
        submissions = reddit_fetcher.submissions_following_next_links(reddit_id)
        chapters = [Chapter(submission) for submission in submissions]

        title = chapters[0].title  # TODO
        story = Story(title=title, chapters=chapters)

        Archive.store(story)

        return story

    def fetch_from_archive(self, key):
        #   TODO make the key in the archive just the reddit_id, so we can look them up with just that
        #       though the filenames would still be longer, for human-readability
        # get from archive
        # return Story
        story = Archive.get(key)

