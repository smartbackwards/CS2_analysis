
from awpy import Demo
import pandas as pd

def save_csvs(dem: Demo, target_dir: str):
    dem.bomb.to_csv(target_dir+"/bomb.csv")
    dem.damages.to_csv(target_dir+"/damages.csv")
    dem.grenades.to_csv(target_dir+"/grenades.csv")
    dem.infernos.to_csv(target_dir+"/infernos.csv")
    dem.kills.to_csv(target_dir+"/kills.csv")
    dem.rounds.to_csv(target_dir+"/rounds.csv")
    dem.smokes.to_csv(target_dir+"/smokes.csv")
    dem.ticks.to_csv(target_dir+"/ticks.csv")
    dem.weapon_fires.to_csv(target_dir+"/weapon_fires.csv")

def save_csv(df: pd.DataFrame, target_dir: str, df_name: str):
    df.to_csv(f'{target_dir}/{df_name}.csv')
    