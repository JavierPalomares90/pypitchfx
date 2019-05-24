import uuid
class Runner:

    def __init__(self,id,start,end,event,event_num,score='F',rbi='F',earned='F'):
        self.uuid = uuid.uuid4()
        self.id = id
        self.start = start
        self.end = end
        self.event = event
        self.event_num = event_num
        self.score = score
        self.rbi = rbi
        self.earned = earned