class Chapter:
    """
    A single installment of a series. Possibly the only installment.

    A chapter is roughly correlated to a Submission. Sometimes the Submission body is
    the only text of the chapter, and sometimes the chapter body spills into the
    comments.
    """

    def __init__(self, submission):
        self.submission = submission
        self.extract_text()

    def extract_text(self):
        """Extract the text from the submission body and zero or more comments."""
        self.text = self.submission.selftext

        if not self.submission.comments:
            return

        comment = self.submission.comments[0]
        while True:
            if len(comment.body) > 2000:
                # Dumb heuristic to differentiate author notes from actual content
                self.text += comment.body
                comment.body = "[series-to-epub]: included in chapter text"

            if comment.replies == []:
                return
            comment = comment.replies[0]
