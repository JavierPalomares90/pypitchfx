# Pypitchfx
### Javier Palomares

During one of my grad school projects, I decided to train some AI/ML models related to baseball. In order to do this, I would need to collect any data that MLB makes available about the game scores, players, pitch by pitch results, and pitch data.
While researching this, I found that since 2007, MLB has tracked every pitch thrown in games using high speed cameras and MLB makes this data available through its Gameday website as xml files available at http://gd2.mlb.com/components/game/mlb/ (Update: this portal will soon be depracated and replaced with an API. I am an updating this tool to use that API instead of the xml feed).
I searched for a few tools to get the data, and by far the best tool I found available was this [pitchf/x package.](https://pitchrx.cpsievert.me/)
Unfortunately, it's written for R, and hasn't been updated in a few years.

With that in mind, I decided to build my own python package available here.
This packages parses the  xml files into objects to simplify data interaction.


## Installing the package
The package is now uploaded on pypi. Install it using pip

```pip install pypitchfx```

## Parsing Data into Objects
The  data  available  at  MLB’s  Gameday  portal  is  formatted  into  xml  files. There is 1 xml file per game `innings_all.xml`,  containing all of the innings,  half innings, at bats, and pitches occurring during the game formatted as xml elements in sequential order.  Within this file there is a `game` element composed of 9 `inning` child elements (or more if extra innings are needed to break a tie).  Each `inning` element has a `top` and `bottom` child element for each half inning when teams swap batting and fielding.  The`top` and `bottom` elements have `atbat` child elements for each batter appearance in the half inning. The child elements of the `atbat` element is the sequence of pitches in the at bat. Additionally, there is a `players.xml` file pergame containing the data for the players in the game.

The tool parses each of the xml elements into python objects for easier data manipulation.

![Element Hiearchy](https://github.com/JavierPalomares90/pypitchfx/blob/master/images/Element_Hierarchy.png "Hierarchy of Elements")


Additionally, the tool generates unique identifiers at parse time to guarantee uniqueness and to relate parent and child elements.

![E-R Diagram](https://github.com/JavierPalomares90/pypitchfx/blob/master/images/gameday_er_diagram.png "E-R Diagram")

 Entity-Relationship diagram of the database model the `pypitchfx` tool writesthe  Gameday  data  to.   All  of  the  data  fields  available  in  the  xml  fields  are  mapped  tocolumns of the same name.  Generated UUIDs are the tables’ primary keys.  Foreign keyconstraints enforce parent child relationships.  Entities maintain list of the parent to allow for fast lookups of the parent entity.  The DDL statements used to insert and create thetables are available in the pypitch repository in `Queries.py`. Batter and Pitcher are materi-alized views to used to distinguish pitchers and batters in the `Game_Player` table.


## Getting data objects for a given data range
Pass in a range of date (start and end inclusive) for the games you're looking for. The tool will automatically look for all games played in the given range.

```
from pypitchfx.scrape import scrape_games_players
games,players=scrape_games_players(start='2013-06-01',end='2013-06-01')
```
## Writing to a database
Pass in a sqlalchemy engine and the script will write to a relational database following the ER diagram shown above.

For example:
```
from sqlalchemy import create_engine
from pypitchfx.scrape import scrape_games_players

engine = create_engine('postgresql+psycopg2:<user>:<pw>@localhost')
games,players=scrape_games_players(start='2013-06-01',end='2013-06-01',engine=engine)
```
