import pypitchfx
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
import logging
import time

localtime = time.asctime( time.localtime(time.time()) )

logger = logging.getLogger("pypitchfx")
logger.setLevel(logging.DEBUG)

# create file handler which logs debug messages
fh = logging.FileHandler("scrape_{}.log".format(localtime), 'w', 'utf-8')
fh.setLevel(logging.DEBUG)

# create console handler with an info log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# creating a formatter
formatter = logging.Formatter('- %(name)s - %(levelname)-8s: %(message)s')

# setting handler format
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

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
        else:
            logger.info("Parsing innings all and players starting on {} to {}".format(start,end))
    else:
        logger.info("Parsing innings all and players for game ids " + game_ids)
    game_urls = makeUrls(start,end,game_ids)
    for url in game_urls:
        logger.info(url)
        print(url)
    db_connection = None

    if engine is not None:
        table_names = engine.table_names()
        db_connection = engine.connect()
        create_tables(db_connection,table_names)

    innings_all_urls = get_innings_all_urls(game_urls)
    players_urls = get_players_urls(game_urls)
    num_innings_all_urls = len(innings_all_urls)
    num_player_urls = len(players_urls)
    if num_innings_all_urls != num_player_urls:
        logger.error("There is a mismatch between the number of player and innings_all xml. Bailing out")
        exit(1)
    logger.info("Starting to parse {} innings_all and player xml files from MLB gameday repository in batches of {}.".format(num_innings_all_urls,batch_size))
    # upload the player and game data in batches if the db_connection is not null
    num_to_load = num_innings_all_urls
    index = 0
    games = []
    players = []
    while True:
        start_index = index*batch_size
        end_index = min((index+1)*batch_size,num_to_load)
        logger.info("Loading {} to {} out of {}".format(start_index,end_index,num_to_load))
        if (start_index >= num_to_load):
            break
        index = index + 1
        innings_to_load = innings_all_urls[start_index:end_index]
        players_to_load = players_urls[start_index:end_index]
        games.append(parse_innings_all(innings_to_load,db_connection))
        players.append(parse_players(players_to_load,db_connection))
    if db_connection is not None:
        db_connection.close()

    logger.info("parsed {} game and {} players".format(len(games),len(players)))

    return games,players

def main():
    args = get_args()
    start = args.start
    end = args.end
    gids = args.gameId
    batch_size = args.batchSize
    games,players = scrape_games_players(start,end,batch_size,game_ids=gids)

if __name__=="__main__":
    main()
