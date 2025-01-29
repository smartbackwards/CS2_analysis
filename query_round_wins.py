import os
import sys
import pandas as pd
from utils.utils import get_match_info
from utils.stats import analyse_df_clawback_bozo, analyse_round_clawback_bozo
from style.style import get_style_dict

TOURNAMENT_DIRS = [#"E:/Tier1_2025/BLAST Bounty Season 1/",
                   "E:/Tier1_2025/BLAST Bounty Season 1 Finals/"]

# get percentage of round wins that had to be clawed back
# fake 4v5%, 5v4%
def get_clawback_win_pct():
    results = {}
    
    for TOURNAMENT_DIR in TOURNAMENT_DIRS:
        for map_dir in os.listdir(TOURNAMENT_DIR):
            rounds = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"rounds.csv"))
            kills = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"kills.csv"))
            match_info = get_match_info(os.path.join(TOURNAMENT_DIR,map_dir))
            teams = match_info["teams"]
            
            for team in teams:
                if team not in results:
                    results[team] = {"W":0, "L":0, "CBW":0, "BL":0}
            
            for id, row in rounds.iterrows():
                kills_in_round_df = kills[kills["round"]==row["round"]]
                winner = row["winner_clan_name"]
                loser = teams[0] if winner==teams[1] else teams[1]   
                
                round_was_cbk = not analyse_round_clawback_bozo(kills_in_round_df,row["winner"]).empty
                if round_was_cbk:
                    results[winner]["CBW"] += 1
                    results[loser]["BL"] += 1
                
                results[winner]["W"] += 1
                results[loser]["L"] += 1
                
    return results

def get_buyround_win_pct():
    results = {}
    
    for TOURNAMENT_DIR in TOURNAMENT_DIRS:
        for map_dir in os.listdir(TOURNAMENT_DIR):
            rounds = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"rounds.csv"))
            kills = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"kills.csv"))
            match_info = get_match_info(os.path.join(TOURNAMENT_DIR,map_dir))
            teams = match_info["teams"]
            
            for team in teams:
                if team not in results:
                    results[team] = {"W":0, "L":0, "BRW":0, "BRL":0}
            
            for id, row in rounds.iterrows():
                # kills_in_round_df = kills[kills["round"]==row["round"]]
                winner = row["winner_clan_name"]
                loser = teams[0] if winner==teams[1] else teams[1]   
                
                # round_was_cbk = not analyse_round_clawback_bozo(kills_in_round_df,row["winner"]).empty
                if row["CT_average_economy"]>=3800 and row["T_average_economy"]>=3800:
                    results[winner]["BRW"] += 1
                    results[loser]["BRL"] += 1
                
                results[winner]["W"] += 1
                results[loser]["L"] += 1
                
    return results

def get_buy_vs_low_econ_pct():
    results = {}
    
    for TOURNAMENT_DIR in TOURNAMENT_DIRS:
        for map_dir in os.listdir(TOURNAMENT_DIR):
            rounds = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"rounds.csv"))
            kills = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"kills.csv"))
            match_info = get_match_info(os.path.join(TOURNAMENT_DIR,map_dir))
            teams = match_info["teams"]
            
            for team in teams:
                if team not in results:
                    results[team] = {"W":0, "L":0, "BRW":0, "BRL":0, "LRW":0, "LRL":0}
            
            for id, row in rounds.iterrows():
                # kills_in_round_df = kills[kills["round"]==row["round"]]
                winner = row["winner_clan_name"]
                loser = teams[0] if winner==teams[1] else teams[1]   
                
                # round_was_cbk = not analyse_round_clawback_bozo(kills_in_round_df,row["winner"]).empty
                if row["winner"]=="CT":
                    if row["CT_average_economy"]>=3800 and row["T_average_economy"]<3800:
                        results[winner]["BRW"] += 1
                        results[loser]["LRL"] += 1
                    elif row["T_average_economy"]>=3800 and row["CT_average_economy"]<3800:
                        results[winner]["LRW"] += 1
                        results[loser]["BRL"] += 1
                elif row["winner"]=="T":
                    if row["T_average_economy"]>=3800 and row["CT_average_economy"]<3800:
                        results[winner]["BRW"] += 1
                        results[loser]["LRL"] += 1
                    elif row["CT_average_economy"]>=3800 and row["T_average_economy"]<3800:
                        results[winner]["LRW"] += 1
                        results[loser]["BRL"] += 1
                else:
                    print(f'unknown winner {row["winner"]}')
                
                
                results[winner]["W"] += 1
                results[loser]["L"] += 1
                
    return results
            
def get_t_side_trade_pct():
    results = {}
    
    for TOURNAMENT_DIR in TOURNAMENT_DIRS:
        for map_dir in os.listdir(TOURNAMENT_DIR):
            kills = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"kills.csv"))
            match_info = get_match_info(os.path.join(TOURNAMENT_DIR,map_dir))
            teams = match_info["teams"]
            
            for team in teams:
                if team not in results:
                    results[team] = {"deaths":0, "tSideDeaths":0, "tradedDeaths":0, "tradedTSideDeaths":0}
                
            kills = kills[kills["attacker_team_name"]!=kills["victim_team_name"]]
            
            for team in teams:
                team_deaths = kills[kills["victim_team_clan_name"]==team]
                results[team]["deaths"] += team_deaths["is_traded"].count()
                results[team]["tradedDeaths"] += team_deaths["is_traded"].sum()
                
                t_deaths = team_deaths[team_deaths["victim_team_name"]=="TERRORIST"]
                results[team]["tSideDeaths"] += t_deaths["is_traded"].count()
                results[team]["tradedTSideDeaths"] += t_deaths["is_traded"].sum()
        return results
 
def get_average_team_positions_both_sides(queried_team, queried_map, time=20):
    data = []
    for TOURNAMENT_DIR in TOURNAMENT_DIRS:
        for map_dir in os.listdir(TOURNAMENT_DIR):
            match_info = get_match_info(os.path.join(TOURNAMENT_DIR,map_dir))
            
            if match_info["map"]!=queried_map or queried_team not in match_info["teams"]:
                continue
            
            rounds = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"rounds.csv"))
            ticks = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"ticks.csv"))
            
            ticks = ticks[ticks["team_clan_name"]==queried_team]
            
            for id, row in rounds.iterrows():
                data.append(ticks[ticks["tick"]==time*64+row["freeze_end"]])
    return pd.concat(data)
            
            
team_trades = get_t_side_trade_pct()

for team in team_trades:
    print(team, team_trades[team])               