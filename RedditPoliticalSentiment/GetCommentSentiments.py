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
        netScore = float(sentimentScores['positive']) - float(sentimentScores['negative'])
        netSentimentScores.append(netScore)
    return netSentimentScores


liberalSample = CreateCommentSamples.getRandomSample(100, "LiberalSubCommentsTest.csv")
liberalCommentArr = CreateCommentSamples.convertSampleToArray(liberalSample).tolist()
netLiberalSentiments = getNetSentiments(liberalCommentArr)
meanLiberalSentiment = mean(netLiberalSentiments)
print(meanLiberalSentiment)
