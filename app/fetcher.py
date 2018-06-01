from app.archive import Archive
from app.models.story import Story
from app import fetchers


class Fetcher:
    """Calls an appropriate fetcher and returns a Story."""

    def fetch_from_reddit(self, url_or_id):
        """Fetch story from reddit by following 'next' links."""
        reddit_id = url_or_id  # TODO

        reddit_fetcher = fetchers.Reddit()
        chapters = [submission.get_text()
                    for submission
                    in reddit_fetcher.submissions_following_next_links(reddit_id)]

        title = chapters[0].title  # TODO
        story = Story(title=title, chapters=chapters)

        Archive.store(story)

        return story

    def fetch_from_archive(self, id):
        # Note that ID can be partial, as long as it is unique
        return Archive.get(id)
