# Utils class for various helper methods
# Author: Javier Palomares

import argparse
from datetime import datetime,timedelta, date
from bs4 import BeautifulSoup # required  pip3 install lxml
import requests
import re

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
    url = get_scoreboard_url(year,month,day)

    resp = requests.get(url)
    contents = resp.content
    soup = BeautifulSoup(contents,'xml')
    scoreboard_xml = soup.find('scoreboard')
    from pypitchfx.parse.parse import parse_scoreboard_xml
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

def get_innings_all_urls(game_urls):
    innings_all = []
    for game in game_urls:
        innings_all.append(game+"/inning/inning_all.xml")
    return innings_all

def get_players_urls(game_urls):
    players = []
    for game in game_urls:
        players.append(game + "/players.xml")
    return players

def get_innings_hit_urls(game_urls):
    innings_hit = []
    for game in game_urls:
        innings_hit.append(game + "/inning/inning_hit.xml")
    return innings_hit

def get_miniscoreboard_urls(game_urls):
    miniscoreboard = []
    for game in game_urls:
        miniscoreboard.append(game + "/miniscoreboard.xml")
    return miniscoreboard

def get_scoreboard_url(year,month,day):
    root = _GAMEDAY_ROOT
    url = "{}/year_{}/month_{:02d}/day_{:02d}/scoreboard.xml".format(root,year,month,day)
    return url

def get_args():
    parser = argparse.ArgumentParser(description='Scrape data')
    parser.add_argument('-s','--start')
    parser.add_argument('-e','--end')
    parser.add_argument('-g','--gameId',required=False,nargs='+')
    parser.add_argument('-b','--batchSize',required=False,default=20)
    args = parser.parse_args()
    return args

def get_height_from_string(s):
    tokens = re.split('-|\' ',s)
    feet = int(tokens[0])
    inches = int(tokens[1])
    height = 12 * feet + inches
    return height

def  get_gid_from_url(url):
    # find the gid from the url
    x = re.search('gid_[0-9]{4}_[0-9]{2}_[0-9]{2}_.*_[0-9]+\/',url)
    gid = x.group()
    # remove the backslash
    gid = gid.replace('/','')
    return gid

def get_ids(pojos):
    ids = []
    for i in pojos:
        id_ = str(i.uuid)
        ids.append(id_)
    return ids

def get_boolean_from_TF(b):
    if b =='T' or b == 'Y':
        return True
    elif b == 'F' or b =='N':
        return False
    else:
        raise("Invalid boolean " +b )

def get_at_bat_outcome(ab):
    # For now, good event if we get an out
    event = ab.event.lower()
    if 'out' in event:
        return 1.0
    # else, bad outcome
    return 0

def get_pitch_outcome(pitch):
    des = pitch.des.lower()
    # good pitch if we get foul or out or strike
    if 'foul' in des or 'out' in des or 'strike' in des:
        return 1.0
    return 0

def zulu_to_ts(start):
    start = start.replace('T', ' ')
    start = start.replace('Z', '')
    if start == '':
        return None
    return start

def runner_base_to_int(pos):
    if pos == "":
        return 0
    elif pos == '1B':
        return 1
    elif pos == '2B':
        return 2
    elif pos == '3B':
        return 3
    elif pos == 'score':
        return 4
    else:
        raise Exception("Invalid runner base " + pos)


