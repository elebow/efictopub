from app.archiver import Archive
from app.chapter import Chapter
from app.story import Story


class Controller:
    """Uses RedditFetcher and other classes to build Stories."""

    def fetch_from_reddit_next(self, reddit, url_or_id):
        """Fetch story from reddit by following 'next' links."""
        reddit_id = url_or_id  # TODO

        submissions = reddit.submissions_following_next_links(reddit_id)
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
        pass

