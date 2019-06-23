import uuid
class Action:

    def __init__(self,b,s,o,des,event,tfs,tfs_zulu,player,pitch,event_num,home_team_runs,away_team_runs):
        self.uuid = uuid.uuid4()
        self.b = b
        self.s = s
        self.o = o
        self.des = des
        self.event = event
        self.tfs = tfs
        self.tfs_zulu = tfs_zulu
        self.player = player
        self.pitch = pitch
        self.event_num = event_num
        self.home_team_runs = home_team_runs
        self.away_team_runs = away_team_runs

        self.half_inning_id = None
        self.inning_id = None
        self.game_id = None
