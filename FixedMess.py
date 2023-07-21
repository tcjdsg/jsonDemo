from collections import defaultdict
from Chromo import Chromosome

class FixedMes(object):
    """
    distance:
    orderInputMes:

    """
    distance = [[]]
    numJzjPos = 18
    planeOrderNum = 10
    planeNum = 12
    jzjNumbers=[1,2,3,4,5,6,7,8,9,10,11,12]  #舰载机编号
    #停机时间设置
    jzjStartTime = [0 for _ in range(12)]
    #每架舰载机的工序数量
    jzjOrdersNum = {}

    station_resource_type = 5
    total_station_resource = [6, 8, 7, 5, 6]

    Activity_num  = (planeOrderNum)*planeNum+2 #活动数量

    #工序顺序
    #1充电
    #2氧气
    #3氮气
    #4液压
    #5空调通风
    #6加油
    #7挂弹
    #8惯导
    #9结束
    SUCOrder = defaultdict(lambda: [])
    SUCOrder[1] = [2, 3, 4, 5, 6, 7, 8, 9]
    SUCOrder[2] = [3, 4, 5, 6, 7, 8, 9]
    SUCOrder[3] = [7, 8, 9]
    SUCOrder[4] = [9]
    SUCOrder[5] = [9]
    SUCOrder[6] = [9]
    SUCOrder[7] = [9]
    SUCOrder[8] = [9]
    SUCOrder[9] = [10]
    SUCOrder[10] = []

    act_info={}

    cross = 0.5
    cross1 = 2.5
    MutationRate = 0.25
    MutationRatePmo = 0.05
    human_walk_speed = 1 #人员行走速度60 m/(s)
    populationnumber = 30
    ge = 50
    populationnumberson = populationnumber
    AgenarationIten = ge / 3
    GenarationIten = 0

    #保存每代染色体信息 父代
    AllFit = []
    AllFitSon = []
    AllFitFamily = []
    #vnsIter = -1

    Paternal = [[0,0] for _ in range(int(populationnumber/2))]
    #每一代的平均值
    Avufit = {}
    Bestfit={}
    AverPopmove = 0
    AverPopTime = 0
    AverPopVar = 0
    Diversity = 0.0
    bestHumanNumberTarget=[]
    Allactivity = []
    constraintHuman =[]
    constraintStation=[]

    @classmethod
    def my(cls):
        for i in range(cls.populationnumber):
            cls.AllFit.append(Chromosome())
            cls.AllFitSon.append(Chromosome())
            cls.AllFitFamily.append(Chromosome())
            cls.AllFitFamily.append(Chromosome())

















