import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import json

import fruitYield 

class RecommendTrees:
    def __init__(self, pref_probs, tree_counts, seasons):
        """
        Initialize Recommender System

        Parameters:
        pref_probs: numpy array
            array with probabilities for each location
        tree_counts: dict
            {location: {fruit: num_trees}} for number of trees of a fruit in a given location
        seasons: dict
            {fruit: [months]} with list of months that the fruit will yield fruit in the year
        """

        self.pref_probs = pref_probs
        self.fruit_pick_probs = {
            "orange": [0.25, 0.35, 0.30, 0.10],         # for ranges [1-3 fruits, 4-6 fruits, 7-10 fruits, 10+ fruits]
            "pomegranate": [0.45, 0.30, 0.15, 0.10]
        }
        self.fruit_range_midpoints = [2, 5, 8.5, 12]
        self.seasons = seasons
        self.tree_counts = tree_counts
    
    # NOTE: this would be replaced by actual user data in the future
    def simulate_expected_fruit_picked(self, fruit):
        """
        Simulate the expected number of fruit picked from a single fruit tree in a month (assumption made here is that a month is a 30-day period).
        fruit: string
            Name of the fruit tree for which data is to be simulated
        """
        # simulate number of ppl who visit tree in a day normal w mean 4 and var/std 2
        # sample number of ppl from gauss
        # sample for each person the number of fruit picked from multinomial and calculcated expected value of fruits picked in a day
        # do this for all 30 days and take avg

        fruit_pick_probs = self.fruit_pick_probs[fruit]
        expected_val = 0
        for day in range(30):
            num_ppl_visit_today = int(round(stats.norm.rvs(4, 2, size=1)[0]))
            today_dat = np.array([0, 0, 0, 0])
            for person in range(num_ppl_visit_today):
                fruit_picked = stats.multinomial.rvs(1, fruit_pick_probs, size=1)
                today_dat += fruit_picked[0]
            today_expect = 0
            for cat in range(len(today_dat)):
                numfruit = today_dat[cat] * self.fruit_range_midpoints[cat]
                today_expect += numfruit * fruit_pick_probs[cat]
            expected_val += today_expect
        
        expected_val = expected_val / 30

        return expected_val

    def expected_fruit_on_tree_month(self, fruit, pastmo_rain, pastmo_temp):
        """
        Get the expected number of fruit on a single fruit tree in a month (assumption made here is that a month is a 30-day period)
        fruit: string
            Name of the fruit tree for which data is to be calculated  
        pastmo_rain: float
            Average rainfall in inches over the past year
        pastmo_temp: float  
            Average temperature in inches over the past year 
        """

        with open("weatherData.json", "r") as f:
            data = json.load(f)
        fruit_counts = fruitYield.frootstrap(data, pastmo_rain, pastmo_temp, 10000)
        expected_year = fruit_counts[fruit]
        fruit_season = self.seasons[fruit] 

        return expected_year/len(fruit_season)

    def expected_fruit_in_loc(self, expected_picked, expected_yield, location, fruit):
        """
        Get the expected number of fruit in a location in a month (assumption made here is that a month is a 30-day period)
        expected_picked: float
            expected number of fruit picked from a single fruit tree in a month
        expected_yield: float
            expected number of fruit on a single fruit tree in a month
        """
        num_trees = self.tree_counts[location][fruit]
        return (expected_yield - expected_picked) * num_trees
    
    def calculate_fruit_in_all_locs(self, campus_boundary, stanford_map_locs, fruit, pastmo_rain, pastmo_temp):
        """
        Return the expected number of a fruit in each location in a month (assumption made here is that a month is a 30-day period)
        campus_boundary: tuple
            (x1, x2, y1, y2) defining coordinates of campus boundary
        stanford_map_locs: dict
            {location: [(x1, x2), (y1, y2)]} defining the coordinates of the boundary for each location
        fruit: string
            Name of the fruit tree for which data is to be calculated   
        pastmo_rain: float
            Average rainfall in inches over the past year
        pastmo_temp: float  
            Average temperature in inches over the past year    
        """
        all_expected = np.zeros((campus_boundary[1], campus_boundary[3]))

        for loc, coords in stanford_map_locs.items():
            expected_picked = self.simulate_expected_fruit_picked(fruit)
            expected_yield = self.expected_fruit_on_tree_month(fruit, pastmo_rain, pastmo_temp)
            loc_fruit = self.expected_fruit_in_loc(expected_picked, expected_yield, loc, fruit)
            all_expected[coords[0][0], coords[1][0]] = loc_fruit
        
        return all_expected

    def recommend_location(self, campus_boundary, stanford_map_locs, fruit, stanford_coord_locs, pastmo_rain, pastmo_temp):
        """
        Return the location with the largest probability of finding fruit
        campus_boundary: tuple
            (x1, x2, y1, y2) defining coordinates of campus boundary
        stanford_map_locs: dict
            {location: [(x1, x2), (y1, y2)]} defining the coordinates of the boundary for each location
        fruit: string
            Name of the fruit tree for which data is to be calculated
        stanford_coord_locs:
            For each coordinate of the resultant matrix, it provides the respective location on campus
        pastmo_rain: float
            Average rainfall in inches over the past year
        pastmo_temp: float  
            Average temperature in inches over the past year 
        """
        all_locs_values = self.calculate_fruit_in_all_locs(campus_boundary, stanford_map_locs, fruit, pastmo_rain, pastmo_temp)
        scaled_values = np.array(all_locs_values) * np.array(self.pref_probs)
        max_loc_ind = list(np.unravel_index(np.argmax(scaled_values, axis=None), scaled_values.shape))
        max_loc = stanford_coord_locs[tuple(max_loc_ind)]
        print(f"There are {self.tree_counts[max_loc][fruit]} {fruit} trees that you can pick fruits from in {max_loc}!")
        return scaled_values, max_loc
    
    def visualize(self, scaled_values):
        """
        Visualize the probability distribution for finding fruit in each location on campus. 
        """
        probs = (scaled_values.T / sum(sum(scaled_values))).flatten()

        locs = ["gsb", "memchu", "med", "ev", "tressider", "engg"]

        fig, ax = plt.subplots(figsize=(8, 6))
        
        plt.bar(locs, probs)
        
        ax.set_xlabel('Locations')
        ax.set_ylabel('Probabilities')
        
        return fig, ax


