import feather
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from AtBat import AtBat
from Action import Action
from Pitch import Pitch
from Pickoff import Pickoff
from Queries import *



def get_engine():
    engine = create_engine('postgresql+psycopg2://postgres:J5Oou5wrkGgN4I7G@localhost:5532/')
    return engine

def insert_player(cursor,player):
    player_id = player['id']
    full_name = player['full_name']
    # Escape names with single quote (like O'Connor)
    full_name = full_name.replace("'","''")
    sql = text(INSERT_PLAYERS.format(player_id=player_id,full_name=full_name).replace("'None'",'None').replace('None','NULL'))
    cursor.execute(sql)

def get_ids(innings):
    ids = []
    for i in innings:
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

def insert_game(conn,game):
    print('Inserting {}\n'.format(game.url))
    game_id = game.uuid
    at_bat = game.atBat
    deck = game.deck
    hole = game.hole
    ind = game.ind 
    innings = game.innings
    innings_ids = get_ids(innings)
    sql = text(INSERT_GAME.format(game_id=game_id,at_bat = at_bat,deck =deck,hole=hole,ind=ind,innings_id=innings_ids,url=game.url).replace("'None'",'None').replace('None','NULL'))
    conn.execute(sql)


def load_players():
    path = "data/py_players.feather"
    df = feather.read_dataframe(path)
    engine = get_engine()
    conn = engine.connect()
    for index,player in df.iterrows():
        insert_player(conn,player)
    conn.close()

def insert_inning(conn,game_id,inning):
    inning_id = str(inning.uuid)
    num = int(inning.num)
    away_team = inning.away_team
    home_team = inning.home_team
    nxt = get_boolean_from_TF(inning.next)
    top_id = str(inning.top.uuid)
    bot_id = None
    if inning.bottom is not None:
        bot_id = str(inning.bottom.uuid)
    sql = text(INSERT_INNING.format(inning_id=inning_id,num=num,away_team=away_team,home_team=home_team,top_inning_id = top_id, bottom_inning_id = bot_id,game_id=game_id,next=nxt).replace("'None'",'None').replace('None','NULL'))
    conn.execute(sql)

def insert_half_inning_helper(conn,hf,i,at_bats_and_actions_ids):
    inning_id = str(i.uuid)
    hf_id = str(hf.uuid)
    at_bats_and_actions_ids = get_ids(hf.at_bats_and_actions)
    sql = text(INSERT_HALF_INNING.format(half_inning_id=hf_id,inning_id=inning_id,at_bats_actions_id=at_bats_and_actions_ids).replace("'None'",'None').replace('None','NULL'))
    conn.execute(sql)

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
    

def insert_pitch(conn,ab_id,pitch):
    pitch_id = str(pitch.uuid)
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
        at_bat_id = ab_id,
        outcome = outcome
    ).replace("'None'",'None').replace('None','NULL'))
    conn.execute(sql)

def zulu_to_ts(start):
    start = start.replace('T', ' ')
    start = start.replace('Z', '')
    if start == '':
        return None
    return start

def runner_base_to_int(pos):
    #TODO: Test
    if pos == "":
        return 0
    elif pos == '1B':
        return 1
    elif pos == '2B':
        return 2
    elif pos == '3B':
        return 3
    else:
        raise("invalid runner base" + pos)

def insert_runner(conn,ab_id,runner):
    runner_id = str(runner.uuid)
    id_ = runner.id
    score = get_boolean_from_TF(runner.score)
    start = runner_base_to_int(runner.start)
    end = runner_base_to_int(runner.end)
    event = runner.event
    if score:
        end = 4
    rbi = get_boolean_from_TF(runner.rbi)
    earned = get_boolean_from_TF(runner.earned)
    sql = text(INSERT_RUNNER.format(runner_id=runner_id,id=id_,start=start,end=end,event=event,score=score,rbi=rbi,earned=earned,at_bat_id=ab_id).replace("'None'",'None').replace('None','NULL'))
    conn.execute(sql)

def insert_pickoff(conn,ab_id,pickoff):
    po_id =  str(pickoff.uuid)
    des = pickoff.des
    des = des.replace("'","''")
    event_num = pickoff.event_num
    sql = text(INSERT_PICKOFF.format(po_id=po_id,des=des,event_num=event_num,at_bat_id=ab_id).replace("'None'",'None').replace('None','NULL'))
    conn.execute(sql)

def insert_at_bat(conn,hf_id,ab):
    ab_id = str(ab.uuid)
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
    sql = text(INSERT_AT_BAT.format(at_bat_id=ab_id,num=num,b=b,s=s,o=0,start_tfs_zulu=start,batter=batter,b_height=b_height,pitcher=pitcher,p_throws=p_throws,des=des,event_num=event_num,event=event,home_team_runs=home_team_runs,away_team_runs=away_team_runs,score=score,pitch_ids=pitch_ids,runner_ids=runner_ids,half_inning_id=hf_id,outcome=outcome,stands=stands).replace("'None'",'None').replace('None','NULL'))
    conn.execute(sql)
    for pitch in ab.pitches:
        if isinstance(pitch,Pitch):
            insert_pitch(conn,ab_id,pitch)
        elif isinstance(pitch,Pickoff):
            insert_pickoff(conn,ab_id,pitch)
        else:
            raise("Invalid pitch "+ pitch)
    for runner in ab.runners:
        insert_runner(conn,ab_id,runner)

def insert_action(conn,hf_id,action):
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
    sql = text(INSERT_ACTION.format(action_id=a_id,b=b,s=s,o=o,des=des,event=event,tfs_zulu=tfs_zulu,player=player,pitch=pitch,event_num=event_num,home_team_runs=home_team_runs,away_team_runs=away_team_runs,half_inning_id=hf_id).replace("'None'",'None').replace('None','NULL'))
    conn.execute(sql)

def insert_half_inning(conn,hf,i):
    at_bats_and_actions_ids = get_ids(hf.at_bats_and_actions)
    insert_half_inning_helper(conn,hf,i,at_bats_and_actions_ids)
    hf_id = str(hf.uuid)
    for a in hf.at_bats_and_actions:
        if isinstance(a,AtBat):
            insert_at_bat(conn,hf_id,a)
        elif isinstance(a,Action):
            insert_action(conn,hf_id,a)

def insert_innings(conn,game):
    game_id = str(game.uuid)
    innings = game.innings
    for i in innings:
        insert_inning(conn,game_id,i)
        insert_half_inning(conn,i.top,i)
        if(i.bottom is not None):
            insert_half_inning(conn,i.bottom,i)

def load_game(game):
    engine = get_engine()
    conn = engine.connect()
    insert_game(conn,game)
    insert_innings(conn,game)
    conn.close()


def main():
    load_players()

if __name__=="__main__":
    main()
