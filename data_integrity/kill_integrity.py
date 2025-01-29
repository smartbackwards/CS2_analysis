import pandas as pd
import sys
import os
import json

kill_dict = {}
data_directory = sys.argv[1]
for maps in os.listdir(data_directory):
    kills_df = pd.read_csv(os.path.join(data_directory,maps,"kills.csv"))
    kills_df = kills_df[kills_df["attacker_team_name"]!=kills_df["victim_team_name"]]
    
    with open(os.path.join(data_directory,maps,'matchInfo.json'), 'r') as file:
        info_dict = json.load(file)
    
    for team in info_dict["teams"]:
        # for player in info_dict["players"][team]:
        #     if player not in kill_dict:
        #         kill_dict[player] = 0
        if team not in kill_dict:
            kill_dict[team] = 0
               
        kill_dict[team] += (kills_df["attacker_team_clan_name"]==team).sum()

kd = dict(sorted(kill_dict.items(), key=lambda item: item[1], reverse=True))
for player in kd:
    print(player, kill_dict[player])
            
    