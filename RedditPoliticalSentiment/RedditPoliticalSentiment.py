import praw

reddit = praw.Reddit()
print(reddit.read_only)

for submission in reddit.subreddit('learnpython').new(limit=5):
    print(submission.title)