# if __name__ == "__main__":
#     import simulateLocationPref as locpreffile
    
#     campus_bounds = (0, 3, 0, 2)  
#     stanford_map_dict = {"ev": [0.5, 1.5], "gsb": [0.5, 0.5], "memchu": [1.5, 0.5], "tressider": [1.5, 1.5], "med": [2.5, 0.5], "engg": [2.5, 1.5]}
#     stanford_map_locs = {"ev": [(0, 1), (1, 2)], "gsb": [(0, 1), (0, 1)], "memchu": [(1, 2), (0, 1)], "tressider": [(1, 2), (1, 2)], "med": [(2, 3), (0, 1)], "engg": [(2, 3), (1, 2)]}
#     stanford_coord_locs = {(0, 1): "ev", (0, 0): "gsb", (1, 0): "memchu", (1, 1): "tressider", (2, 0): "med", (2, 1): "engg"}


#     pref_locs = ["med"]

#     pref_obj = locpreffile.LocationPref(campus_bounds, stanford_map_dict, stanford_map_locs)
#     pdf = pref_obj.create_pref_pdf(pref_locs)

#     fig, ax = pref_obj.visualize(pdf)
#     plt.show()

#     prob_locs = pref_obj.probability_locs(pdf)
#     print(sum(sum(prob_locs)))
#     print(prob_locs)

#     pref_probs = prob_locs
#     tree_counts = {"ev": {"orange": 1, "pomegranate": 1}, "gsb": {"orange": 0, "pomegranate": 0}, "memchu": {"orange": 2, "pomegranate": 0}, "tressider": {"orange": 0, "pomegranate": 0}, "med": {"orange": 1, "pomegranate": 0}, "engg": {"orange": 0, "pomegranate": 1}}
#     stanford_map_locs = {"ev": [(0, 1), (1, 2)], "gsb": [(0, 1), (0, 1)], "memchu": [(1, 2), (0, 1)], "tressider": [(1, 2), (1, 2)], "med": [(2, 3), (0, 1)], "engg": [(2, 3), (1, 2)]}
#     campus_boundary=(0, 3, 0, 2) 
#     seasons = {"orange": ["december", "january", "february"], "pomegranate": ["october", "november", "december"]}

#     obj = RecommendTrees(pref_probs=pref_probs, tree_counts=tree_counts, seasons=seasons)
#     all_expected = obj.calculate_fruit_in_all_locs(campus_boundary, stanford_map_locs, "orange", 1, 69.5)
#     scaled, loc = obj.recommend_location(campus_boundary, stanford_map_locs, "orange", stanford_coord_locs, 1, 69.5)
#     print(scaled, loc)