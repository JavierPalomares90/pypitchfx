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

<atbat num="5" b="2" s="1" o="3" start_tfs="014210" start_tfs_zulu="2013-06-02T01:42:10Z" batter="445988" stand="R" b_height="6-0" pitcher="502188" p_throws="R" des="Martin Prado grounds into a force out, shortstop Starlin Castro to second baseman Darwin Barney. Miguel Montero out at 2nd. " des_es="Martin Prado batea rodado batea para out forzado, campo corto Starlin Castro a segunda base Darwin Barney. Miguel Montero a cabo a 2da. " event_num="37" event="Forceout" event_es="Out Forzado" home_team_runs="0" away_team_runs="1">
<pitch des="Ball" des_es="Bola mala" id="31" type="B" tfs="014215" tfs_zulu="2013-06-02T01:42:15Z" x="78.11" y="178.73" event_num="31" on_1b="471083" sv_id="130601_204253" play_guid="" start_speed="94.1" end_speed="86.6" sz_top="3.24" sz_bot="1.5" pfx_x="-8.37" pfx_z="9.76" px="0.676" pz="1.042" x0="-1.804" y0="50.0" z0="5.678" vx0="9.672" vy0="-137.238" vz0="-10.083" ax="-15.986" ay="30.133" az="-13.461" break_y="23.8" break_angle="41.7" break_length="4.4" pitch_type="FF" type_confidence="2.000" zone="14" nasty="58" spin_dir="220.505" spin_rate="2601.758" cc="" mt=""/>
<pitch des="Foul" des_es="Foul" id="32" type="S" tfs="014237" tfs_zulu="2013-06-02T01:42:37Z" x="103.86" y="143.33" event_num="32" on_1b="471083" sv_id="130601_204315" play_guid="" start_speed="94.4" end_speed="87.2" sz_top="3.13" sz_bot="1.5" pfx_x="-10.59" pfx_z="3.76" px="-0.189" pz="2.347" x0="-1.892" y0="50.0" z0="5.747" vx0="8.406" vy0="-138.123" vz0="-4.736" ax="-20.513" ay="29.922" az="-24.819" break_y="23.8" break_angle="36.0" break_length="6.7" pitch_type="FT" type_confidence="2.000" zone="5" nasty="32" spin_dir="250.274" spin_rate="2288.905" cc="" mt=""/>
<pitch des="Ball" des_es="Bola mala" id="33" type="B" tfs="014301" tfs_zulu="2013-06-02T01:43:01Z" x="156.22" y="105.34" event_num="33" on_1b="471083" sv_id="130601_204340" play_guid="" start_speed="94.8" end_speed="87.6" sz_top="3.21" sz_bot="1.5" pfx_x="-9.61" pfx_z="3.3" px="-1.849" pz="4.41" x0="-1.995" y0="50.0" z0="5.893" vx0="3.835" vy0="-139.06" vz0="0.58" ax="-18.891" ay="30.05" az="-25.618" break_y="23.8" break_angle="35.3" break_length="6.4" pitch_type="FT" type_confidence="2.000" zone="11" nasty="34" spin_dir="250.861" spin_rate="2086.167" cc="" mt=""/>
<pitch des="In play, out(s)" des_es="En juego, out(s)" id="34" type="X" tfs="014329" tfs_zulu="2013-06-02T01:43:29Z" x="112.45" y="153.69" event_num="34" on_1b="471083" sv_id="130601_204407" play_guid="" start_speed="94.4" end_speed="86.9" sz_top="3.13" sz_bot="1.5" pfx_x="-9.26" pfx_z="6.48" px="-0.109" pz="2.11" x0="-1.895" y0="50.0" z0="5.753" vx0="8.142" vy0="-138.107" vz0="-6.333" ax="-17.861" ay="31.06" az="-19.6" break_y="23.8" break_angle="37.5" break_length="5.6" pitch_type="FT" type_confidence="2.000" zone="5" nasty="35" spin_dir="234.854" spin_rate="2294.567" cc="" mt=""/>
<runner id="471083" start="1B" end="" event="Forceout" event_num="37"/>
</atbat>
def parse_at_bat(ab):
    #TODO: Finish impl
    ab_attributes = dict(ab.attrs)
    num = 

def parse_half_inning(half):
    ab_s = list(half.children)
    at_bats = []
    for ab in ab_s:
        at_bat = parse_at_bat(ab)
        at_bats.append(at_bat)
    h = HalfInning()
    h.at_bats = at_bats
    return h

def add_half_innings(inning,half_innings):
    top = half_innings[0]
    bottom = half_innings[1]
    top_inning = parse_half_inning(top)
    bottom_inning = parse_bottom_inning(bottom)

def parse_inning(inning):
    innings_attr = dict(inning.attrs)
    num = innings_attr["num"]
    away_team = innings_attr["away_team"]
    home_team = innings_attr["home_team"]
    nxt = innings_attr["next"]
    half_innings = list(inning.children)
    i = Inning(num,away_team,home_team,nxt)
    add_half_innings(i,half_innings)
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
