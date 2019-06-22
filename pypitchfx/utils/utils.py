# Utils class for various helper methods
# Author: Javier Palomares

import argparse
from datetime import datetime,timedelta, date
from bs4 import BeautifulSoup # required  pip3 install lxml
import requests
from parse.parse import parse_scoreboard_xml

_GAMEDAY_ROOT = "http://gd2.mlb.com/components/game/mlb"

def gids2urls(gids):
    urls = []
    root = _GAMEDAY_ROOT
    for gid in gids:
       elements = gid.split('_') 
       year = elements[0]
       month = elements[1]
       day = elements[2]
       url = "{root}/year_{year}/month_{month}/day_{day}/gid_{id}".format(root=root,year=year,month=month,day=day,id=gid)
       urls.append(url)
    return urls


def get_gids_for_day(day_date):
    year = day_date.year
    month = day_date.month
    day = day_date.day
    root = _GAMEDAY_ROOT
    url = "{}/year_{}/month_{:02d}/day_{:02d}/scoreboard.xml".format(root,year,month,day)
    resp = requests.get(url)
    contents = resp.content
    soup = BeautifulSoup(contents,'xml')
    scoreboard_xml = soup.find('scoreboard')
    return parse_scoreboard_xml(scoreboard_xml)

# returns the days between the start and end date, inclusive
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def makeUrls(start=None,end=None,gids=None):
    if gids is None:
        if start is None or end is None:
            raise Exception("Need to specify start or end")
        # Get all the gids by parsing the scoreboard for each day
        start_date = datetime.strptime(start,"%Y-%m-%d")
        end_date = datetime.strptime(end,"%Y-%m-%d")
        gids=[]
        for day in daterange(start_date,end_date):
            gids_day = get_gids_for_day(day)
            gids = gids + gids_day
    return gids2urls(gids)
        
        
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

def get_args():
    parser = argparse.ArgumentParser(description='Scrape data')
    parser.add_argument('-s','--start')
    parser.add_argument('-e','--end')
    parser.add_argument('-g','--gameId',required=False,nargs='+')
    args = parser.parse_args()
    return args

def get_height_from_string(s):
    height = 0
    h = s.split('-')
    feet = int(h[0])
    inches = int(h[1])
    height = 12 * feet + inches
    return height
