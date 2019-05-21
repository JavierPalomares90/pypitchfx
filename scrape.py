#!/usr/bin/env python
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup # required  pip3 install lxml
import gids as gds
import argparse
from datetime import datetime
import requests
from Game import Game
from Inning import Inning
from AtBat import AtBat
from HalfInning import HalfInning

'''
Python tool to scrape pitchf/x data from mlb's website.
Inspired by pitchfx package written in R
Author: Javier Palomares
'''

def gids2urls(gids):
    urls = []
    root = "http://gd2.mlb.com/components/game/mlb"
    for gid in gids:
       elements = gid.split('_') 
       year = elements[1]
       month = elements[2]
       day = elements[3]
       url = "{root}/year_{year}/month_{month}/day_{day}/{id}".format(root=root,year=year,month=month,day=day,id=gid)
       urls.append(url)
    return urls


def makeUrls(start=None,end=None,gids=None):
    if gids is None:
        if start is None or end is None:
            raise Exception("Need to specify start or end")
        gids = gds.get_gids()
        subset_gids = get_subset_gids(gids,start,end)
        return gids2urls(subset_gids)
        
        
def get_subset_gids(gids,first,last):
    list = []
    first_dt = datetime.strptime(first,"%Y-%m-%d")
    last_dt = datetime.strptime(last,"%Y-%m-%d")
    for gid in gids:
        elements = gid.split('_')
        gid_dt = datetime.strptime(elements[1]+"-"+elements[2]+"-"+elements[3],"%Y-%m-%d")
        if(first_dt <= gid_dt and gid_dt <= last_dt):
            list.append(gid)
    return list

def get_innings_all(game_dir):
    innings_all = []
    for game in game_dir:
        innings_all.append(game+"/inning/inning_all.xml")
    return innings_all

def get_players(game_dir):
    players = []
    for game in game_dir:
        players.append(game + "/players.xml")
    return players

def get_innings_hit(game_dir):
    innings_hit = []
    for game in game_dir:
        innings_hit.append(game + "/inning/inning_hit.xml")
    return innings_hit

def get_miniscoreboard(game_dir):
    miniscoreboard = []
    for game in game_dir:
        miniscoreboard.append(game + "/miniscoreboard.xml")
    return miniscoreboard

def parse_game(game_xml):
    game_attrs = dict(game_xml.attrs)
    atBat = game_attrs["atBat"]
    deck = game_attrs["deck"]
    hole = game_attrs["hole"]
    ind = game_attrs["ind"]
    game = Game(atBat,deck,hole,ind)
    return game

def parse_pitch(pitch):
    #TODO Complete impl
    pass

def parse_at_bat(ab):
    ab_attributes = dict(ab.attrs)
    num = ab_attributes['num']
    b = ab_attributes['b']
    s = ab_attributes['s']
    o = ab_attributes['o']
    start_tfs = ab_attributes['start_tfs']
    start_tfs_zulu = ab_attributes['start_tfs_zulu']
    batter = ab_attributes['batter']
    stand = ab_attributes['stand'] # TODO: Convert to binary
    b_height = ab_attributes['b_height']
    pitcher = ab_attributes['pitcher']
    p_throws = ab_attributes['p_throws']
    des = ab_attributes['des']
    event_num = ab_attributes['event_num']
    event = ab_attributes['event']
    home_team_runs = ab_attributes['home_team_runs']
    away_team_runs = ab_attributes['away_team_runs']

    at_bat = AtBat(num,b,s,o,start_tfs,start_tfs_zulu,batter,
        stand,b_height,pitcher,p_throws,des,event_num,event,home_team_runs,away_team_runs)
    # get the pitches
    pitches_xml = list(inning.children)
    pitches = []
    for p in pitches_xml:
        pitch = parse_pitch(p)
        pitches.append(pitch)
    at_bat.pitches = pitches
    return at_bat


def parse_half_inning(half):
    ab_xml = list(half.children)
    at_bats = []
    for ab in ab_xml:
        at_bat = parse_at_bat(ab)
        at_bats.append(at_bat)
    h = HalfInning()
    h.at_bats = at_bats
    return h

def add_half_innings(inning,half_innings):
    top = half_innings[0]
    bottom = half_innings[1]
    top_inning = parse_half_inning(top)
    bottom_inning = parse_half_inning(bottom)
    inning.top = top_inning
    inning.bottom = bottom_inning
    return inning

def parse_inning(inning):
    innings_attr = dict(inning.attrs)
    num = innings_attr["num"]
    away_team = innings_attr["away_team"]
    home_team = innings_attr["home_team"]
    nxt = innings_attr["next"]
    half_innings = list(inning.children)
    i = Inning(num,away_team,home_team,nxt)
    i = add_half_innings(i,half_innings)
    return i


def parse_innnings_all(innings_all):
    for url in innings_all:
        resp = requests.get(url)
        contents = resp.content
        soup = BeautifulSoup(contents,'xml')
        game_xml = soup.find('game')
        game = parse_game(game_xml)
        innings_xml = soup.find_all('inning')
        innings = []
        for inni in innings_xml:
            innings.append(parse_inning(inni))
        x = 0
    pass
        

def scrape(start,end,game_ids=None,suffix="inning/inning_all.xml",db_connection=None):
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
    parse_innnings_all(innings_all)
    
def get_args():
    parser = argparse.ArgumentParser(description='Scrape data')
    parser.add_argument('-s','--start')
    parser.add_argument('-e','--end')
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    start = args.start
    end = args.end
    scrape(start,end)

if __name__=="__main__":
    main()
