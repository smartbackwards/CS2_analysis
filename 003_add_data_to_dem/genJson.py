import sys
import os
import pandas as pd

def check_for_nans(ticks,data_dir):
    nan_indices = ticks[ticks["round"].isna()].index
    if len(nan_indices)>0:
        ranges = []
        start = nan_indices[0]
        for i in range(1, len(nan_indices)):
            if nan_indices[i] != nan_indices[i - 1] + 1:
                ranges.append((start, nan_indices[i - 1]))
                start = nan_indices[i]
        ranges.append((start, nan_indices[-1]))
        
        print(f"Rounds error in {data_dir}")
        for rng in ranges:
            print(f"rows: {rng}, first_tick: {ticks.loc[rng[0],'tick']}, last_tick: {ticks.loc[rng[1],'tick']}")
        sys.exit()
        # return ranges
    else:
        print(f"Rounds alright in {data_dir}, generating JSON")

def get_map(data_dir):
    return data_dir.split("-")[-1].replace("/","")


def get_team_round_counts():
    return {
        "roundsPlayed":0,
        "roundsWon":0,
        "ctRoundsPlayed":0,
        "ctRoundsWon":0,
        "tRoundsPlayed":0,
        "tRoundsWon":0
    }

def get_rounds_dict(rounds,ticks,teams):
    rounds_dict = {}
    for team in teams:
        rounds_dict[team] = get_team_round_counts()
        
    for id,row in rounds.iterrows():
        round_no = row["round"]
        
        round_ticks = ticks[ticks["round"]==round_no]
        
        CT_team = round_ticks[round_ticks["team_name"]=="CT"]["team_clan_name"].iloc[0]
        T_team = round_ticks[round_ticks["team_name"]=="TERRORIST"]["team_clan_name"].iloc[0]
        
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
        # print(CT_team, T_team, row["winner"])

def get_teams(ticks):
    clean_teams = []
    for team in list(dict.fromkeys(ticks["team_clan_name"].to_list())):
        if str(team)!= "nan":
            clean_teams.append(team)
    return clean_teams        

def get_players(ticks,teams):
    playerdict = {}
    for team in teams:
        playerdict[team] = list(dict.fromkeys(ticks[ticks["team_clan_name"]==team]["name"].to_list()))
    return playerdict

if __name__ == "__main__":
    if len(sys.argv)!=5:
        print("usage: python3 genJson.py data_directory tournament_name online/LAN isArena")
    else:
        data_dir = sys.argv[1]
        
        
        ticks = pd.read_csv(os.path.join(data_dir,"ticks.csv"))
        rounds = pd.read_csv(os.path.join(data_dir,"rounds.csv"))
        
        teams = get_teams(ticks)
        rounds = get_rounds_dict(rounds,ticks,teams)
        players = get_players(ticks, teams)
        map = get_map(data_dir)
        
        match_dict = {
            "teams":teams,
            "rounds":rounds,
            "players":players,
            "tournament": sys.argv[2],
            "type":sys.argv[3],
            "isArena":bool(sys.argv[4]),
            "map":map,
        }
        import json
        with open(data_dir+"/matchInfo.json", "w") as outfile: 
            json.dump(match_dict, outfile)
        
    
    # check_for_nans(ticks, data_dir)
    
    
    
    