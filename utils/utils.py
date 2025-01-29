import pandas as pd
import os 
import json

def check_for_nans(ticks: pd.DataFrame, match_name:str):
    nan_indices = ticks[ticks["round"].isna()].index
    if len(nan_indices)>0:
        ranges = []
        start = nan_indices[0]
        for i in range(1, len(nan_indices)):
            if nan_indices[i] != nan_indices[i - 1] + 1:
                ranges.append((start, nan_indices[i - 1]))
                start = nan_indices[i]
        ranges.append((start, nan_indices[-1]))
        
        print(f"Rounds error in {match_name}")
        for rng in ranges:
            print(f"rows: {rng}, first_tick: {ticks.loc[rng[0],'tick']}, last_tick: {ticks.loc[rng[1],'tick']}")
        raise Exception("NaNs exist in round column in the ticks dataframe")
    else:
        print(f"Rounds alright in {match_name}, generating JSON")
        
def get_teams(ticks: pd.DataFrame):
    teams = list(dict.fromkeys(ticks["team_clan_name"].to_list()))
    clean_teams = []
    for team in teams:
        if str(team)!="nan":
            clean_teams.append(team)
    return sorted(clean_teams)

def get_players(ticks: pd.DataFrame,teams:list):
    playerdict = {}
    for team in teams:
        playerdict[team] = list(dict.fromkeys(ticks[ticks["team_clan_name"]==team]["name"].to_list()))
    return playerdict

def get_map(data_dir):
    return data_dir.split("-")[-1].replace("/","")

def get_kill_death_occurrences(df, player):
    df = df[pd.notna(df["attacker_team_name"])]
    df_a = df[df["attacker_team_name"]!=df["victim_team_name"]]
    return (df_a["attacker_name"]==player).sum(), (df["victim_name"]==player).sum()

def get_match_info(data_directory):
    with open(os.path.join(data_directory,"matchinfo.json"), 'r') as file:
        data = json.load(file)
    return data