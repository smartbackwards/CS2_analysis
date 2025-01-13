import pandas as pd
import sys
import os

CSVs = ("bomb", "damages","grenades","kills","ticks","weapon_fires")
start_tick_CSVs = ("infernos","smokes",)
def assign_rounds(df, df_ranges, tick="tick"):
    # Iterate through each range in df_ranges
    for _, row in df_ranges.iterrows():
        round_num = row['round']  # Value to assign
        start_tick = row['start']  # Start of the range
        end_tick = row['official_end']      # End of the range
        # Assign 'round' where 'tick' falls within the range
        df.loc[(df[tick] >= start_tick) & (df[tick] <= end_tick), 'round'] = round_num

    return df

rounds = pd.read_csv(os.path.join(sys.argv[1],"rounds.csv"))
for CSV in CSVs:
    df = assign_rounds(pd.read_csv(os.path.join(sys.argv[1],f"{CSV}.csv")),rounds)
    print(f"adjusting {CSV}")
    df.to_csv(os.path.join(sys.argv[1],f"{CSV}.csv"))

for CSV in start_tick_CSVs:
    df = assign_rounds(pd.read_csv(os.path.join(sys.argv[1],f"{CSV}.csv")),rounds,"start_tick")
    print(f"adjusting {CSV}")
    df.to_csv(os.path.join(sys.argv[1],f"{CSV}.csv"))