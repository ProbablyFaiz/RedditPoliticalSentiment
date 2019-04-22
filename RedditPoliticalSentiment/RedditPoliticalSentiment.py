import praw
import csv
import datetime
from multiprocessing import Process

#On Reddit and the Reddit API, adding subreddits together in the url such that you have r/sub1+sub2+...
#treats the resulting combination of subs as one single subreddit, allowing me to scrape all of them simultaneously
def createMultiSubString(subArr):
    multiString = ""
    for sub in subArr:
        multiString +=  "+" + sub
    multiString = multiString[1:]
    return multiString

def collectSubComments(fileName, subString): 
    with open(fileName + '.csv', 'w',newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
        filewriter.writerow(['Comment', 'Subreddit','Date Created','Author','ID'])
        for comment in reddit.subreddit(subString).stream.comments():
            commentBodySansFormatting = comment.body.encode('ascii', errors='ignore')
            filewriter.writerow([commentBodySansFormatting, comment.subreddit, comment.created_utc, comment.author, comment.id])

def main():
    reddit = praw.Reddit()
    print(reddit.read_only)

    liberalSubreddits = ["neoliberal","LateStageCapitalism","SandersForPresident","socialism","EnoughTrumpSpam","progressive"]
    conservativeSubreddits = ["the_donald","Conservative","askthe_donald","libertarian","TheNewRight"]

    libString = createMultiSubString( liberalSubreddits)
    conString = createMultiSubString(conservativeSubreddits)
    print(libString)

    collectSubComments('LiberalSubComments', libString)
    collectSubComments('ConservativeSubComments', conString)

