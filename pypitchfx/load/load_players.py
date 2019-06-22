from pypitchfx.load.Queries import *
from pypitchfx.gameday_model import GamePlayer
from pypitchfx.utils.utils import *

def insert_player(cursor,player):
    player_id = player['id']
    full_name = player['full_name']
    # Escape names with single quote (like O'Connor)
    full_name = full_name.replace("'","''")
    sql = text(INSERT_PLAYERS.format(player_id=player_id,full_name=full_name).replace("'None'",'None').replace('None','NULL'))
    cursor.execute(sql)
