import uuid
class HalfInning:
    
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.at_bats_and_actions = None
        self.isTop = None

        self.inning_id = None
        self.game_id = None
        