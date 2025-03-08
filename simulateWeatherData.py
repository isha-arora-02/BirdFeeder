import random
import numpy as np

##############################################################################
                         #   IDEA!
##############################################################################
# model average rainfall differently...use an exponential. ChatGPT says that exponential is
# good for areas where rain occurs in bursts with long dry spells. Perfect for NorCal.
# I just made the change.

# another idea: need to make some sort of correlation between rain, temp, and number of fruit
# so that the bayes net is actually making predictions based on some underlying
# biological reality about how these trees respond to environmental factors.

# Function to generate simulated rainfall data (in inches)
def generate_rainfall(lmbda=1.0):  # Lambda is the rate parameter (1/mean rainfall)
    return tuple(round(random.expovariate(lmbda), 2) for _ in range(12))

# Function to generate simulated temperature data (in Fahrenheit)
def generate_temperature():
    return tuple(round(random.uniform(30, 80), 1) for _ in range(12))

# Create dictionary with data from 2010 to 2025
weather_data = {}
for year in range(2010, 2026):
    weather_data[year] = [
        {"rainfall": generate_rainfall()},  # Rainfall data for the year
        {"temperature": generate_temperature()}  # Temperature data for the year
    ]

print(weather_data)