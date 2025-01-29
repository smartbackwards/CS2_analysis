import pandas as pd
import os
from utils.utils import get_match_info
from utils.stats import analyse_round_even_situation, analyse_round_clawback_bozo

TOURNAMENT_DIRS = ["anubis_csv/anubis_dem"]#["E:/Tier1_2025/BLAST Bounty Season 1/","E:/Tier1_2025/BLAST Bounty Season 1 Finals/"]

def get_buy_round_ADR():
    results = {}
    
    for TOURNAMENT_DIR in TOURNAMENT_DIRS:
        for map_dir in os.listdir(TOURNAMENT_DIR):
            rounds = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"rounds.csv"))
            damages = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"damages.csv"))
            match_info = get_match_info(os.path.join(TOURNAMENT_DIR,map_dir))
            teams = match_info["teams"]
            
            damages = damages[damages["attacker_team_name"]!=damages["victim_team_name"]]
            
            buy_round_ids = []
            
            for id, row in rounds.iterrows():
                if row["T_average_economy"]>=3800 and row["CT_average_economy"]>=3800:
                    buy_round_ids.append(row["round"])
            
            buy_round_damages = damages[damages["round"].isin(buy_round_ids)]
            
            for team in teams:
                for player in match_info["players"][team]:
                    if player not in results:
                        results[player] = {
                            "buy_rounds": 0,
                            "buy_round_damage":0,
                            "rounds":0,
                            "damage":0,
                            "team":team
                            # "anti_eco_rounds":0,
                            # "anti_eco_damage":0
                        }

                    results[player]["buy_rounds"] += len(buy_round_ids)
                    
                    results[player]["buy_round_damage"] += (buy_round_damages[buy_round_damages["attacker_name"]==player]["dmg_health_real"]).sum()
                    
                    results[player]["rounds"] += match_info["rounds"][team]["roundsPlayed"]
                    
                    results[player]["damage"] += (damages[damages["attacker_name"]==player]["dmg_health_real"]).sum()
    return results

def get_eco_bashers():
    results = {}
    
    for TOURNAMENT_DIR in TOURNAMENT_DIRS:
        for map_dir in os.listdir(TOURNAMENT_DIR):
            rounds = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"rounds.csv"))
            kills = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"kills.csv"))
            damages = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"damages.csv"))
            match_info = get_match_info(os.path.join(TOURNAMENT_DIR,map_dir))
            teams = match_info["teams"]
            
            damages = damages[damages["attacker_team_name"]!=damages["victim_team_name"]]
            
            for id, row in rounds.iterrows():
                if row["T_average_economy"]>=3800 and row["CT_average_economy"]<1600:
                    anti_eco_team = row["T_team_clan_name"]
                elif row["CT_average_economy"]>=3800 and row["T_average_economy"]<1600:
                    anti_eco_team = row["CT_team_clan_name"]
                else:
                    anti_eco_team = None
                    
                if anti_eco_team:
                    round_damages = damages[damages["round"]==row["round"]]
                    round_kills = kills[kills["round"]==row["round"]]
                    for player in match_info["players"][anti_eco_team]:
                        if player not in results:
                            results[player] = {
                                "kills":0,
                                "rounds":0,
                                "damage":0,
                                "deaths":0 
                            }
                            
                        results[player]["rounds"]+=1
                        results[player]["damage"]+=(round_damages[round_damages["attacker_name"]==player]["dmg_health_real"]).sum()
                        results[player]["kills"]+=(round_kills[round_kills["attacker_name"]==player]["attacker_name"]).count()
                        results[player]["deaths"] += (round_kills[round_kills["victim_name"]==player]["victim_name"]).count()

    return results

def get_player_positions_on_map(queried_player, queried_map, only_CT = True):
    results = {}
    
    for TOURNAMENT_DIR in TOURNAMENT_DIRS:
        for map_dir in os.listdir(TOURNAMENT_DIR):            
            match_info = get_match_info(os.path.join(TOURNAMENT_DIR,map_dir))
            
            if match_info["map"] != queried_map:
                continue  # Skip to the next map_dir
            
            contains_player = False
            for team in match_info["teams"]:
                for player in match_info["players"][team]:
                    if player == queried_player:
                        contains_player = True
                        break  # Break inner player loop
                
                if contains_player:
                    break  # Break team loop
            
            if not contains_player:
                continue  # Skip to the next map_dir
            
            ticks = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"ticks.csv"))
            ticks = ticks[ticks["name"]==queried_player]
            ticks = ticks[ticks["health"]>0]
            if only_CT:
                ticks = ticks[ticks["team_name"]=="CT"]
            
            for id, row in ticks.iterrows():
                if row["last_place_name"] not in results:
                    results[row["last_place_name"]] = 0
                    
                results[row["last_place_name"]]+=1
    
    return results

