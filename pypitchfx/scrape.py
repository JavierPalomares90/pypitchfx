import numpy as np
import pandas as pd
from bs4 import BeautifulSoup # required  pip3 install lxml
from datetime import datetime
import requests
from gameday_model.Game import Game
from gameday_model.Action import Action
from gameday_model.AtBat import AtBat
from gameday_model.GamePlayer import GamePlayer
from gameday_model.HalfInning import HalfInning
from gameday_model.Inning import Inning
from gameday_model.Pickoff import Pickoff
from gameday_model.Runner import Runner
from parse.parse import *
from utils.utils import *

'''
Python tool to scrape pitchf/x data from MLB's Gameday repo
Inspired by pitchfx package written in R
Author: Javier Palomares
'''

def add_half_innings(inning,half_innings):
    top = half_innings[0]
    top_inning = parse_half_inning(top)
    inning.top = top_inning
    if(len(half_innings) > 1):
        bottom = half_innings[1]
        bottom_inning = parse_half_inning(bottom)
        inning.bottom = bottom_inning
    return inning

# Return the games and players for the given date range or list of ids
# Pass in a db_connection to write the games and players to a relational DB
def scrape_games_players(start=None,end=None,game_ids=None,db_connection=None):
    if game_ids is None:
        if start is None or end is None:
            raise('Specify the start and end dates, or give the game ids')
    game_urls = makeUrls(start,end,game_ids)
    for url in game_urls:
        print(url)
    innings_all_urls = get_innings_all_urls(game_urls)
    players_urls = get_players_urls(game_urls)
    players = parse_players(players_urls,db_connection)
    games = parse_innings_all(innings_all_urls,db_connection)
    return games,players

def main():
    args = get_args()
    start = args.start
    end = args.end
    gids = args.gameId
    games,players = scrape_games_players(start,end,game_ids=gids)

if __name__=="__main__":
    main()
