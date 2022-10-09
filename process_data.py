'''
champion
    has average winrates at time intervals
    has common positions x% top y% jg z% mid ...
    has aoe ultimate
    has average damage dealt at time intervals
    has average damage mitigated and taken at time intervals
    has average self healing at time intervals
    has average ally healing at time intervals
    has mtg colors?
    has average winrate at different numbers of games played
    has average kda
    has objective prowess
    has average turrets destroyed, and/or damage to structures
    has damage type split (physical%, magical%)
    has range
    has number of cc abilities?
'''



# Imports
import json
import gzip
import tqdm

# Globals


# Classes


# Functions
#function to get champion data from data.json.gz and add it to champions.json

#data was incorrectly formatted, so this function fixes it
def fix_data():
    matches = []
    with open ("searched_matches.txt", "r") as f:
        searched_matches = f.read().splitlines()
    searched_matches_set = set(searched_matches)
    
    with gzip.open("data.json.gz", "rb") as f:
        data = f.read().decode("utf-8")
        open_brackets = 0
        i = 0
        for j in tqdm.tqdm(range(len(searched_matches_set))):
            data_element = ""
            while True:
                if data[i] == "{":
                    open_brackets += 1
                elif data[i] == "}":
                    open_brackets -= 1
                    if open_brackets == 0:
                        data_element += data[i]
                        i += 1
                        matches.append(data_element)
                        break
                data_element = data_element + data[i]
                i += 1
    with gzip.open("data.json.gz", "wb") as f:
        f.write(json.dumps(matches).encode("utf-8"))
        

def get_champion_data():
    #open data.json.gz
    with gzip.open('data.json.gz', 'rb') as f:
        data = json.load(f)
    #reset champions.json
    with open('champions.json', 'w') as f:
        f.write('')
        
    #open champions.json
    with open('champions.json', 'r') as f:
        champions = json.load(f)
    #loop through data
    for match in data:
        #if gamelength is less than 300, skip
        if match['gameDuration'] < 300:
            continue
        #loop through participants
        for player in match['players']:
            #get champion id
            champion_name = player['championName']
            #if champion id not in champions
            if champion_name not in champions:
                #add champion id to champions
                champions[champion_name] = {}
            #add number of games played to champion
            if 'games_played' not in champions[champion_name]:
                champions[champion_name]['games_played'] = 1
            else:
                champions[champion_name]['games_played'] += 1
            #add wins to champion
            if 'wins' not in champions[champion_name]:
                champions[champion_name]['wins'] = 0
            if player['win']:
                champions[champion_name]['wins'] += 1
            

    #open champions.json
    with open('champions.json', 'w') as f:
        #write champions to champions.json
        json.dump(champions, f, indent=4)
    #return champions
    return champions 

