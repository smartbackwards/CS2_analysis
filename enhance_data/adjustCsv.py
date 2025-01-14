import pandas as pd
import sys
import os

def add_round_winners(ticks_df, rounds_df):
    for id, row in rounds_df.iterrows():
        freeze_end_tick = row["freeze_end"]
        winner = row["winner"]
        
        first_tick_df = ticks_df[ticks_df["tick"]==freeze_end_tick]
        CT_team = first_tick_df[first_tick_df["team_name"]=="CT"]["team_clan_name"].iloc[0]
        T_team = first_tick_df[first_tick_df["team_name"]=="TERRORIST"]["team_clan_name"].iloc[0]

        rounds_df.loc[id,"CT_team_clan_name"] = CT_team
        rounds_df.loc[id,"T_team_clan_name"] = T_team
        rounds_df.loc[id,"winner_clan_name"] = CT_team if winner=="CT" else T_team
        
    return rounds_df   

TIER_ONE_GUNS=('AK-47', 'AWP', 'M4A1-S', 'M4A4', 'AUG', 'SG 553', 'G3SG1', 'SCAR-20')
def check_full_gun(list_of_inventories):
    count = 0
    for inv in list_of_inventories:
        count += any(item in inv for item in TIER_ONE_GUNS)
    return count==5

def add_buy_types(ticks_df, rounds_df, kills_df):
    for id, row in rounds_df.iterrows():
        round_no = row["round"] 
        freeze_end = row["freeze_end"]
        
        kill_ticks = kills_df[kills_df["round"]==round_no]["tick"]
        if len(kill_ticks) > 0:
            econ_tick = min(freeze_end+20*64, (kill_ticks.iloc[0])-1)
        else:
            econ_tick = freeze_end+20*64
        
        econ_tick_df = ticks_df[ticks_df["tick"]==econ_tick]
        
        T_econ = econ_tick_df[econ_tick_df["team_name"]=="TERRORIST"]
        CT_econ = econ_tick_df[econ_tick_df["team_name"]=="CT"]
        
        rounds_df.loc[id,"CT_average_economy"] = CT_econ["current_equip_value"].mean()
        rounds_df.loc[id,"T_average_economy"] = T_econ["current_equip_value"].mean()
        rounds_df.loc[id,"CT_full_gun_round"] = check_full_gun(CT_econ["inventory"])
        rounds_df.loc[id,"T_full_gun_round"] = check_full_gun(T_econ["inventory"])
        
    return rounds_df

