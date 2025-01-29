import os
import pandas as pd

from utils.stats import identify_and_mark_trade_kills

TIER_ONE_DIR = "E:/Tier1_2025/"

for tournament_dir in os.listdir(TIER_ONE_DIR):
    for map_dir in os.listdir(os.path.join(TIER_ONE_DIR,tournament_dir)):
        # add new functionality 
        kills = pd.read_csv(os.path.join(TIER_ONE_DIR,tournament_dir,map_dir,"kills.csv"))
        rounds = pd.read_csv(os.path.join(TIER_ONE_DIR,tournament_dir,map_dir,"rounds.csv"))
        
        kills = identify_and_mark_trade_kills(kills,rounds)
        kills.to_csv(os.path.join(TIER_ONE_DIR,tournament_dir,map_dir,"kills.csv"))
        
        