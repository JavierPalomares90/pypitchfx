import uuid
class Game:

    def __init__(self, atBat, deck, hole,ind):
        self.uuid = uuid.uuid4()
        self.atBat = atBat
        self.deck = deck
        self.hole = hole
        self.ind = ind
        self.innings = None
        self.url = None
        self.gid = None
    
