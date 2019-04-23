import csv
import time
from multiprocessing import Process
import praw
import unidecode


# On Reddit and the Reddit API, adding subreddits together in the url such that you have r/sub1+sub2+... treats the
# resulting combination of subs as one single subreddit, allowing us to scrape all of them simultaneously
def createMultiSubString(subArr):
    multiString = ""
    for sub in subArr:
        multiString += "+" + sub
    multiString = multiString[1:]  # Remove leading +
    return multiString


def collectSubComments(fileName, subString):
    with open(fileName + '.csv', 'w', newline='', encoding='ascii') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
        filewriter.writerow(['Comment', 'Subreddit', 'Date Created', 'Author', 'ID'])
        for comment in reddit.subreddit(subString).stream.comments():
            asciiCommentBody = unidecode.unidecode(comment.body)
            # Only add comment to CSV if it is more than three words long for more accurate sentiment analysis
            if len(asciiCommentBody.split()) > 3:
                filewriter.writerow(
                    [asciiCommentBody, comment.subreddit, comment.created_utc, comment.author, comment.id])

reddit = praw.Reddit()
print(reddit.read_only)

liberalSubreddits = ["politics", "neoliberal", "LateStageCapitalism", "SandersForPresident", "socialism",
                     "EnoughTrumpSpam",
                     "progressive"]
conservativeSubreddits = ["the_donald", "Conservative", "askthe_donald", "libertarian", "TheNewRight"]

libString = createMultiSubString(liberalSubreddits)
conString = createMultiSubString(conservativeSubreddits)

#Defining these loops as processes allows us to run the comment streams simultaneously.
libProcess = Process(target=collectSubComments, args=('LiberalSubComments', libString))
conProcess = Process(target=collectSubComments, args=('ConservativeSubComments', conString))
if __name__ == '__main__':
    libProcess.start()
    conProcess.start()

    time.sleep(200000)  #Stop looping after a period of 200,000 seconds, 2.5ish days
    libProcess.terminate()
    conProcess.terminate()
