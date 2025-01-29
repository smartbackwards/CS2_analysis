import pandas as pd

def get_style_dict():
    df = pd.read_csv("./team_style_sheet.csv")
    style_dict = {}
    for id, row in df.iterrows():
        style_dict[row["team"]] = {
            "primary_color": row["primary_color"],
            "secondary_color": row["secondary_color"]
        }
    return style_dict

def get_style_dict_2024():
    df = pd.read_csv("./team_style_sheet_2024.csv")
    style_dict = {}
    for id, row in df.iterrows():
        style_dict[row["team"]] = {
            "primary_color": row["primary_color"],
            "secondary_color": row["secondary_color"]
        }
    return style_dict