def get_opening_frag_stats():
    results = {}
    
    for TOURNAMENT_DIR in TOURNAMENT_DIRS:
        for map_dir in os.listdir(TOURNAMENT_DIR):
            rounds = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"rounds.csv"))
            kills = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"kills.csv"))
            
            match_info = get_match_info(os.path.join(TOURNAMENT_DIR,map_dir))
            teams = match_info["teams"]
            
            for team in teams:
                for player in match_info["players"][team]:
                    if player not in results:
                        results[player] = {
                            "team":team,
                            "roundsPlayed":0,
                            "openingKills":0,
                            "openingDeaths":0,
                            "untradedOpeningKills":0,
                            "untradedOpeningDeaths":0,
                            
                            
                            
                        }

                    results[player]["roundsPlayed"] += match_info["rounds"][team]["roundsPlayed"]
            
            for id, row in rounds.iterrows():
                round_kills = kills[kills["round"]==row["round"]]
                
                if not round_kills.empty:
                    first_kill = round_kills.head(1)
                    
                    if first_kill["attacker_team_name"].iloc[0] != first_kill["victim_team_name"].iloc[0]:
                    
                        killer = first_kill["attacker_name"].iloc[0]
                        victim = first_kill["victim_name"].iloc[0]
                        
                        results[killer]["openingKills"] += 1
                        results[victim]["openingDeaths"] += 1
                        
                        if not first_kill["is_traded"].iloc[0]:
                            results[killer]["untradedOpeningKills"] += 1
                            results[victim]["untradedOpeningDeaths"] += 1
                        
                        # if first_kill["attacker_team_name"]==
                    
    return results                            


def kills_per_round_won():
    results = {}
    
    for TOURNAMENT_DIR in TOURNAMENT_DIRS:
        for map_dir in os.listdir(TOURNAMENT_DIR):
            rounds = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"rounds.csv"))
            kills = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"kills.csv"))
            
            match_info = get_match_info(os.path.join(TOURNAMENT_DIR,map_dir))
            teams = match_info["teams"]
            
            for team in teams:
                rounds_won = []
                for id, row in rounds.iterrows():
                        if row["winner_clan_name"]==team:
                            rounds_won.append(row["round"])
                kills_in_wins = kills[kills["round"].isin(rounds_won)]
                kills_in_wins = kills_in_wins[kills_in_wins["attacker_team_name"]!=kills_in_wins["victim_team_name"]]
                for player in match_info["players"][team]:
                    if player not in results:
                        results[player] = {
                            "team":team,
                            "roundsWon":0,
                            "killsInRoundsWon":0,
                            # "openingDeaths":0,
                            # "untradedOpeningKills":0,
                            # "untradedOpeningDeaths":0
                        }              
                    results[player]["killsInRoundsWon"] += (kills_in_wins[kills_in_wins["attacker_name"]==player]["attacker_name"]).count()       
                    results[player]["roundsWon"] += match_info["rounds"][team]["roundsWon"]
                
    return results
                            
def get_traded_even_state_stats():
    results = {}
    
    for TOURNAMENT_DIR in TOURNAMENT_DIRS:
        for map_dir in os.listdir(TOURNAMENT_DIR):
            rounds = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"rounds.csv"))
            kills = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"kills.csv"))
            
            match_info = get_match_info(os.path.join(TOURNAMENT_DIR,map_dir))
            teams = match_info["teams"]
            
            for team in teams:
                for player in match_info["players"][team]:
                    if player not in results:
                        results[player] = {
                            "team":team,
                            "roundsPlayed":0,
                            "evenKills":0,
                            "evenDeaths":0,
                            "untradedEvenKills":0,
                            "untradedEvenDeaths":0
                        }

                    results[player]["roundsPlayed"] += match_info["rounds"][team]["roundsPlayed"]
            
            for id, row in rounds.iterrows():
                round_kills = kills[kills["round"]==row["round"]]
                
                ek = analyse_round_even_situation(round_kills)
                for id, row in ek.iterrows():
                    attacker = row["attacker_name"]
                    
                    if str(attacker)!="nan" and row["attacker_team_name"]!=row["victim_team_name"]:
                        results[attacker]["evenKills"] += 1
                    results[row["victim_name"]]["evenDeaths"] += 1
                    
                    if not row["is_traded"]:
                        if str(attacker)!="nan" and row["attacker_team_name"]!=row["victim_team_name"]:
                            results[attacker]["untradedEvenKills"] += 1
                        results[row["victim_name"]]["untradedEvenDeaths"] += 1
                    
    return results                    

