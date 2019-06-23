import uuid
class Inning:

    def __init__(self, num, away_team, home_team,nxt):
        self.uuid = uuid.uuid4()
        self.num = num
        self.away_team = away_team
        self.home_team = home_team
        self.next = nxt
        # top and bottom half innings
        self.top = None
        self.bottom = None
        self.game_id = None
