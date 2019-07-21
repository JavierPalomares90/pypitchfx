class GamePlayer:
    # need to add a game_id to this 
    def __init__(self,_id,first,last,num,boxname,
    rl,bats,position,status,team_abbrev,
    team_id,parent_team_abbrev,parent_team_id,avg,
    hr,rbi,current_position,bat_order,
    game_position,wins,losses,era):
        self.id = _id
        self.first=first
        self.last = last
        self.num=num
        self.boxname = boxname
        self.rl = rl
        self.bats = bats
        self.position = position
        self.status = status
        self.team_abbrev = team_abbrev
        self.team_id = team_id
        self.parent_team_abbrev = parent_team_abbrev
        self.parent_team_id = parent_team_id
        self.avg = avg
        self.hr = hr
        self.rbi = rbi
        self.current_position = current_position
        self.bat_order = bat_order
        self.game_position = game_position
        self.wins = wins
        self.losses = losses
        self.era = era
        self.gid = None
        self.url = None


