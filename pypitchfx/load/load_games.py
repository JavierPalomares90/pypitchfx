from pypitchfx.load.queries import *
from pypitchfx.gameday_model.Action import Action
from pypitchfx.gameday_model.AtBat import AtBat
from pypitchfx.gameday_model.Game import Game 
from pypitchfx.gameday_model.GamePlayer import GamePlayer 
from pypitchfx.gameday_model.Inning import Inning 
from pypitchfx.gameday_model.HalfInning import HalfInning 
from pypitchfx.gameday_model.Pickoff import Pickoff 
from pypitchfx.gameday_model.Pitch import Pitch
from pypitchfx.gameday_model.Runner import Runner 
from pypitchfx.utils.utils import *
from sqlalchemy.sql import text
import logging
logger = logging.getLogger("pypitchfx")


def insert_game(conn,game):
    logger.info('Inserting {}\n'.format(game.url))
    game_id = game.uuid
    at_bat = game.atBat
    deck = game.deck
    hole = game.hole
    ind = game.ind 
    innings = game.innings
    innings_ids = get_ids(innings)
    sql = text(INSERT_GAME.format(
        game_id=game_id,
        at_bat = at_bat,
        deck =deck,
        hole=hole,
        ind=ind,
        innings_id=innings_ids,
        url=game.url,
        gid=game.gid)
        .replace("'None'",'None').replace('None','NULL'))
    conn.execute(sql)


def insert_inning(conn,inning):
    inning_id = str(inning.uuid)
    game_id = inning.game_id
    num = int(inning.num)
    away_team = inning.away_team
    home_team = inning.home_team
    nxt = get_boolean_from_TF(inning.next)
    top_id = str(inning.top.uuid)
    bot_id = None
    if inning.bottom is not None:
        bot_id = str(inning.bottom.uuid)
    sql = text(INSERT_INNING.format(
        inning_id=inning_id,
        num=num,
        away_team=away_team,
        home_team=home_team,
        top_inning_id = top_id,
        bottom_inning_id = bot_id,
        game_id=game_id,
        next=nxt)
        .replace("'None'",'None').replace('None','NULL'))
    conn.execute(sql)

def insert_half_inning_helper(conn,hf):
    game_id = hf.game_id
    inning_id = hf.inning_id
    hf_id = str(hf.uuid)
    isTop = hf.isTop
    at_bats_and_actions_ids = get_ids(hf.at_bats_and_actions)
    sql = text(INSERT_HALF_INNING.format(
        half_inning_id=hf_id,
        inning_id=inning_id,
        game_id = game_id,
        isTop = isTop,
        at_bats_actions_id=at_bats_and_actions_ids)
        .replace("'None'",'None').replace('None','NULL'))
    conn.execute(sql)

def insert_pitch(conn,pitch):
    pitch_id = str(pitch.uuid)
    game_id = pitch.game_id
    inning_id = pitch.inning_id
    hf_id = pitch.half_inning_id
    ab_id = pitch.at_bat_id

    des = pitch.des
    des = des.replace("'","''")
    id_ = pitch.id
    type_ = pitch.type
    tfs_zulu = zulu_to_ts(pitch.tfs_zulu)
    x = pitch.x
    y = pitch.y
    event_num = pitch.event_num
    sv_id = pitch.sv_id
    play_guid = pitch.play_guid
    start_speed = pitch.start_speed
    end_speed = pitch.end_speed
    sz_top = pitch.sz_top
    sz_bot = pitch.sz_bot
    pfx_x = pitch.pfx_x
    pfx_z = pitch.pfx_z
    px = pitch.px
    pz = pitch.pz
    x0 = pitch.x0
    y0 = pitch.y0
    z0 = pitch.z0
    vx0 = pitch.vx0
    vy0 = pitch.vy0
    vz0 = pitch.vz0
    ax = pitch.ax
    ay = pitch.ay
    az = pitch.az
    break_y = pitch.break_y
    break_angle = pitch.break_angle
    break_length = pitch.break_length
    pitch_type = pitch.pitch_type
    type_confidence = pitch.type_confidence
    zone = pitch.zone
    nasty = pitch.nasty
    spin_dir = pitch.spin_dir
    spin_rate = pitch.spin_rate
    cc = ''
    mt = ''
    outcome = get_pitch_outcome(pitch)
    sql = text(INSERT_PITCH.format(
        pitch_id = pitch_id,
        des = des,
        id = id_,
        type = type_,
        tfs_zulu = tfs_zulu,
        x = x,
        y = y,
        event_num = event_num,
        sv_id = sv_id,
        play_guid = play_guid,
        start_speed = start_speed,
        end_speed = end_speed,
        sz_top = sz_top,
        sz_bot = sz_bot,
        pfx_x = pfx_x,
        pfx_z = pfx_z,
        px = px,
        pz = pz,
        x0 = x0,
        y0 = y0,
        z0 = z0,
        vx0 = vx0,
        vy0 = vy0,
        vz0 = vz0,
        ax = ax,
        ay = ay,
        az = az,
        break_y = break_y,
        break_angle = break_angle,
        pitch_type=pitch_type,
        break_length = break_length,
        type_confidence = type_confidence,
        zone = zone,
        nasty = nasty,
        spin_dir = spin_dir,
        spin_rate = spin_rate,
        cc = cc,
        mt = mt,
        game_id = game_id,
        inning_id = inning_id,
        half_inning_id = hf_id,
        at_bat_id = ab_id,
        outcome = outcome
    ).replace("'None'",'None').replace('None','NULL'))
    conn.execute(sql)


