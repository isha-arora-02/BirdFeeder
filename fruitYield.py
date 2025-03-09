# for oranges, season is december-Feb, so start 9mo in April
# for pomegranates, season is october-december so start 9mo in February.

# THE OUTPUT HERE SHOULD BE AN EXPECTATION!!!

import numpy as np
import random
import json

# outline:
    # make bins for temp and rainfall
    # define which bin this year falls into
    # boostrap an expectation from that sample

# Load from a file
with open('weatherData.json', 'r') as f:
    X = json.load(f)
# print(X)

def averageRain(data, year):
    averageRain = 0
    for value in data[year][0]:
        averageRain += (np.sum(data[year][0][value]) / 12)
    return averageRain

def averageTemp(data, year):
    averageTemp = 0
    for value in data[year][1]:
        averageTemp += (np.sum(data[year][1][value]) / 12)
    return averageTemp

def fruitYield(data, latestWeather):
    # latestWeather is a tuple of this year's weather: (rain, temp).
    # come up w rain and temp avg values for this past year
    fruit = 0
    pomegranateCountList = []
    orangeCountList = []
    for year in data:
        rain = averageRain(data, year)
        temp = averageTemp(data, year)
        # print(rain, temp)
        if abs(latestWeather[0] - rain) < 0.8:
            if abs(latestWeather[1] - temp) < 3:
                pomegranateCountList.append(data[year][3]["pomegranates"])
                orangeCountList.append(data[year][2]["oranges"])
                # print(year)
    # if len(pomegranateCountList) > 0:
    #     print(np.mean(pomegranateCountList), pomegranateCountList)
    return (pomegranateCountList, orangeCountList)
    #bootstrap fruitList for an estimated population mean
        #if rain and temp avg are within x distance from this past year's values, append the fruit count to list
        #make it fruit-specific; do u want to look at orange or pom?

# print(fruitYield(X, (2, 67)))
# tree1 = fruitYeild
# tree2 = fruitYeild
#do it for a few trees and make an "orange sample" for the area. Then use this to bootstrap.

def frootstrap(data, avgRain, avgTemp, numIterations):
    # model five orange trees and five pomegranate bushes
    # averageRain and averageTemp are numbers you observe from this year.
    orangeCounts = []
    pomegranateCounts = []

    orangeList = fruitYield(data, (avgRain, avgTemp))[1]
    pomegranateList = fruitYield(data, (avgRain, avgTemp))[0]
    orangeCounts.extend(orangeList)
    pomegranateCounts.extend((pomegranateList))
        # apparently random.choices() automatically samples WITH replacement.
    bootstrapOrangeMean = 0
    for i in range(numIterations):
        sample = np.random.choice(orangeCounts, len(orangeCounts), replace=True)
        # print(sample)
        sampleSum = np.sum(sample)
        bootstrapOrangeMean += (sampleSum / (numIterations * len(orangeCounts)))
    # print(bootstrapOrangeMean)
    bootstrapPomegranateMean = 0
    for i in range(numIterations):
        sample = np.random.choice(pomegranateCounts, len(pomegranateCounts), replace=True)
        sampleSum = np.sum(sample)
        bootstrapPomegranateMean += (sampleSum / (numIterations * len(pomegranateCounts)))
    # print(bootstrapPomegranateMean)

    return {"orange": bootstrapOrangeMean, "pomegranate": bootstrapPomegranateMean}

 # print(frootstrap(X, 1, 66, 10000))