def get_traded_clawback_bozo_stats():
    results = {}
    
    for TOURNAMENT_DIR in TOURNAMENT_DIRS:
        for map_dir in os.listdir(TOURNAMENT_DIR):
            rounds = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"rounds.csv"))
            kills = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"kills.csv"))
            
            match_info = get_match_info(os.path.join(TOURNAMENT_DIR,map_dir))
            teams = match_info["teams"]
            
            for team in teams:
                for player in match_info["players"][team]:
                    if player not in results:
                        results[player] = {
                            "team":team,
                            "roundsPlayed":0,
                            "clawbackKills":0,
                            "bozoDeaths":0,
                            "untradedClawbackKills":0,
                            "untradedBozoDeaths":0
                        }

                    results[player]["roundsPlayed"] += match_info["rounds"][team]["roundsPlayed"]
            
            for id, row in rounds.iterrows():
                round_kills = kills[kills["round"]==row["round"]]
                
                cbk = analyse_round_clawback_bozo(round_kills,row['winner'])
                for id, row in cbk.iterrows():
                    attacker = row["attacker_name"]
                    
                    if str(attacker)!="nan" and row["attacker_team_name"]!=row["victim_team_name"]:
                        results[attacker]["clawbackKills"] += 1
                    results[row["victim_name"]]["bozoDeaths"] += 1
                    
                    if not row["is_traded"]:
                        if str(attacker)!="nan" and row["attacker_team_name"]!=row["victim_team_name"]:
                            results[attacker]["untradedClawbackKills"] += 1
                        results[row["victim_name"]]["untradedBozoDeaths"] += 1
                    
    return results 

def get_team_damage():
    results = {}
    
    for TOURNAMENT_DIR in TOURNAMENT_DIRS:
        for map_dir in os.listdir(TOURNAMENT_DIR):
            kills = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"kills.csv"))
            damages = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"damages.csv"))
            
            match_info = get_match_info(os.path.join(TOURNAMENT_DIR,map_dir))
            teams = match_info["teams"]
            
            for team in teams:
                for player in match_info["players"][team]:
                    if player not in results:
                        results[player] = {
                            "team":team,
                            "roundsPlayed":0,
                            "teamDamage":0,
                            "teamKills":0
                        }
                    results[player]["roundsPlayed"] += match_info["rounds"][team]["roundsPlayed"]
            
            team_damage = damages[damages["attacker_team_name"]==damages["victim_team_name"]]
            team_kills = kills[kills["attacker_team_name"]==kills["victim_team_name"]]
            
            for id, row in team_damage.iterrows():
                results[row["attacker_name"]]["teamDamage"] += row["dmg_health_real"]
            
            for id, row in team_kills.iterrows():
                results[row["attacker_name"]]["teamKills"] += 1
    return results

