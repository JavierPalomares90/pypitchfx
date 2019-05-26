import feather
from sqlalchemy import create_engine
import psycopg2

BATCH_SIZE = 5000;

INSERT_PLAYERS = """INSERT INTO player(player_id,full_name)
VALUES({player_id},{full_name})
"""

def get_conn():
    conn = psycopg2.connect(user='postgres', password='J5Oou5wrkGgN4I7G',
                        host='localhost', port='5432')
    return conn 

def insert_player(cursor,player):
    player_id = player['id']
    full_name = player['full name']
    sql = INSERT_PLAYERS.format(player_id=player_id,full_name=full_name)
    cursor.execute(sql)

def load_players():
    path = "data/py_players.feather"
    df = feather.read_dataframe(path)
    conn = get_conn()
    cursor = conn.cursor()
    i = 0
    for player in df.rows:
        insert_player(cursor,player)
        if(i % BATCH_SIZE == 0):
            conn.commit()
    cursor.close()
def main():
    load_players()

if __name__=="__main__":
    main()
