# takes DEM file as first argument, target folder as second
from awpy import Demo
import sys
import os

def save_csvs(dem, target_dir):
    dem.bomb.to_csv(target_dir+"/bomb.csv")
    dem.damages.to_csv(target_dir+"/damages.csv")
    dem.grenades.to_csv(target_dir+"/grenades.csv")
    dem.infernos.to_csv(target_dir+"/infernos.csv")
    dem.kills.to_csv(target_dir+"/kills.csv")
    dem.rounds.to_csv(target_dir+"/rounds.csv")
    dem.smokes.to_csv(target_dir+"/smokes.csv")
    dem.ticks.to_csv(target_dir+"/ticks.csv")
    dem.weapon_fires.to_csv(target_dir+"/weapon_fires.csv")
    
if __name__ == "__main__":
    demo_file_path = sys.argv[1]
    base_name = os.path.splitext(demo_file_path)[0]
    target_dir = os.path.join(sys.argv[2],base_name)
    os.makedirs(target_dir, exist_ok=True)

    print(f"Parsing {base_name}")
    
    dem = Demo(demo_file_path)
    save_csvs(dem,target_dir)
    
    