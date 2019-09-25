from pypitchfx.load.queries import *
from pypitchfx.gameday_model import GamePlayer
from pypitchfx.utils.utils import *
from sqlalchemy.sql import text

import logging
logger = logging.getLogger("pypitchfx")

def insert_player(conn,player):
    logger.info('Inserting {}\n'.format(player.url))
    player_id = player.id
    first = player.first
    last = player.last
    boxname = player.boxname
    num = player.num
    rl = player.rl
    bats = player.bats
    position = player.position
    _status = player.status
    team_abbrev = player.team_abbrev
    team_id = player.team_id
    parent_team_abbrev = player.parent_team_abbrev
    parent_team_id = player.parent_team_id
    avg = player.avg
    hr = player.hr
    rbi = player.rbi
    current_position = player.current_position
    bat_order = player.bat_order
    game_position = player.game_position
    wins = player.wins
    losses = player.losses
    era = player.era
    gid = player.gid
    bat_order = player.bat_order
    game_position = player.game_position

    # Escape names with single quote (like O'Connor)
    first = first.replace("'","''")
    last = last.replace("'","''")
    boxname = boxname.replace("'","''")
    if not num:
        num = 0
    # some players have '-' to indicate NULL era
    if era is not None and '-' in era:
        era = None
        
    sql = text(INSERT_GAMEPLAYER.format(
        id=player_id,
        first=first,
        last=last,
        num=num,
        boxname=boxname,
        rl=rl,
        bats=bats,
        position=position,
        status=_status,
        team_abbrev=team_abbrev,
        team_id=team_id,
        parent_team_abbrev=parent_team_abbrev,
        parent_team_id=parent_team_id,
        avg=avg,
        hr = hr,
        rbi=rbi,
        current_position=current_position,
        bat_order=bat_order,
        wins=wins,
        losses=losses,
        era=era,
        game_position=game_position,
        gid=gid)
        .replace("'None'",'None').replace('None','NULL'))
    conn.execute(sql)

def load_player(player,conn):
    insert_player(conn,player)
