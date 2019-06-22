# Helper class to parse xml from Gameday xml into objects
# Author: Javier Palomares

from gameday_model.Game import Game
from gameday_model.Action import Action
from gameday_model.AtBat import AtBat
from gameday_model.GamePlayer import GamePlayer
from gameday_model.HalfInning import HalfInning
from gameday_model.Inning import Inning
from gameday_model.Pickoff import Pickoff
from gameday_model.Runner import Runner
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup # required  pip3 install lxml
import requests

def parse_game(game_xml):
    game_attrs = dict(game_xml.attrs)
    atBat = game_attrs["atBat"]
    deck = game_attrs["deck"]
    hole = game_attrs["hole"]
    ind = game_attrs["ind"]
    game = Game(atBat,deck,hole,ind)
    return game

def parse_scoreboard_xml(scoreboard_xml):
    game_ids = []
    go_games = scoreboard_xml.find_all('go_game')
    for game in go_games:
        game_xml = game.find_all('game')[0]
        attrs = dict(game_xml.attrs)
        game_id = attrs['id']
        game_ids.append(game_id)
    return game_ids

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


# Parse the url to the /inning/inning_all.xml url
# Load the games using the  db_connection if passed in
def parse_innings_all(innings_all,db_connection=None):
    games = []
    for url in innings_all:
        gid = get_gid_from_url(url)
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
            game.gid = gid
        except Exception as e:
            print('unable to load game {}'.format(url))
            print(e)
    return games

def parse_player(player,gid):
    player_attrs = dict(player.attrs)
    _id = player_attrs.get('id')
    first = player_attrs.get('first')
    last = player_attrs.get('last')
    num = player_attrs.get('num')
    boxname = player_attrs.get('boxname')
    rl = player_attrs.get('rl')
    bats = player_attrs.get('bats')
    position = player_attrs.get('position')
    _status = player_attrs.get('status')
    team_abbrev = player_attrs.get('team_abbrev')
    team_id = player_attrs.get('team_id')
    parent_team_abbrev = player_attrs.get('parent_team_abbrev')
    parent_team_id = player_attrs.get('parent_team_id')
    avg = player_attrs.get('avg')
    hr = player_attrs.get('hr')
    rbi = player_attrs.get('rbi')
    current_position = player_attrs.get('current_position')
    bat_order = player_attrs.get('bat_order')
    game_position = player_attrs.get('game_position')
    wins = player_attrs.get('wins')
    losses = player_attrs.get('losses')
    era = player_attrs.get('era')
    
    p = gameday_model.GamePlayer()
    p.gid = gid
    p.id = _id
    p.first = first
    p.last = last
    p.num = num
    p.boxname = boxname
    p.rl = rl
    p.bats = bats
    p.position = position
    p.status = _status
    p.team_abbrev = team_abbrev
    p.team_id = team_id
    p.parent_team_abbrev = parent_team_abbrev
    p.parent_team_id = parent_team_id
    p.avg = avg
    p.hr = hr
    p.rbi = rbi
    p.current_position = current_position
    p.bat_order = bat_order
    p.game_position = game_position
    p.wins = wins
    p.losses = losses
    p.era = era
    
    return p



# Parse the url to the /players.xml url
# Load the player using the db_connection if passed in
def parse_players(players_urls,db_connection=None):
    players = []
    for url in players_urls:
        try:
            gid = get_gid_from_url(url)
            resp = requests.get(url)
            contents = resp.content
            soup = BeautifulSoup(contents,'xml')
            players_xml = soup.find_all('player')
            players = []
            for player_xml in players_xml:
                players.append(parse_player(player_xml,gid))
        except Exception as e:
            print('unable to load player {}'.format(url))
            print(e)
    return players 