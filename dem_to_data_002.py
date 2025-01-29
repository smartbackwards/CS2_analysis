import sys
import os

from awpy import Demo
from dem_to_csv.extractCsv import save_csvs, save_csv
from utils.utils import check_for_nans, get_map 
from enhance_data.adjustCsv import add_round_winners, add_buy_types
from enhance_data.genJson import gen_JSON
from utils.stats import identify_and_mark_trade_kills

import json

def enhance_CSVs(target_dir, ticks_df, rounds_df, kills_df, tournament, type, is_arena):
    enhanced_rounds_df = add_round_winners(ticks_df, rounds_df)
    save_csv(enhanced_rounds_df, target_dir, "rounds")
    enhanced_rounds_df = add_buy_types(ticks_df, rounds_df, kills_df)
    save_csv(enhanced_rounds_df, target_dir, "rounds")
    enhanced_kills_df = identify_and_mark_trade_kills(kills_df, rounds_df)
    save_csv(enhanced_kills_df, target_dir, "kills")
    
    map = get_map(target_dir)
    match_dict = gen_JSON(ticks_df, rounds_df, tournament, type, is_arena, map)
    with open(target_dir+"/matchInfo.json", "w") as outfile: 
            json.dump(match_dict, outfile)



if __name__ == "__main__":
    # first argument - directory with dem files
    # second argument - target directory with CSV files
    # third argument - tournament name
    # fourth argument - online/LAN
    # fifth argument - is_arena
    
    if len(sys.argv)!=6:
        print("""
              usage: python dem_to_data_002.py <dir_with_dem> <target_dir> <tournament_name> <online/LAN> <is_arena>
              """)
        sys.exit()
    
    dem_directory = sys.argv[1]
    target_directory = sys.argv[2]
    
    for demo_file in os.listdir(dem_directory):
        file_path = os.path.join(dem_directory,demo_file)
        base_name = os.path.splitext(file_path)[0]
        target_dir = os.path.join(sys.argv[2],base_name)
        os.makedirs(target_dir, exist_ok=True)
        print(f"Parsing {base_name}")
        
        dem = Demo(file_path)
        save_csvs(dem,target_dir)
        
        # confirm integrity of the data
        try:
            check_for_nans(dem.ticks, base_name)
            enhance_CSVs(target_dir, dem.ticks,dem.rounds, dem.kills,
                         sys.argv[3], sys.argv[4], sys.argv[5])
            
        except Exception as e:
            print(e)
    
    