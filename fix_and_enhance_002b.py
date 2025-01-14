from dem_to_data_002 import enhance_CSVs
from enhance_data.fixCsv import fix_CSVs
import sys
import pandas as pd

if __name__ == "__main__":
    if len(sys.argv)==5:
        fix_CSVs(sys.argv[1])
        
        ticks = pd.read_csv(sys.argv[1]+"/ticks.csv")
        kills = pd.read_csv(sys.argv[1]+"/kills.csv")
        rounds = pd.read_csv(sys.argv[1]+"/rounds.csv")
        enhance_CSVs(sys.argv[1],ticks,rounds,kills,sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("provide arguments: directory with data, tournament name, online/LAN, is_arena")