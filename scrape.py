#!/usr/bin/env python
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
'''
Python tool to scrape pitchf/x data from mlb's website.
Inspired by pitchfx package written in R
Author: Javier Palomares
'''

def makeUrls(start,end,gids=None):
    root = "http://gd2.mlb.com/components/game/mlb/"
    if gids is None:
        if start is None or end is None:
            raise Exception("Need to specify start or end")
    start = 


def scrape(start,end,game_ids,suffix="inning/inning_all.xml",db_connection):
    if game_ids is None:
        game_dir = makeUrls(start,end)
    else:
        game_dir = makeUrls(gids=game_ids)
    
