import pandas as pd
import os


def assign_rounds(df: pd.DataFrame, df_rounds: pd.DataFrame, tick="tick"):
    for _, row in df_rounds.iterrows():
        round_num = row['round']  
        start_tick = row['start']  
        end_tick = row['official_end']      
        df.loc[(df[tick] >= start_tick) & (df[tick] <= end_tick), 'round'] = round_num
    return df

def fix_CSVs(data_dir):
    CSVs = ("bomb", "damages","grenades","kills","ticks","weapon_fires")
    start_tick_CSVs = ("infernos","smokes",)


    rounds = pd.read_csv(os.path.join(data_dir,"rounds.csv"))
    for CSV in CSVs:
        df = assign_rounds(pd.read_csv(os.path.join(data_dir,f"{CSV}.csv")),rounds)
        print(f"adjusting {CSV}")
        df.to_csv(os.path.join(data_dir,f"{CSV}.csv"))

    for CSV in start_tick_CSVs:
        df = assign_rounds(pd.read_csv(os.path.join(data_dir,f"{CSV}.csv")),rounds,"start_tick")
        print(f"adjusting {CSV}")
        df.to_csv(os.path.join(data_dir,f"{CSV}.csv"))