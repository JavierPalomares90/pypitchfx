import uuid
class AtBat:

    def __init__(self, num, b, s,o, start_tfs, 
        start_tfs_zulu, batter,stand,b_height,pitcher,
        p_throws,des,event_num,event,home_team_runs,away_team_runs,score='F'):
        self.uuid = uuid.uuid4()
        self.num = num
        self.balls = b
        self.strikes = s
        self.outs = o
        self.start_tfs = start_tfs
        self.start_tfs_zulu = start_tfs_zulu
        self.batter = batter
        self.stand = stand
        self.b_height = b_height 
        self.pitcher = pitcher
        self.p_throws = p_throws
        self.des = des
        self.event_num = event_num
        self.event = event
        self.home_team_runs = home_team_runs
        self.score=score
        self.away_team_runs = away_team_runs
        self.pitches = None
        self.runners = None

        self.half_inning_id = None
        self.inning_id = None
        self.game_id = None