import uuid
class Pitch:

    def __init__(self,des,id_,type_,tfs,tfs_zulu,x,y,event_num,sv_id,
    play_guid,start_speed,end_speed,sz_top,sz_bot,pfx_x,pfx_z,
    px,pz,x0,y0,z0,vx0,vy0,vz0,ax,ay,az,break_y,break_angle,break_length,
    pitch_type,type_confidence,zone,nasty,spin_dir,spin_rate,cc,mt):
        self.uuid = uuid.uuid4()
        self.des = des
        self.id = id_
        self.type = type_
        self.tfs = tfs
        self.tfs_zulu = tfs_zulu
        self.x = x
        self.y = y
        self.event_num = event_num
        self.sv_id = sv_id
        self.play_guid = play_guid 
        self.start_speed = start_speed
        self.end_speed = end_speed
        self.sz_top = sz_top
        self.sz_bot = sz_bot
        self.pfx_x = pfx_x
        self.pfx_z = pfx_z
        self.px = px
        self.pz = pz
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.vx0 = vx0
        self.vy0 = vy0
        self.vz0 = vz0
        self.ax = ax
        self.ay = ay
        self.az = az
        self.break_y = break_y
        self.break_angle = break_angle
        self.break_length = break_length
        self.pitch_type = pitch_type
        self.type_confidence = type_confidence
        self.zone = zone
        self.nasty = nasty
        self.spin_dir = spin_dir
        self.spin_rate = spin_rate
        self.cc = cc
        self.mt = mt

        self.at_bat_id = None
        self.half_inning_id = None
        self.inning_id = None
        self.game_id = None


