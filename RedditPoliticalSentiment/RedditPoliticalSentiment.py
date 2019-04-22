import praw
import csv
import datetime
from multiprocessing import Process

def createMultiSubString(subArr):
    multiString = ""
    for sub in subArr:
        multiString +=  "+" + sub
    multiString = multiString[1:]
    return multiString

def collectSubComments(fileName, subString): 
    with open(fileName + '.csv', 'w',newline='',encoding='utf-8') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', escapechar='\\', quoting=csv.QUOTE_ALL)
        filewriter.writerow(['Comment', 'Subreddit','Date Created','Author','ID'])
        for comment in reddit.subreddit(subString).stream.comments():
            commentBodySansFormatting = comment.body.encode('utf-8', errors='ignore')
            filewriter.writerow([commentBodySansFormatting, comment.subreddit, comment.created_utc, comment.author, comment.id])

reddit = praw.Reddit()
print(reddit.read_only)

liberalSubreddits = ["neoliberal","LateStageCapitalism","SandersForPresident","socialism","EnoughTrumpSpam","progressive"]
conservativeSubreddits = ["the_donald","Conservative","askthe_donald","libertarian","TheNewRight"]

libString = createMultiSubString( liberalSubreddits)
conString = createMultiSubString(conservativeSubreddits)
print(libString)

collectSubComments('LiberalSubComments', libString)
collectSubComments('ConservativeSubComments', conString)

