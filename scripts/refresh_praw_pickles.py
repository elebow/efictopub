import pickle
import praw

from app.lib import reddit_util

reddit = reddit_util.setup_reddit()

subm1 = praw.models.reddit.submission.Submission(reddit, id='886al5')
subm1.comments[0]
subm1.selftext
subm2 = praw.models.reddit.submission.Submission(reddit, id='88bcar')
subm2.comments[0]
subm2.selftext
subm3 = praw.models.reddit.submission.Submission(reddit, id='88ejcl')
subm3.comments[0]
subm3.selftext = subm3.selftext.replace("[Next]", "nah")

subms = [subm1, subm2, subm3]

with open("array_of_3_submissions_with_comments.pickle", "wb") as outfile:
    pickle.dump(subms, outfile)
