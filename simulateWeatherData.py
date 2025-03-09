import random
from scipy import stats
from scipy.stats import bernoulli
import json

def generate_rainfall():
    avg_rain = [4, 4, 2.5, 1.5, 0.75, 0.5, 0.1, 0.1, 0, 1.5, 3, 5]
    std_devs = [1, 1, 1, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 1, 0.8, 1.2]


    # Pair the avg temps and st.devs above, then go thru them as pairs (the zip fn does this)
    # each temp/stdev pairing is used as params in normal to get one sample for each month of the year.
    rainfall = tuple(abs(round(stats.norm(loc=mu, scale=sigma).rvs(), 1)) for mu, sigma in zip(avg_rain, std_devs))
    return rainfall


def generate_temperature():
    """Generate monthly temperature data using a normal distribution."""
    # Average temperatures (°F) for norCal by month
    if bernoulli.rvs(0.75):
        avg_temps = [50, 54, 57, 60, 65, 70, 75, 76, 74, 66, 57, 51]
        std_devs = [2, 3, 1, 1, 1, 2, 3, 2, 4, 3, 2, 2]
    elif bernoulli.rvs(0.5):
        avg_temps = [50, 49, 54, 55, 58, 60, 70, 71, 70, 66, 54, 54]
        std_devs = [2, 3, 1, 1, 1, 2, 3, 2, 4, 3, 2, 2]
    else:
        avg_temps = [60, 61, 60, 62, 68, 70, 75, 74, 72, 76, 60, 59]
        std_devs = [2, 3, 1, 1, 1, 2, 3, 2, 4, 3, 2, 2]

    # Pair the avg temps and st.devs above, then go thru them as pairs (the zip fn does this)
    # each temp/stdev pairing is used as params in normal to get one sample for each month of the year.
    temperatures = tuple(round(stats.norm(loc=mu, scale=sigma).rvs(), 1) for mu, sigma in zip(avg_temps, std_devs))
    #you'll get a TUPLE of TWELVE values.
    return temperatures



def calculate_fruit_yield(rainfall, temperature, fruitType):
    """Calculate fruit yield based on rainfall and temperature conditions."""

    if fruitType == "orange":
        for month in range(12):
            fruitYield = 180 + (10 * temperature[month]) + (5 * rainfall[month]) - (0.2 * (temperature[month] ** 2)) - (0.05 * (rainfall[month] ** 2)) + (0.5 * temperature[month] * rainfall[month])
            if fruitYield < 0:
                fruitYield = 0

    if fruitType == "pomegranate":
        for month in range(12):
            fruitYield = 10 + (7 * temperature[month]) + (3 * rainfall[month]) - (0.15 * (temperature[month] ** 2)) - (0.07 * (rainfall[month] ** 2)) + (0.3 * temperature[month] * rainfall[month])
            if fruitYield < 0:
                fruitYield = 0
        # if fruitMean > 15:
        #     fruitMean = 15
    # fruitVariance = fruitMean * 0.1
    # fruitGaussian = stats.norm(fruitMean, fruitVariance)

    return round(fruitYield)


def simulateWeatherData():
    """
    This function simulates data tying temperature and rainfall to AVERAGE fruit
    production on orange and pomegranate plants at Stanford. It contains a dictionary of years,
    and each year has four inner dictionaries:
    - "rainfall" <- length-12 tuple of monthly rainfall
    - "temperature" <- length-12 tuple of monthly temps
    - "oranges" <- average orange production across Stanford trees for the year
    - "pomegranates" <- average pomegranate production across Stanford bushes for the year
    """
    weather_data = {}
    for year in range(1995, 2026):
        rainfall = generate_rainfall()
        temperature = generate_temperature()
        orange_yield = calculate_fruit_yield(rainfall, temperature, "orange")
        pomegranate_yield = calculate_fruit_yield(rainfall, temperature, "pomegranate")


        weather_data[year] = [
            {"rainfall": rainfall},
            {"temperature": temperature},
            {"oranges": orange_yield},
            {"pomegranates": pomegranate_yield}
        ]
    return weather_data


weatherData = simulateWeatherData()
# print(weatherData)

# saving weatherData into json format
with open('weatherData.json', 'w') as f:
    json.dump(weatherData, f)

