import sys
import random
from colorama import init, Fore, Style
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


import simulateWeatherData as dat_file
import simulateLocationPref as loc_file

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


def main():
    # print logo!
    bird_color = Fore.LIGHTBLUE_EX
    feeder_color = Fore.LIGHTGREEN_EX
    
    for line in BIRDFEEDER_LOGO:
        bird_part = line[:22]
        feeder_part = line[22:]       
        print(f"{bird_color}{bird_part}{feeder_color}{feeder_part}{Style.RESET_ALL}")
    print()
    print(CARDINAL_ON_TREE)
    print("\n\n\n")
    
    print("Welcome to BirdFeeder!\n")
    user_name = input("Before we get started, what is your name?\n")

    print(f"\n\nHi {user_name}, hope you are having a great day today :) Now, let's starting assisting you to glean fruits.\n")
    print("We have the following locations that you may pick fruits from: Escondido Village, Graduate School of Business, Tressider, Memorial Church, Engineering Quad, and the School of Medicine.\n")
    
    pref_locs_str = input("Please input you preferred locations separated by commas using the guidelines below: \n- For Escondido Village, type ev\n- For Graduate School of Business, type gsb\n- For Tressider, type tressider\n- For Memorial Church, type memchu\n- For the Engineering Quad, type engg\n- For the School of Medicine, type med\n\n")

    pref_locs_lst = [x.strip() for x in pref_locs_str.split(',')]

    pref_obj = loc_file.LocationPref(CAMPUS_BOUNDS, STANFORD_MAP_DICT, STANFORD_MAP_LOCS)
    pref_pdf = pref_obj.create_pref_pdf(pref_locs_lst)

    # ask user for location prefs
    # map answers to graph (x, y) coordinates
    # run generation of location pref prob distribution
    # etc.
    

if __name__ == "__main__":
    main()

