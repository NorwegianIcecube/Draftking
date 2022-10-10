import requests
import numpy as np
import tkinter as tk
import cassiopeia as cass
import pandas as pd
import json
import cassiopeia_championgg as cassgg
from dotenv import load_dotenv
import os

load_dotenv()

# Set up Riot API key
api_key = os.getenv("RIOT_API_KEY")

#champion class
class Champion:
    def __init__(self, name):
        self.name = name
        self.champion = cass.get_champion(name, region="EUW")
        #get win rate of champion
        self.winrate = self.champion.win_rates
        print(self.winrate)
        #self.winrate = cass.get_champion(name)#.win_rate
        '''
        #determine roles champion can play
        self.roles = []
        if self.champion.roles.top:
            self.roles.append("top")
        if self.champion.roles.jungle:
            self.roles.append("jungle")
        if self.champion.roles.mid:
            self.roles.append("mid")
        if self.champion.roles.adc:
            self.roles.append("adc")
        if self.champion.roles.support:
            self.roles.append("support")

        #determine if champion has an aoe ult
        self.aoe_ult = False
        if self.champion.ult.aoe:
            self.aoe_ult = True
 
        #implement "mtg color" identity of champion
        # 0 = none, 1 = red, 2 = blue, 3 = green, 4 = black, 5 = white
         
        
    def winrate_vs(self, enemy):
        #get win rate of champion vs enemy
        return self.champion.win_rate_vs(enemy)

    def winrate_with(self, ally):
        #get win rate of champion with ally
        return self.champion.win_rate_with(ally)
    '''
        

#add the entries to the listbox
def update_listbox(side):
    if side == "Blue":
        blue_listbox.insert("end", "Blue: " + entry_list[-1][0] + " " + entry_list[-1][1])
    red_listbox.insert("end", "Red: " + entry_list[-1][0] + " " + entry_list[-1][1])

#add entry to dictionary when submit button is pressed
def add_entry():
    e = entry.get()
    #return if entry is not in the list of champions
    if e.lower() not in champions_lower:
        return
    #entry should be in the format (pick/ban, champion)
    if len(entry_list) < 6: 
        pickban ="Ban"
    elif len(entry_list) <12:
        pickban = "Pick"
    elif len(entry_list) < 16:
        pickban = "Ban"
    else: pickban = "Pick"
    entry_list.append((pickban, e))
    entry.delete(0, "end")
    update_listbox(order[len(entry_list)-1])

def add_summoner():
    summoner_listbox.insert("end", side.get() + ": " + summoner_entry.get())
    summoner_entry.delete(0, "end")
    summoners[summoner_entry.get()] = side.get()

#get list of all champions
def get_champion_list():
    r = requests.get("http://ddragon.leagueoflegends.com/cdn/10.24.1/data/en_US/champion.json")
    champions = r.json()["data"].keys()
    champion_map = (map(lambda x: x.lower(), champions))
    champions_lower = list(champion_map)
    return champions, champions_lower

def check_for_wukong(champion):
    if champion == "wukong":
        return "monkeyking"
    return champion

#list of all champions
champions, champions_lower = get_champion_list()
#dict of all champions as Champion objects
champion_dict = {}
for champion in champions:
    champion_dict[champion] = Champion(champion)

#create an empty gui with dimensions 1400x800 with a white background
root = tk.Tk()
root.geometry("1400x800")
root.configure(bg="white")

#add a label to the gui
label = tk.Label(root, text="Champion Select Assistant", bg="white", fg="black", font=("Arial", 20))
label.pack()

#add an input field
entry = tk.Entry(root, width=50)
#add a label to the input field
entry_label = tk.Label(root, text="Enter champion name", bg="white", fg="black", font=("Arial", 15))
entry_label.pack()
entry.pack()

#add two listboxes side by side to the gui
blue_listbox = tk.Listbox(root, width=50)
red_listbox = tk.Listbox(root, width=50)
#create a label for each listbox
blue_label = tk.Label(root, text="Blue Team", bg="white", fg="black", font=("Arial", 20))
red_label = tk.Label(root, text="Red Team", bg="white", fg="black", font=("Arial", 20))
#add the listboxes side by side and labels above them to the gui
blue_label.pack(side="left")
blue_listbox.pack(side="left")
red_label.pack(side="right")
red_listbox.pack(side="right")

#add a submit button. Entry_list is a list of tuples containing the side, pick/ban, and champion, it is where the submission is stored. Order is a list determining the order of the picks/bans
entry_list = []
order = ["Blue","Red","Blue","Red","Blue","Red","Blue","Red","Red","Blue","Blue","Red","Red","Blue","Red","Blue","Red","Blue","Blue","Red"]
submit_button = tk.Button(root, text="Submit", command=add_entry)
submit_button.pack()
#also submit when enter is pressed
root.bind('<Return>', lambda event: add_entry())

#add an entry field, button and listbox for summoner names and team sides
#add multiple choice input for team side
side = tk.StringVar(root)
side.set("Blue")
side_menu = tk.OptionMenu(root, side, "Blue", "Red")
side_label = tk.Label(root, text="Enter summoner name", bg="white", fg="black", font=("Arial", 15))
side_label.pack()
side_menu.pack()

#add summoner entry
summoner_entry = tk.Entry(root, width=50)
summoner_entry.pack()

#add listbox for summoner names
summoner_listbox = tk.Listbox(root, width=50)
summoner_listbox.pack()

#submit summoner name and side to listbox and add to dictionary
summoners = {}
summoner_button = tk.Button(root, text="Submit", command=add_summoner)
summoner_button.pack()







#show the gui
root.mainloop()
