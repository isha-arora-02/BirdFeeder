import sys
import random
from colorama import init, Fore, Style
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date

import simulateWeatherData as dat_file
import simulateLocationPref as loc_file
import recommenderSystem as rec_file

# Initialize colorama
init()

BIRDFEEDER_LOGO = [
    "  ____  _          _   _______           _           ",
    " |  _ \\(_)        | | |  _____|         | |          ",
    " | |_) |_ _ __ ___| | | |__ ___  ___   _| | ___ _ __ ",
    " |  _ <| | '__/  _| | |  __/ _ \\/ _ \\/ _  |/ _ \\ '__|",
    " | |_) | | |  | |_| | | | |  __/| __/ |_| |  __/      ",
    " |____/|_|_|  |___/_| |_|  \___|\\___|\\__/_|\\___|_|   "
]

CARDINAL_ON_TREE = r""" 
      _
    <(o )___
      (  __/
       `~~~
        ccee88oo   
     C8O8O8Q8PoOb o8oo
    dOB69QO8PdUOpugoO9bD
CgggbU8OU qOp qOdoUOdcb
    6OuU  /p u gcoUodpP
      \\\//  /duUp/
        \\\////
         |||/\
         |||||
         |||||
         |||||
         |||||
         |||||
"""

CAMPUS_BOUNDS = (0, 3, 0, 2) 
STANFORD_MAP_DICT = {"ev": [0.5, 1.5], "gsb": [0.5, 0.5], "memchu": [1.5, 0.5], "tressider": [1.5, 1.5], "med": [2.5, 0.5], "engg": [2.5, 1.5]}
STANFORD_MAP_LOCS = {"ev": [(0, 1), (1, 2)], "gsb": [(0, 1), (0, 1)], "memchu": [(1, 2), (0, 1)], "tressider": [(1, 2), (1, 2)], "med": [(2, 3), (0, 1)], "engg": [(2, 3), (1, 2)]}
STANFORD_COORD_LOCS = {(0, 1): "ev", (0, 0): "gsb", (1, 0): "memchu", (1, 1): "tressider", (2, 0): "med", (2, 1): "engg"}
TREE_COUNTS =  {"ev": {"orange": 1, "pomegranate": 1}, "gsb": {"orange": 0, "pomegranate": 0}, "memchu": {"orange": 2, "pomegranate": 0}, "tressider": {"orange": 0, "pomegranate": 0}, "med": {"orange": 1, "pomegranate": 0}, "engg": {"orange": 0, "pomegranate": 1}}
SEASONS = {"orange": ["december", "january", "february"], "pomegranates": ["october", "november", "december"]}



def main():

    def input_valid_str(prompt, valid_values):
        while True:
            user_input = input(prompt).strip().lower() 
            if user_input in valid_values:
                return user_input
            else:
                print(f"That is not one of the options! Please enter one of {valid_values}\n")

    def input_valid_lst(prompt, valid_values):
        flag = True
        while flag:
            user_input = input(prompt)
            user_input_lst = [x.strip() for x in user_input.split(',')]
            for i in user_input_lst:
                if i not in valid_values:
                    flag = False
            if flag == True:
                return user_input
            else:
                print(f"That is not one of the options! Please enter one of {valid_values}\n")
                flag = True


    # print logo!
    bird_color = Fore.LIGHTBLUE_EX
    feeder_color = Fore.LIGHTGREEN_EX
    
    for line in BIRDFEEDER_LOGO:
        bird_part = line[:22]
        feeder_part = line[22:]       
        print(f"{bird_color}{bird_part}{feeder_color}{feeder_part}{Style.RESET_ALL}")
    print()
    print(CARDINAL_ON_TREE)
    print("\n\n")
    
    print("Welcome to BirdFeeder!\n")
    user_name = input("Before we get started, what is your name?\n")

    print(f"\n\nHi {user_name}, hope you are having a great day today :) Now, let's starting assisting you to glean fruits.\n")

    print("We have the following locations that you may pick fruits from: Escondido Village, Graduate School of Business, Tressider, Memorial Church, Engineering Quad, and the School of Medicine.\n")
    
    pref_locs_str = input_valid_lst("Please input you preferred locations separated by commas using the guidelines below: \n- For Escondido Village, type ev\n- For Graduate School of Business, type gsb\n- For Tressider, type tressider\n- For Memorial Church, type memchu\n- For the Engineering Quad, type engg\n- For the School of Medicine, type med\n\n", ["ev", "gsb", "memchu", "tressider", "med", "engg"])

    # get pdf of preferred locations
    pref_locs_lst = [x.strip() for x in pref_locs_str.split(',')]
    pref_obj = loc_file.LocationPref(CAMPUS_BOUNDS, STANFORD_MAP_DICT, STANFORD_MAP_LOCS)
    pref_pdf = pref_obj.create_pref_pdf(pref_locs_lst)
    prob_locs = pref_obj.probability_locs(pref_pdf)

    fruit = input_valid_lst("\nNow, please tell us what fruit you would like to pick of the following: orange, pomegranate\n", ["orange", "pomegranate"])
    fruit = fruit.strip().lower()

    # ensure fruit can be picked in this month
    month = date.today().strftime("%B")

    if month.lower() not in SEASONS[fruit]:
        print(f"\nUnfortunately, {fruit}s are not available in {month}. :,( But, I can show you the probailities of picking {fruit}s on different locations on campus in the months that {fruit} trees on campus yield fruits.\n")
        monthlst = ", ".join(SEASONS[fruit])
        month = input_valid_lst(f"Which of the following months would you like to view these probabilities for? - {monthlst}\n", SEASONS[fruit])

    print("\nCalculating the best location to visit...\n\n")

    # define recommender object
    rec_obj = rec_file.RecommendTrees(prob_locs, TREE_COUNTS, SEASONS)
    scaled_values, loc_to_visit = rec_obj.recommend_location(CAMPUS_BOUNDS, STANFORD_MAP_LOCS, fruit, STANFORD_COORD_LOCS)

    print("Now let's see what the probability distributions were for finding fruit for each location!")
    fig, ax = rec_obj.visualize(scaled_values)
    plt.title("Probability Distribution of Finding Fruits")
    plt.show()

if __name__ == "__main__":
    main()

