# Pypitchfx
Python tool written to parse data from MLB's Gameday and PitchF/X data.
Inspired by pitchfx package written in R.

The tool parses the gameday day xml files into objects to make data interaction simpler

## Getting players and games for a given data range
```
from pypitchfx.scrape import scrape_games_players
games,players=scrape_games_players(start='2013-06-01',end='2013-06-01')
```
## Writing to a database
Pass in a sqlalchemy engine and the script will write to a relational database
For example:
```
from sqlalchemy import create_engine
from pypitchfx.scrape import scrape_games_players

engine = create_engine('postgresql+psycopg2:<user>:<pw>@localhost')
games,players=scrape_games_players(start='2013-06-01',end='2013-06-01',engine=engine)
```
