import uuid
class Pickoff:

    def __init__(self, des,event_num):
        self.uuid = uuid.uuid4()
        self.des = des
        self.event_num = event_num