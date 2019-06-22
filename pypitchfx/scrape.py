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

def scrape(start,end,game_ids=None,db_connection=None):
    if game_ids is None:
        game_dir = makeUrls(start,end)
    else:
        game_dir = makeUrls(gids=game_ids)
    for url in game_dir:
        print(url)
    innings_all = get_innings_all(game_dir)
    players = get_players(game_dir)
    innings_hit = get_innings_hit(game_dir)
    mini_scoreboard = get_miniscoreboard(game_dir)
    games = parse_innings_all(innings_all)

def main():
    args = get_args()
    start = args.start
    end = args.end
    gids = args.gameId
    scrape(start,end,game_ids=gids)

if __name__=="__main__":
    main()
