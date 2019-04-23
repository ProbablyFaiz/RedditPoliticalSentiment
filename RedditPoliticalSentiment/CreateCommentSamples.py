import random

import pandas


def getRandomSample(sampleSize, fileName):
    population = pandas.read_csv(fileName, sep=',')
    populationSize = len(population.index)
    rowsToSkip = random.sample(range(1, populationSize), populationSize - sampleSize)
    sample = pandas.read_csv(fileName, skiprows=rowsToSkip)
    return sample


sampleSize = 10
projectPath = 'C:/Users/faizs/source/Python/RedditPoliticalSentiment/RedditPoliticalSentiment/'

liberalSample = getRandomSample(sampleSize, "LiberalSubComments.csv")
liberalSample.to_csv(path_or_buf=projectPath + 'LiberalSubSample.csv')
conservativeSample = getRandomSample(sampleSize, "ConservativeSubComments.csv")
conservativeSample.to_csv(path_or_buf=projectPath + 'ConservativeSubSample.csv')
