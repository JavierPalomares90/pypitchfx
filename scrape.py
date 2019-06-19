import numpy as np
import pandas as pd
from bs4 import BeautifulSoup # required  pip3 install lxml
import gids as gds
import argparse
from datetime import datetime,timedelta,date
import requests
from Game import Game
from Inning import Inning
from AtBat import AtBat
from HalfInning import HalfInning
from Pitch import Pitch
from Runner import Runner
from Action import Action
from Pickoff import Pickoff

'''
Python tool to scrape pitchf/x data from mlb's website.
Inspired by pitchfx package written in R
Author: Javier Palomares
'''
root = "http://gd2.mlb.com/components/game/mlb"

def gids2urls(gids):
    urls = []
    for gid in gids:
       elements = gid.split('_') 
       year = elements[1]
       month = elements[2]
       day = elements[3]
       url = "{root}/year_{year}/month_{month}/day_{day}/{id}".format(root=root,year=year,month=month,day=day,id=gid)
       urls.append(url)
    return urls

def parse_scoreboard_xml(scoreboard_xml):
    game_ids = []
    go_games = scoreboard_xml.find_all('go_game')
    for game in go_games:
        game_xml = game.find_all('game')[0]
        attrs = dict(game_xml.attrs)
        game_id = attrs['id']
        game_ids.append(game_id)
    return game_ids

def get_gids_for_day(day_date):
    year = day_date.year
    month = day_date.month
    day = day_date.day
    url = "{}/year_{}/month_{:02d}/day_{:02d}/scoreboard.xml".format(root,year,month,day)
    resp = requests.get(url)
    contents = resp.content
    soup = BeautifulSoup(contents,'xml')
    scoreboard_xml = soup.find('scoreboard')
    return parse_scoreboard_xml(scoreboard_xml)


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def makeUrls(start=None,end=None,gids=None):
    if gids is None:
        if start is None or end is None:
            raise Exception("Need to specify start or end")
        # Get all the gids by parsing the scoreboard for each day
        start_date = datetime.strptime(start,"%Y-%m-%d")
        end_date = datetime.strptime(end,"%Y-%m-%d")
        subset_gids=[]
        for day in daterange(start_date,end_date):
            gids_day = get_gids_for_day(day)
            subset_gids.append(gids_day)
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

def parse_pitch(pitch_xml):
    pitch_attrs = dict(pitch_xml.attrs)
    des = pitch_attrs.get('des')
    id_var = pitch_attrs.get('id')
    type_var = pitch_attrs.get('type')
    tfs = pitch_attrs.get('tfs')
    tfs_zulu = pitch_attrs.get('tfs_zulu')
    x = pitch_attrs.get('x')
    y = pitch_attrs.get('y')
    event_num = pitch_attrs.get('event_num')
    sv_id = pitch_attrs.get('sv_id')
    play_guid = pitch_attrs.get('play_guid')
    start_speed = pitch_attrs.get('start_speed')
    end_speed = pitch_attrs.get('end_speed')
    sz_top = pitch_attrs.get('sz_top')
    sz_bot = pitch_attrs.get('sz_bot')
    pfx_x = pitch_attrs.get('pfx_x')
    pfx_z = pitch_attrs.get('pfx_z')
    px = pitch_attrs.get('px')
    pz = pitch_attrs.get('pz')
    x0 = pitch_attrs.get('x0')
    y0 = pitch_attrs.get('y0')
    z0 = pitch_attrs.get('z0')
    vx0 = pitch_attrs.get('vx0')
    vy0 = pitch_attrs.get('vy0')
    vz0 = pitch_attrs.get('vz0')
    ax = pitch_attrs.get('ax')
    ay = pitch_attrs.get('ay')
    az = pitch_attrs.get('az')
    break_y = pitch_attrs.get('break_y')
    break_angle = pitch_attrs.get('break_angle')
    break_length = pitch_attrs.get('break_length')
    pitch_type = pitch_attrs.get('pitch_type')
    type_conf = pitch_attrs.get('type_confidence')
    zone = pitch_attrs.get('zone')
    nasty = pitch_attrs.get('nasty')
    spin_dir = pitch_attrs.get('spin_dir')
    spin_rate = pitch_attrs.get('spin_rate')
    cc = pitch_attrs.get('cc')
    mt = pitch_attrs.get('mt')

    pitch = Pitch(des,id_var,type_var,tfs,tfs_zulu,x,y,event_num,sv_id,
    play_guid,start_speed,end_speed,sz_top,sz_bot,pfx_x,pfx_z,
    px,pz,x0,y0,z0,vx0,vy0,vz0,ax,ay,az,break_y,break_angle,break_length,
    pitch_type,type_conf,zone,nasty,spin_dir,spin_rate,cc,mt)
    return pitch