def insert_runner(conn,runner):
    runner_id = str(runner.uuid)
    game_id = runner.game_id
    inning_id = runner.inning_id
    hf_id = runner.half_inning_id
    ab_id = runner.at_bat_id
    id_ = runner.id
    score = get_boolean_from_TF(runner.score)
    start = runner_base_to_int(runner.start)
    end = runner_base_to_int(runner.end)
    event = runner.event
    if score:
        end = 4
    rbi = get_boolean_from_TF(runner.rbi)
    earned = get_boolean_from_TF(runner.earned)
    sql = text(INSERT_RUNNER.format(
        runner_id=runner_id,
        id=id_,
        start=start,
        end=end,
        event=event,
        score=score,
        rbi=rbi,
        earned=earned,
        game_id = game_id,
        inning_id = inning_id,
        half_inning_id = hf_id,
        at_bat_id = ab_id)
        .replace("'None'",'None').replace('None','NULL'))
    conn.execute(sql)

def insert_pickoff(conn,pickoff):
    po_id =  str(pickoff.uuid)
    ab_id = pickoff.at_bat_id
    hf_id = pickoff.half_inning_id
    inning_id = pickoff.inning_id
    game_id = pickoff.game_id
    des = pickoff.des
    des = des.replace("'","''")
    event_num = pickoff.event_num
    sql = text(INSERT_PICKOFF.format(
        po_id=po_id,
        des=des,
        event_num=event_num,
        game_id = game_id,
        inning_id = inning_id,
        half_inning_id=hf_id,
        at_bat_id = ab_id)
        .replace("'None'",'None').replace('None','NULL'))
    conn.execute(sql)

def insert_at_bat(conn,ab):
    ab_id = str(ab.uuid)
    game_id = ab.game_id
    inning_id = ab.inning_id
    hf_id = ab.half_inning_id

    num = int(ab.num)
    b = int(ab.balls)
    s = int(ab.strikes)
    o = int(ab.outs)
    start = zulu_to_ts(ab.start_tfs_zulu)
    batter = ab.batter
    stands = ab.stand
    b_height = int(ab.b_height)
    pitcher = ab.pitcher
    p_throws = ab.p_throws
    des = ab.des
    des = des.replace("'","''")

    event_num = int(ab.event_num)
    event = ab.event
    home_team_runs = int(ab.home_team_runs)
    away_team_runs = int(ab.away_team_runs)
    pitch_ids = get_ids(ab.pitches)
    runner_ids = get_ids(ab.runners)
    score = get_boolean_from_TF(ab.score)
    outcome = get_at_bat_outcome(ab)
    sql = text(INSERT_AT_BAT.format(
        at_bat_id=ab_id,
        num=num,b=b,
        s=s,
        o=0,
        start_tfs_zulu=start,
        batter=batter,
        b_height=b_height,
        pitcher=pitcher,
        p_throws=p_throws,
        des=des,
        event_num=event_num,
        event=event,
        home_team_runs=home_team_runs,
        away_team_runs=away_team_runs,
        score=score,
        pitch_ids=pitch_ids,
        runner_ids=runner_ids,
        half_inning_id=hf_id,
        game_id = game_id,
        inning_id = inning_id,
        outcome=outcome,
        stands=stands)
        .replace("'None'",'None').replace('None','NULL'))
    conn.execute(sql)
    for pitch in ab.pitches:
        if isinstance(pitch,Pitch):
            insert_pitch(conn,pitch)
        elif isinstance(pitch,Pickoff):
            insert_pickoff(conn,pitch)
        else:
            raise("Invalid pitch "+ pitch)
    for runner in ab.runners:
        insert_runner(conn,runner)

def insert_action(conn,action):
    game_id = action.game_id
    inning_id = action.inning_id
    hf_id = action.half_inning_id

    a_id = str(action.uuid)
    b = action.b
    s = action.s
    o = action.o
    des = action.des
    des = des.replace("'","''")
    event = action.event
    tfs_zulu= zulu_to_ts(action.tfs_zulu)
    player = action.player
    pitch = action.pitch
    event_num = action.event_num
    home_team_runs = action.home_team_runs
    away_team_runs = action.away_team_runs
    sql = text(INSERT_ACTION.format(
        action_id=a_id,
        b=b,
        s=s,
        o=o,
        des=des,
        event=event,
        tfs_zulu=tfs_zulu,
        player=player,
        pitch=pitch,
        event_num=event_num,
        home_team_runs=home_team_runs,
        away_team_runs=away_team_runs,
        half_inning_id=hf_id,
        game_id = game_id,
        inning_id = inning_id)
        .replace("'None'",'None').replace('None','NULL'))
    conn.execute(sql)

def insert_half_inning(conn,hf,i):
    insert_half_inning_helper(conn,hf)
    game_id = hf.game_id
    inning_id = hf.inning_id
    hf_id = str(hf.uuid)
    for a in hf.at_bats_and_actions:
        if isinstance(a,AtBat):
            insert_at_bat(conn,a)
        elif isinstance(a,Action):
            insert_action(conn,a)

def insert_innings(conn,game):
    innings = game.innings
    for i in innings:
        insert_inning(conn,i)
        insert_half_inning(conn,i.top,i)
        if(i.bottom is not None):
            insert_half_inning(conn,i.bottom,i)

# Load the Game object into a sql DB
def load_game(game,conn):
    insert_game(conn,game)
    insert_innings(conn,game)