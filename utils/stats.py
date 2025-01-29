import pandas as pd
from typing import Literal
CT_SIDE_ALIASES = ("CT", "COUNTER-TERRORISTS")
T_SIDE_ALIASES = ("T", "TERRORIST")

def analyse_round_clawback_bozo(round_df: pd.DataFrame, round_winner: Literal["CT","T"]):
    """
        round_df - df containing kills from a given round
        round_winner - str with round_winner
    """
    global CT_SIDE_ALIASES, T_SIDE_ALIASES
    # clawback-bozo logic:
    # only count kills when:
    #   team A wins round
    #   team B is in a man advantage
    #   player from team B dies
    CT_alive = 5
    T_alive = 5
    cbk = []
    for id,row in round_df.iterrows():
        if (round_winner == "CT" and T_alive>CT_alive and row["victim_team_name"] in T_SIDE_ALIASES) \
            or (round_winner == "T" and CT_alive>T_alive and row["victim_team_name"] in CT_SIDE_ALIASES):
            row["CT_alive"]=CT_alive
            row["T_alive"]=T_alive
            cbk.append(row)

        if row["victim_team_name"] in CT_SIDE_ALIASES:
            CT_alive -= 1
        elif row["victim_team_name"] in T_SIDE_ALIASES:
            T_alive -= 1
        else:
            print(f"unknown side {row['victim_team_name']}")
    return pd.DataFrame(cbk)


    # print(round_winner)


def analyse_df_clawback_bozo(kills_df,rounds_df):
    cbk_df = []
    for id, row in rounds_df.iterrows():
        round_kill_df = kills_df[kills_df["round"]==row["round"]]
        winner = row["winner"]
        cbk_df.append(analyse_round_clawback_bozo(round_kill_df, winner))        
    return pd.concat(cbk_df)


def analyse_round_even_situation(round_df):
    global CT_SIDE_ALIASES, T_SIDE_ALIASES
    CT_alive = 5
    T_alive = 5
    cbk = []
    for id,row in round_df.iterrows():
        if CT_alive == T_alive:
            row["CT_alive"]=CT_alive
            row["T_alive"]=T_alive
            cbk.append(row)

        if row["victim_team_name"] in CT_SIDE_ALIASES:
            CT_alive -= 1
        elif row["victim_team_name"] in T_SIDE_ALIASES:
            T_alive -= 1
        else:
            print(f"unknown side {row['victim_team_name']}")
    return pd.DataFrame(cbk)

def analyse_df_even(kills_df,rounds_df):
    cbk_df = []
    for round in rounds_df["round"].to_list():
        round_df = kills_df[kills_df["round"]==round]
        cbk_df.append(analyse_round_even_situation(round_df))
    cbk_df = pd.concat(cbk_df)
    return cbk_df

def get_ADR(df,player,round_count):
    df_a = df[df["attacker_team_name"]!=df["victim_team_name"]]
    return df_a[df_a["attacker_name"]==player]["dmg_health_real"].sum()/round_count

def identify_and_mark_trade_kills(kills_df, rounds_df, time_window=5, ticks_per_second=64):
    """
    Identifies and marks only the last kill of an engagement as traded in a DataFrame.

    Parameters:
        df (pd.DataFrame): A DataFrame containing columns:
                          - 'attacker_name', 'victim_name', 'tick', 'attacker_team_name', 'victim_team_name'.
        time_window (int): Time window in seconds for identifying trade kills.
        ticks_per_second (int): Number of ticks per second in the game.

    Returns:
        pd.DataFrame: A DataFrame with two new columns:
                      - 'is_traded': True if the kill was traded, otherwise False.
                      - 'trader_name': Name of the player responsible for the trade (or None if not traded).
    """
    # Add new columns with default values
    kills_df['is_traded'] = False
    kills_df['trader_name'] = None

    time_ticks = time_window * ticks_per_second

    for id, row in rounds_df.iterrows():
        df = kills_df[kills_df["round"]==row["round"]]
        for i, (index, kill) in enumerate(df.iterrows()):
            # Skip team kills
            if kill['attacker_team_name'] == kill['victim_team_name']:
                continue
            
            # Define the time window
            end_tick = kill['tick']
            start_tick = end_tick - time_ticks
            
            # Find all potential trades within the time window
            possible_trade = df[(df['tick'] >= start_tick) & 
                                (df['tick'] <= end_tick) & 
                                (df['attacker_team_name'] != df['victim_team_name']) &
                                (df['attacker_name'] == kill['victim_name'])
                                ]
            
            
            if not possible_trade.empty:
                last_kill_index = possible_trade.index[-1]
                
                kills_df.at[last_kill_index, 'is_traded'] = True
                kills_df.at[last_kill_index, 'trader_name'] = kill['attacker_name']
            
    return kills_df