def parse_runner(r):
    runner_attributes = dict(r.attrs)
    id_var = runner_attributes['id']
    start = runner_attributes['start']
    end = runner_attributes['end']
    event = runner_attributes['event']
    event_num = runner_attributes['event_num']
    # score, rbi,earned are optional attributes
    score = runner_attributes.get('score','F')
    rbi = runner_attributes.get('rbi','F')
    earned = runner_attributes.get('earned','F')
    runner = Runner(id_var,start,end,event,event_num,score,rbi,earned)
    return runner

def parse_pickoff(po):
    po_attributes = dict(po.attrs)
    des = po_attributes['des']
    event_num = po_attributes['event_num']
    pickoff = Pickoff(des,event_num)
    return pickoff

def get_height_from_string(s):
    height = 0
    h = s.split('-')
    feet = int(h[0])
    inches = int(h[1])
    height = 12 * feet + inches
    return height

def parse_at_bat(ab):
    ab_attributes = dict(ab.attrs)
    num = ab_attributes['num']
    b = ab_attributes['b']
    s = ab_attributes['s']
    o = ab_attributes['o']
    start_tfs = ab_attributes['start_tfs']
    start_tfs_zulu = ab_attributes['start_tfs_zulu']
    batter = ab_attributes['batter']
    stand = ab_attributes['stand'] 
    # convert stand to binary variable
    if stand == 'L':
        stand = 0
    elif stand == 'R':
        stand = 1
    else:
        raise("Invalid value for stand" + stand)
    b_height = ab_attributes['b_height']
    # convert heigh to numeric
    b_height = get_height_from_string(b_height)
    pitcher = ab_attributes['pitcher']
    p_throws = ab_attributes['p_throws']
    des = ab_attributes['des']

    
    event_num = ab_attributes.get('event_num',-1)
    event = ab_attributes['event']
    home_team_runs = ab_attributes['home_team_runs']
    away_team_runs = ab_attributes['away_team_runs'] # Is this after the atbat?
    score = ab_attributes.get('score','F')

    at_bat = AtBat(num,b,s,o,start_tfs,start_tfs_zulu,batter,
        stand,b_height,pitcher,p_throws,des,event_num,event,home_team_runs,away_team_runs,score)
    # get the pitches and runners during the atbat
    pitches_runners_xml = list(ab.children)
    pitches = []
    runners = []
    for x in pitches_runners_xml:
        if x.name == 'pitch':
            pitch = parse_pitch(x)
            pitches.append(pitch)
        elif x.name == 'runner':
            runner = parse_runner(x)
            runners.append(runner)
        elif x.name == 'po':
            pickoff = parse_pickoff(x)
            # Add the pickoff to the list of pitches
            pitches.append(pickoff)
        else:
            raise('Invalid ab child' + x)
    at_bat.pitches = pitches
    at_bat.runners = runners

    return at_bat

def parse_action(x):
    action_attributes = dict(x.attrs)
    b = action_attributes['b']
    s = action_attributes['s']
    o = action_attributes['o']
    des = action_attributes['des']
    event= action_attributes['event']
    tfs = action_attributes['tfs']
    tfs_zulu = action_attributes['tfs_zulu']
    player = action_attributes['player']
    pitch = action_attributes['pitch']
    event_num = action_attributes['event_num']
    home_team_runs = action_attributes['home_team_runs']
    away_team_runs = action_attributes['away_team_runs']
    action = Action(b,s,o,des,event,tfs,tfs_zulu,player,pitch,event_num,home_team_runs,away_team_runs)
    return action

def parse_half_inning(half):
    abs_and_actions_xml = list(half.children)
    at_bats_and_actions = []
    for x in abs_and_actions_xml:
        if x.name == 'atbat':
            at_bat = parse_at_bat(x)
            at_bats_and_actions.append(at_bat)
        elif x.name =='action':
            action = parse_action(x)
            at_bats_and_actions.append(action)
        else:
            raise('Invalid xml child' + x)
    h = HalfInning()
    h.at_bats_and_actions = at_bats_and_actions
    return h

def add_half_innings(inning,half_innings):
    top = half_innings[0]
    top_inning = parse_half_inning(top)
    inning.top = top_inning
    if(len(half_innings) > 1):
        bottom = half_innings[1]
        bottom_inning = parse_half_inning(bottom)
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
    games = []
    for url in innings_all:
        try:
            resp = requests.get(url)
            contents = resp.content
            soup = BeautifulSoup(contents,'xml')
            game_xml = soup.find('game')
            game = parse_game(game_xml)
            innings_xml = soup.find_all('inning')
            innings = []
            for inni in innings_xml:
                innings.append(parse_inning(inni))
            game.innings = innings
            game.url = url
        except:
            print('unable to load game {}'.format(url))
    return games
        

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
    games = parse_innnings_all(innings_all)
    
def get_args():
    parser = argparse.ArgumentParser(description='Scrape data')
    parser.add_argument('-s','--start')
    parser.add_argument('-e','--end')
    parser.add_argument('-g','--gameId',required=False,type=list)
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    start = args.start
    end = args.end
    gameId = args.gameId
    scrape(start,end,game_ids=gameId)

if __name__=="__main__":
    main()
