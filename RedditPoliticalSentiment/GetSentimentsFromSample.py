import time
from statistics import mean
# noinspection PyUnresolvedReferences
import config
import paralleldots
import random
import pandas

def getRandomSample(sampleSize, fileName):
    population = pandas.read_csv(fileName, sep=',')
    populationSize = len(population.index)
    rowsToSkip = random.sample(range(1, populationSize), populationSize - sampleSize)
    sample = pandas.read_csv(fileName, skiprows=rowsToSkip)
    return sample

def convertSampleToArray(sample):
    comments = sample.Comment.values
    return comments

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
        if i != numberOfQueries - 1:
            time.sleep(65)  # Rate limit resets every minute, using 65 seconds just to be safe
    return allNetSentiments

def takeSampleAndGetMeanSentiment(populationFileName):
    sampleSize = 100
    rateLimitPerMin = 15
    sample = getRandomSample(sampleSize, populationFileName)
    sampleCommentArr = convertSampleToArray(sample).tolist()
    # Rate limit is approx 20 requests/min, using 15 just in case because long comments can count for multiple requests
    netSampleSentiments = netSentimentsWithRateLimit(rateLimitPerMin, sampleCommentArr)
    meanSampleSentiment = mean(netSampleSentiments)
    print('Mean Sample Sentiment for (%d): ' % populationFileName + str(meanSampleSentiment))
    return meanSampleSentiment

liberalMeanSentiment = takeSampleAndGetMeanSentiment('LiberalSubComments.csv')
conservativeMeanSentiment = takeSampleAndGetMeanSentiment('ConservativeSubComments.csv')
meanSentimentDifference = liberalMeanSentiment - conservativeMeanSentiment
print("Mean Difference: %d" % meanSentimentDifference)

