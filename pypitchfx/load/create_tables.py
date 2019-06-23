from sqlalchemy.sql import text
from pypitchfx.load.queries import *

# Helper methods to create necessary tables
def create_game_table(conn):
    conn.execute(CREATE_GAME_TABLE)

def  create_inning_table(conn):
    conn.execute(CREATE_INNING_TABLE)

def create_half_inning_table(conn):
    conn.execute(CREATE_HALF_INNING_TABLE)

def create_at_bat_table(conn):
    conn.execute(CREATE_AT_BAT_TABLE)

def create_pitch_table(conn):
    conn.execute(CREATE_PITCH_TABLE)

def create_runner_table(conn):
    conn.execute(CREATE_RUNNER_TABLE)

def create_pickoff_table(conn):
    conn.execute(CREATE_PICKOFF_TABLE)

def create_action_table(conn):
    conn.execute(CREATE_ACTION_TABLE)

def create_game_player_table(conn):
    conn.execute(CREATE_GAME_PLAYER_TABLE)

def create_player_tables(conn):
    create_game_player_table(conn)

def create_game_tables(conn):
    create_game_table(conn)
    create_inning_table(conn)
    create_half_inning_table(conn)
    create_at_bat_table(conn)
    create_pitch_table(conn)
    create_runner_table(conn)
    create_pickoff_table(conn)
    create_action_table(conn)

def create_tables(conn,table_names):
    if 'game' not in table_names:
        create_game_table(conn)
    if 'game_player' not in table_names:
        create_game_player_table(conn)
    if 'inning' not in table_names:
        create_inning_table(conn)
    if 'half_inning' not in table_names:
        create_half_inning_table(conn)
    if 'at_bat' not in table_names:
        create_at_bat_table(conn)
    if 'runner' not in table_names:
        create_runner_table(conn)
    if 'pitch' not in table_names:
        create_pitch_table(conn)
    if 'action' not in table_names:
        create_action_table(conn)
    if 'pickoff' not in table_names:
        create_pickoff_table(conn)