def get_time_alive():
    results = {}
    
    for TOURNAMENT_DIR in TOURNAMENT_DIRS:
        for map_dir in os.listdir(TOURNAMENT_DIR):
            print(map_dir)
            
            
            match_info = get_match_info(os.path.join(TOURNAMENT_DIR,map_dir))
            teams = match_info["teams"]
            
            # if "M80" not in teams:
            #     continue
            rounds = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"rounds.csv"))
            ticks = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"ticks.csv"))
            for team in teams:
                roundsLost = []
                roundsWon = []
                for id, row in rounds.iterrows():
                    if team != row["winner_clan_name"]:
                        roundsLost.append(row["round"])
                    else:
                        roundsWon.append(row["round"])
                        
                rw_ticks = ticks[ticks["round"].isin(roundsWon)]
                rl_ticks = ticks[ticks["round"].isin(roundsLost)]
                # roundsLost = match_info["rounds"][team]["roundsPlayed"]-match_info["rounds"][team]["roundsWon"]
                for player in match_info["players"][team]:
                    if player not in results:
                        results[player] = {
                            "team":team,
                            "roundsPlayed":0,
                            "roundsLost":0,
                            "ticksAlive":0,
                            "ticksAliveInRoundsLost":0
                        }
                    results[player]["roundsPlayed"] += match_info["rounds"][team]["roundsPlayed"]
                    results[player]["roundsLost"] += len(roundsLost)
                    
                    rlt = rl_ticks[rl_ticks["name"]==player]
                    rwt = rw_ticks[rw_ticks["name"]==player]
                    
                    ticksInRoundsLost = rlt[rlt["health"]>0]["name"].count()
                    ticksInRoundsWon = rwt[rwt["health"]>0]["name"].count()
                    
                    # print(f"{player},{len(roundsLost)},{len(roundsLost)+len(roundsWon)},{ticksInRoundsLost},{ticksInRoundsWon}")
                    results[player]["ticksAlive"] += ticksInRoundsLost+ticksInRoundsWon
                    results[player]["ticksAliveInRoundsLost"] += ticksInRoundsLost
    return results
                                        
def get_kobe():
    results = {}
    
    for TOURNAMENT_DIR in TOURNAMENT_DIRS:
        for map_dir in os.listdir(TOURNAMENT_DIR):
            damages = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"damages.csv"))
            
            damages = damages[damages["weapon"]=="hegrenade"]
            
            dmg = damages.groupby(['tick', 'attacker_name', "round"], as_index=False)['dmg_health_real'].sum()
            for id, row in dmg.iterrows():
                if row["dmg_health_real"]>=130:
                    print(row["attacker_name"], row["round"], map_dir, row["dmg_health_real"])                 

def get_AWP_efficiency(no_no_scopes=False):
    results = {}
    
    for TOURNAMENT_DIR in TOURNAMENT_DIRS:
        for map_dir in os.listdir(TOURNAMENT_DIR):
            weapon_fires = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"weapon_fires.csv"))
            damages = pd.read_csv(os.path.join(TOURNAMENT_DIR,map_dir,"damages.csv"))
            
            match_info = get_match_info(os.path.join(TOURNAMENT_DIR,map_dir))
            teams = match_info["teams"]
            
            for team in teams:
                for player in match_info["players"][team]:
                    if player not in results:
                        results[player] = {
                            "team":team,
                            "roundsPlayed":0,
                            "awpShotsHit":0,
                            "awpShots":0,
                            "legShots":0,
                        }
                    results[player]["roundsPlayed"] += match_info["rounds"][team]["roundsPlayed"]
                
            weapon_fires_awp = weapon_fires[weapon_fires["weapon"]=="weapon_awp"]
            if no_no_scopes:
                weapon_fires_awp = weapon_fires_awp[weapon_fires_awp["player_zoom_lvl"]>0]
            
            for id, row in weapon_fires_awp.iterrows():
                if str(row["player_name"])!= "nan":
                    results[row["player_name"]]["awpShots"]+=1
            
            damages_awp = damages[damages["weapon"]=="awp"]
                    
                    
                    
            merged = pd.merge(
                weapon_fires_awp,
                damages_awp,
                left_on=["tick", "player_name"],
                right_on=["tick", "attacker_name"],
                how="inner"
            )
            unique_hits = merged[["tick", "player_name"]].drop_duplicates()
            
            for id, row in unique_hits.iterrows():
                results[row["player_name"]]["awpShotsHit"]+=1
            
            for id, row in damages_awp.iterrows():
                if row["dmg_health"]<100:
                    results[row["attacker_name"]]["legShots"]+=1
    return results

awp = get_AWP_efficiency()     
for player in awp:
    data = awp[player]
    if data["awpShots"]>0:
        print(f'{player},{data["roundsPlayed"]},{data["awpShotsHit"]},{data["awpShots"]},{data["legShots"]}')

     
# time_alive = get_time_alive()
# get_kobe()
# for player in time_alive:
#     data = time_alive[player]
#     print(f'{player},{data["roundsPlayed"]},{data["roundsLost"]},{data["ticksAlive"]},{data["ticksAliveInRoundsLost"]},')
# # def get_most_time_alive():
    