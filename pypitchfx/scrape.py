from pypitchfx.gameday_model.Action import Action
from pypitchfx.gameday_model.AtBat import AtBat
from pypitchfx.gameday_model.Game import Game 
from pypitchfx.gameday_model.GamePlayer import GamePlayer 
from pypitchfx.gameday_model.HalfInning import HalfInning 
from pypitchfx.gameday_model.Inning import Inning 
from pypitchfx.gameday_model.Pickoff import Pickoff 
from pypitchfx.gameday_model.Pitch import Pitch
from pypitchfx.gameday_model.Runner import Runner 
from pypitchfx.parse.parse import parse_players,parse_innings_all 
from pypitchfx.utils.utils import makeUrls,get_innings_all_urls,get_players_urls,get_args
from pypitchfx.load.create_tables import create_tables

'''
Python tool to scrape pitchf/x data from MLB's Gameday repo
Inspired by pitchfx package written in R
Author: Javier Palomares
'''

# Return the games and players for the given date range or list of ids
# Pass in a SqlAlchemy engine to write the games and players to a relational DB
def scrape_games_players(start=None,end=None,batch_size=20,game_ids=None,engine=None):
    if game_ids is None:
        if start is None or end is None:
            raise Exception('Specify the start and end dates, or give the game ids')
    game_urls = makeUrls(start,end,game_ids)
    for url in game_urls:
        print(url)
    db_connection = None

    if engine is not None:
        table_names = engine.table_names()
        db_connection = engine.connect()
        create_tables(db_connection,table_names)

    innings_all_urls = get_innings_all_urls(game_urls)
    players_urls = get_players_urls(game_urls)
    # upload the player and game data in batches
    num_to_load = len(innings_all_urls)
    index = 0
    games = []
    players = []
    while True:
        start_index = index*batch_size
        end_index = min((index+1)*batch_size,num_to_load)
        if (start_index >= num_to_load):
            break
        index = index + 1
        innings_to_load = innings_all_urls[start_index:end_index]
        players_to_load = players_urls[start_index:end_index]
        games.append(parse_innings_all(innings_to_load,db_connection))
        players.append(parse_players(players_to_load,db_connection))

    if db_connection is not None:
        db_connection.close()

    return games,players

def main():
    args = get_args()
    start = args.start
    end = args.end
    gids = args.gameId
    batch_size = args.batchSize
    games,players = scrape_games_players(start,end,batchSize,game_ids=gids)

if __name__=="__main__":
    main()
