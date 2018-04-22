import praw


class SubmissionCollector:
    def __init__(self, *, app, secret, user_agent):
        self.reddit = praw.Reddit(client_id=app, client_secret=secret, user_agent=user_agent)

    def all_submissions_by_author_name(self, author_name):
        author = self.reddit.redditor(author_name)
        return [self.submission_details(subm) for subm in author.submissions.new(limit=3)]

    def all_submissions_in_list_of_ids(self, id_list):
        # TODO
        pass

    def all_submissions_mentioned_in_reddit_thing(self, thing_id):
        # TODO
        pass

    def all_submissions_mentioned_in_reddit_wiki_page(self, page):
        # TODO
        pass

    def all_submissions_following_next_links(self, start_subm):
        pass

    def comment_chain_ending_with_comment(self, comment_id):
        # TODO
        pass

    def submission_details(self, subm):
        return {
            "post": self.filter_subm(subm),
            "comments": self.all_comments_for_subm(subm)
        }

    def all_comments_for_subm(self, subm):
        subm.comments.replace_more(limit=None)
        return [self.comment_tree(comm) for comm in subm.comments]

    def comment_tree(self, comm):
        if len(comm.replies) == 0:
            return self.filter_comm(comm)
        else:
            return {
                "comment": self.filter_comm(comm),
                "replies": [self.comment_tree(c) for c in comm.replies]
            }

    def filter_comm(self, comm):
        return {
            "author_name": comm.author.name,
            "author_flair_text": comm.author_flair_text,
            "body": comm.body,
            "created_utc": comm.created_utc,
            "edited": comm.edited,
            "permalink": comm.permalink,
            "ups": comm.ups
        }

    def filter_subm(self, subm):
        return {
            "author_name": subm.author.name,
            "created_utc": subm.created_utc,
            "edited": subm.edited,
            "permalink": subm.permalink,
            "selftext": subm.selftext,
            "title": subm.title,
            "ups": subm.ups
        }
