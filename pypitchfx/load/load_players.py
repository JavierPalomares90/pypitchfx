from utils.utils import *
from gameday_model.GamePlayer import GamePlayer
from pypitchfx.load.Queries import *

def insert_player(cursor,player):
    player_id = player['id']
    full_name = player['full_name']
    # Escape names with single quote (like O'Connor)
    full_name = full_name.replace("'","''")
    sql = text(INSERT_PLAYERS.format(player_id=player_id,full_name=full_name).replace("'None'",'None').replace('None','NULL'))
    cursor.execute(sql)
