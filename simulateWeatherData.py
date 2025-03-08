
##############################################################################
                         # to-do
                         # the temp scale in fruit fn is still hard to understand.
                         # app logo
##############################################################################

import random
from scipy import stats
from scipy.stats import bernoulli


def generate_rainfall(lmbda=2):
    # default lambda is 2 to represent the "typical" time until a "success", meaning
    # rainfall. The bernoullis create outlier lambdas to add more heterogeneity to the
    # numbers this fn returns.
    if bernoulli.rvs(0.15):
        if bernoulli.rvs(0.5): #choose an extremely high or low val for lambda.
            lmbda = random.choice([6])
        else:
            lmbda = random.choice([0.1])
    B = stats.expon(scale=lmbda)
    return tuple(round(B.rvs(), 2) for _ in range(12))

# def generate_temperature():
#     """Generate monthly temperature data using a uniform distribution."""
#     return tuple(round(random.uniform(30, 80), 1) for _ in range(12))
#


def generate_temperature():
    """Generate monthly temperature data using a normal distribution."""
    # Average temperatures (°F) for Northern California by month
    avg_temps = [50, 54, 57, 60, 65, 70, 75, 76, 74, 66, 57, 51]

    # different stdevs for each month
    std_devs = [5, 5, 6, 6, 7, 7, 8, 8, 7, 6, 5, 5]

    # Pair the avg temps and st.devs above, then go thru them as pairs (the zip fn does this)
    # each temp/stdev pairing is used as params in normal to get one sample for each month of the year.
    temperatures = tuple(round(stats.norm(loc=mu, scale=sigma).rvs(), 1) for mu, sigma in zip(avg_temps, std_devs))
    #you'll get a TUPLE of TWELVE values.
    return temperatures



def calculate_fruit_yield(rainfall, temperature, fruitType):
    """Calculate fruit yield based on rainfall and temperature conditions."""
    avg_rainfall = sum(rainfall) / len(rainfall)
    avg_temperature = sum(temperature) / len(temperature)
    if fruitType == "orange":
        # Normalize values to a scale (assuming max rainfall ~12 inches per month)
        rainfall_factor = avg_rainfall * 50  # 50-point contribution from rainfall
        # Temperature effect: ideal range ~50-70°F, penalizing extreme values
        # temp_factor first gets distance from 60, the 'ideal temp'.
        # if it's exactly 60, you have a value of 0 which will stay 0 when divided by 60
        # subtracting this from 1 yeilds 1, so it has max contribution.
        # the opposite of this is true if temp is 0.
        temp_factor = max(0, (1 - abs(avg_temperature - 60) / 30)) * 50
        fruitMean = round(rainfall_factor + temp_factor)
        if fruitMean > 280:
            fruitMean = 280
    if fruitType == "pomegranate":
        rainfall_factor = avg_rainfall * 5
        temp_factor = max(0, (1 - abs(avg_temperature - 60) / 60)) * 5
        fruitMean = round(rainfall_factor + temp_factor)
        if fruitMean > 15:
            fruitMean = 15
    fruitVariance = fruitMean * 0.1
    fruitGaussian = stats.norm(fruitMean, fruitVariance)
    fruitYield = fruitGaussian.rvs()
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
    for year in range(2010, 2026):
        rainfall = generate_rainfall()
        temperature = generate_temperature()
    # fruit yeild will be based off avg PAST NINE MO.
        orange_yield = calculate_fruit_yield(rainfall, temperature, "orange")
        pomegranate_yield = calculate_fruit_yield(rainfall, temperature, "pomegranate")


        weather_data[year] = [
            {"rainfall": rainfall},
            {"temperature": temperature},
            {"oranges": orange_yield},
            {"pomegranates": pomegranate_yield}
        ]
    return weather_data
simulateWeatherData()