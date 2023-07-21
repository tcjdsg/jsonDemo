import numpy as np

#Order(i + 1, duration, resource, pre)
class Order(object):

    def __init__(self, id, taskid , jzjId, type,duration, resourceRequestS, es,lf):
        self.id = id
        self.taskid = taskid
        self.belong_plane_id = jzjId
        self.jzjType = type
        self.duration = duration
        self.avilableR = resourceRequestS
        self.predecessor = None
        self.successor = None
        self.es = es
        self.ef = es + duration
        self.needNums = 0
        self.SheiBei=[]

        self.lf = lf
        self.ls = lf - duration

class jsonOrder():
    def __init__(self):
        self.no = None
        self.type = None
        self.action = []

class genjsonOrder():
    def __init__(self):
        self.no = None
        self.type = None
        self.action = []
        self.start_time = None
        self.launch_time = None



