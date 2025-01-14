import sys
import os
import json
import re

DB_FILE="players"
corrections = {}

def add_new_element_UX(element,element_list,team,element_type='player'):
    if element not in teamList:
        createNew = input(f"{element} not in {element_type} database. Team: {team}. Do you want to create new {element_type} named like that? (Y/N) ")
        if createNew=="Y":
            teamList.append(element)
        else:
            newName = input("Enter new name: ")
            # confirm = input(f"Correct {element} to {newName}? Change is irreversible (Y/N) ")
            # if confirm=="Y":
            corrections[element] = newName
            # else:
            #     add_new_element_UX(element,element_list,team,element_type)
            add_new_element_UX(newName,element_list,team,element_type)
            
def correct_file(filename,pre,post):
    # Read in the file
    with open(filename, 'r', encoding='utf-8') as file:
        filedata = file.read()
        
        # Replace using regular expression
    updated_data = filedata.replace(pre,post)
        # Write the updated content back to the file
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(updated_data)   

def correct_directory(dir,pre,post):
    for file in os.listdir(dir):
        correct_file(os.path.join(dir,file),pre,post)

def check_data_files(element_list):
    for subdir in os.listdir(sys.argv[1]):
        try:
            with open(os.path.join(sys.argv[1],subdir,"matchinfo.json"), 'r') as file:
                data = json.load(file)
            for team in data["teams"]:
                for player in data["players"][team]:
                    if player not in corrections:
                        add_new_element_UX(player,element_list,team)
                    if player in corrections:
                        print(f"Correcting {player} to {corrections[player]} in {subdir}")
                        correct_directory(os.path.join(sys.argv[1],subdir),player,corrections[player])

        except Exception as e:
            print(e)

def read_db():
    tl = []
    if os.path.isfile(DB_FILE):
        team_db = open(DB_FILE)
        for team in team_db:
            tl.append(team.rstrip())
        team_db.close()
    else:
        print(f"database file {DB_FILE} doesn't exist" ) 
    return tl         

def write_updated_db():
    team_db = open(DB_FILE,'w')
    for team in teamList:
        team_db.write(team+"\n")
    team_db.close()


if __name__ == "__main__":
    teamList = read_db()            
    check_data_files(teamList)
    write_updated_db()
