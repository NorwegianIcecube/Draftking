import gzip
import json
import requests
import time
import tqdm
from dotenv import load_dotenv
import os

load_dotenv()

# Set up Riot API key
api_key = os.getenv("RIOT_API_KEY")
print(api_key)
regions = ["br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na1", "oc1", "tr1", "ru"]
searched_matches = open("searched_matches.txt", "r+")
searched_matches_set = set(searched_matches.read().splitlines())
print("searched_matches_set length: " + str(len(searched_matches_set)))
#searched_matches_set = set()
#for line in searched_matches:
#    searched_matches_set.add(line.strip())
print("searched_matches_set length: ", len(searched_matches_set))
with gzip.open("data.json.gz", "ab") as f:
    f.write("[".encode("utf-8"))
    # Get all challenger, grandmaster, and master players
    for region in tqdm.tqdm(regions):
        #leagues = ["challenger", "grandmaster", "master"]
        leagues = ["challenger"]
        if region == "na1" or region == "br1" or region == "la1" or region == "la2":
            routing_v = "americas"
        elif region == "eun1" or region == "euw1" or region == "ru" or region == "tr1":
            routing_v = "europe"
        elif region == "jp1" or region == "kr":
            routing_v = "asia"
        elif region == "oc1":
            routing_v = "oce"
        # Open file to check if match is already read
        for league in tqdm.tqdm(leagues):
            players = requests.get("https://"+region+".api.riotgames.com/lol/league/v4/"+league+"leagues/by-queue/RANKED_SOLO_5x5?api_key="+api_key).json()
            #Get data for each player
            for player in tqdm.tqdm(players["entries"]):
                summoner_id = player["summonerId"]
                r=requests.get("https://"+region+".api.riotgames.com/lol/summoner/v4/summoners/"+summoner_id+"?api_key="+api_key).json()
                while r == {'status': {'message': 'Rate limit exceeded', 'status_code': 429}}:
                    print(" waiting")
                    time.sleep(20)
                    r=requests.get("https://"+region+".api.riotgames.com/lol/summoner/v4/summoners/"+summoner_id+"?api_key="+api_key).json()
                
                # Get match history for each player
                puuid = r["puuid"]
                match_ids = requests.get("https://"+routing_v+".api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?start=0&count=50&api_key="+api_key).json()
                while match_ids == {'status': {'message': 'Rate limit exceeded', 'status_code': 429}}:
                    print(" waiting")
                    time.sleep(20)
                    match_ids = requests.get("https://"+routing_v+".api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?start=0&count=100&api_key="+api_key).json()
            
                for match_id in match_ids:
                    #add match_id to searched_matches
                    if match_id not in searched_matches_set:
                        time.sleep(0.1)
                        match = requests.get("https://"+routing_v+".api.riotgames.com/lol/match/v5/matches/"+match_id+"?api_key="+api_key).json()
                        while match == {'status': {'message': 'Rate limit exceeded', 'status_code': 429}}:
                            #print(" waiting 10")
                            time.sleep(10)
                            match = requests.get("https://"+routing_v+".api.riotgames.com/lol/match/v5/matches/"+match_id+"?api_key="+api_key).json()
                        
                        #write data to file in the format specified in data_format.json
                        players = {}
                        for i in range(0,10):
                            try: 
                                players[f"player{i+1}"] = {"championName":match["info"]["participants"][i]["championName"],"teamId":match["info"]["participants"][i]["teamId"],"champLevel":match["info"]["participants"][i]["champLevel"],"kills":match["info"]["participants"][i]["kills"],"deaths":match["info"]["participants"][i]["deaths"],"assists":match["info"]["participants"][i]["assists"],"damageDealtToBuildings":match["info"]["participants"][i]["damageDealtToBuildings"],"damageDealtToObjectives":match["info"]["participants"][i]["damageDealtToObjectives"],"inhibitorsLost":match["info"]["participants"][i]["inhibitorsLost"],"damageSelfMitigated":match["info"]["participants"][i]["damageSelfMitigated"],"firstBloodKill":match["info"]["participants"][i]["firstBloodKill"],"firstTowerKill":match["info"]["participants"][i]["firstTowerKill"],"lane":match["info"]["participants"][i]["lane"],"magicDamageDealtToChampions":match["info"]["participants"][i]["magicDamageDealtToChampions"],"physicalDamageDealtToChampions":match["info"]["participants"][i]["physicalDamageDealtToChampions"],"trueDamageDealtToChampions":match["info"]["participants"][i]["trueDamageDealtToChampions"],"totalDamageDealtToChampions":match["info"]["participants"][i]["totalDamageDealtToChampions"],"magicDamageTaken":match["info"]["participants"][i]["magicDamageTaken"],"physicalDamageTaken":match["info"]["participants"][i]["physicalDamageTaken"],"totalDamageShieldedOnTeammates":match["info"]["participants"][i]["totalDamageShieldedOnTeammates"],"totalHealsOnTeammates":match["info"]["participants"][i]["totalHealsOnTeammates"],"timeCCingOthers":match["info"]["participants"][i]["timeCCingOthers"],"win":match["info"]["participants"][i]["win"]}
                            except:
                                players[f"player{i+1}"] = {"championName":None,"teamId":None,"champLevel":None,"kills":None,"deaths":None,"assists":None,"damageDealtToBuildings":None,"damageDealtToObjectives":None,"inhibitorsLost":None,"damageSelfMitigated":None,"firstBloodKill":None,"firstTowerKill":None,"lane":None,"magicDamageDealtToChampions":None,"physicalDamageDealtToChampions":None,"trueDamageDealtToChampions":None,"totalDamageDealtToChampions":None,"magicDamageTaken":None,"physicalDamageTaken":None,"totalDamageShieldedOnTeammates":None,"totalHealsOnTeammates":None,"timeCCingOthers":None,"win":None}
                        try:
                            dataDict = {"matchId":match["metadata"]["matchId"], "gameDuration":match["info"]["gameDuration"], "gameversion":match["info"]["gameVersion"],"players":players}
                        except:
                            dataDict = {"matchId":match_id, "gameDuration":None, "gameversion":None,"players":players}
                        f.write(json.dumps(dataDict+",").encode("utf-8"))
                        searched_matches.write(match_id+"\n")
                        searched_matches_set.add(match_id)
    f.write("]".encode("utf-8"))
searched_matches.close()