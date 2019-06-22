from pypitchfx.load.Queries import *
from pypitchfx.gameday_model import GamePlayer
from pypitchfx.utils.utils import *
from sqlalchemy.sql import text

def insert_player(conn,player):
    player_id = player.id
    first = player.first
    last = player.last
    boxname = player.boxname
    num = player.num
    rl = player.rl
    bats = player.bats
    position = player.position
    _status = player.status
    ##TODO: Finish parsing

    

    # Escape names with single quote (like O'Connor)
    first = first.replace("'","''")
    last = last.replace("'","''")
    boxname = boxname.replace("'","''")
    sql = text(INSERT_GAMEPLAYER.format())
    conn.execute(sql)
