import time
from statistics import mean

import CreateCommentSamples
import config
import paralleldots

paralleldots.set_api_key(config.parallelDotsAPIKey)
langCode = config.lang_code  # Set to "en", can be changed


def getNetSentiments(commentArray):
    jsonResponse = paralleldots.batch_sentiment(commentArray)
    print(jsonResponse)
    netSentimentScores = []
    for sentimentScores in jsonResponse['sentiment']:
        # Subtract positivity probability from negative prob to get net sentiment score. Neutral does not need
        # consideration because it would reduce the extremity of results by taking away from pos and neg scores.
        netScore = float(sentimentScores['positive']) - float(sentimentScores['negative'])
        netSentimentScores.append(netScore)
    return netSentimentScores


def netSentimentsWithRateLimit(requestsPerMinuteAllowed, commentArray):
    numberOfQueries = int(len(commentArray) / requestsPerMinuteAllowed) + 1
    allNetSentiments = []
    for i in range(numberOfQueries):
        netSentimentsPortion = getNetSentiments(
            commentArray[i * requestsPerMinuteAllowed: i * requestsPerMinuteAllowed + requestsPerMinuteAllowed])
        allNetSentiments.extend(netSentimentsPortion)
        if (i != numberOfQueries - 1):
            time.sleep(65)  # Rate limit resets every minute, using 65 seconds just to be safe
    return allNetSentiments


liberalSample = CreateCommentSamples.getRandomSample(14, "LiberalSubCommentsTest.csv")
liberalCommentArr = CreateCommentSamples.convertSampleToArray(liberalSample).tolist()
# Rate limit is approx 20 requests/min, using 10 just in case because long comments can count for multiple requests
netLiberalSentiments = netSentimentsWithRateLimit(15, liberalCommentArr)
meanLiberalSentiment = mean(netLiberalSentiments)
print("Mean Liberal Sentiment: " + str(meanLiberalSentiment))
