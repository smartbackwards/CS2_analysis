import pandas as pd
import os
import json
from enhance_data.genJson import gen_JSON

directory = "Kato_csv/Kato_dem/saw-vs-gamerlegion-m1-nuke"
PARTS = 3
CSV_names = ["bomb", "damages", "grenades", "infernos", "kills", "rounds", "smokes", "ticks", "weapon_fires"]
tournament = "IEM Katowice 2025 Play-In"
is_lan = "LAN"
is_arena = False
map_played = directory.split('-')[-1]

#make fixed directory
os.makedirs(directory)

for CSV in CSV_names:
    data_list = [] 
    for i in range(PARTS):
        data_list.append(pd.read_csv(os.path.join(f'{directory}-p{i+1}',f'{CSV}.csv')))
    pd.concat(data_list).to_csv(os.path.join(directory,f'{CSV}.csv'))
    if CSV=="ticks":
        ticks=pd.concat(data_list)
    if CSV=="rounds":
        rounds = pd.concat(data_list)

# ticks = pd.read_csv(os.path.join(directory,'ticks.csv'))
# rounds = pd.read_csv(os.path.join(directory,'rounds.csv'))


match_dict = gen_JSON(ticks,rounds,tournament,is_lan,is_arena,map_played)
with open(directory+"/matchInfo.json", "w") as outfile: 
            json.dump(match_dict, outfile)