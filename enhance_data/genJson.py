import sys
import os
import pandas as pd
from typing import Literal

from utils.utils import get_teams, get_players, get_map

def get_team_round_counts():
    return {
        "roundsPlayed":0,
        "roundsWon":0,
        "ctRoundsPlayed":0,
        "ctRoundsWon":0,
        "tRoundsPlayed":0,
        "tRoundsWon":0
    }

def get_rounds_dict(rounds_df,teams):
    rounds_dict = {}
    for team in teams:
        rounds_dict[team] = get_team_round_counts()
        
    for id,row in rounds_df.iterrows():        
        CT_team = row["CT_team_clan_name"]
        T_team = row["T_team_clan_name"]

        rounds_dict[CT_team]["roundsPlayed"] += 1
        rounds_dict[T_team]["roundsPlayed"] += 1
        rounds_dict[CT_team]["ctRoundsPlayed"] += 1
        rounds_dict[T_team]["tRoundsPlayed"] += 1
        
        if row["winner"] in ("T", "TERRORISTS", 2):
            rounds_dict[T_team]["roundsWon"] += 1
            rounds_dict[T_team]["tRoundsWon"] += 1
        elif row["winner"] in ("CT", "COUNTER-TERRORISTS", 3):
            rounds_dict[CT_team]["roundsWon"] += 1
            rounds_dict[CT_team]["ctRoundsWon"] += 1
        else:
            print(f"Unknown round winner: {row['winner']}")
    return rounds_dict   

def gen_JSON(ticks_df: pd.DataFrame, rounds_df:pd.DataFrame, tournament:str, type:Literal["online","LAN"], is_arena:bool, map:str):
    teams = get_teams(ticks_df)
    rounds = get_rounds_dict(rounds_df, teams)
    players = get_players(ticks_df, teams)
    print(f'{teams[0]} {rounds[teams[0]]["roundsWon"]} - {rounds[teams[1]]["roundsWon"]} {teams[1]}')
    return {
            "teams":teams,
            "rounds":rounds,
            "players":players,
            "tournament": tournament,
            "type":type,
            "isArena":is_arena,
            "map":map,
        }

# if __name__ == "__main__":
#     if len(sys.argv)!=5:
#         print("usage: python3 genJson.py data_directory tournament_name online/LAN isArena")
#     else:
#         data_dir = sys.argv[1]
        
        
#         ticks = pd.read_csv(os.path.join(data_dir,"ticks.csv"))
#         rounds = pd.read_csv(os.path.join(data_dir,"rounds.csv"))
        
#         
#         rounds = get_rounds_dict(rounds,ticks,teams)
#         players = get_players(ticks, teams)
#         map = get_map(data_dir)
        
#         match_dict = 
#         import json
#         with open(data_dir+"/matchInfo.json", "w") as outfile: 
#             json.dump(match_dict, outfile)
        
    
    # check_for_nans(ticks, data_dir)
    
    
    
    