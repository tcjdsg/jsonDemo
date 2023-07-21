
# num_activities,
# num_resource_type,
# total_resource,
# activities
"""
初始化，包括加载数据
初始化编码

"""
import copy
import math
import random

import pandas as pd

from Chromo import Chromosome
from FixedMess import FixedMes

from input.read import read
from Station import Station


class MyInit(object):

    def __init__(self,filenameDis,filenameJob):
        self.geneN = 0
        self.activities = {}
        self.filename1 = filenameDis
        self.filename2 = filenameJob

    def readDis(self):

        dis = pd.read_csv(self.filename1, header=None,encoding="utf-8").values
        pdis = dis.tolist()
        for i in range(dis.shape[0]):
            for j in range(dis.shape[1]):
                pdis[i][j] = round(dis[i][j] * 1.0 , 1)#单位是m
                #不考虑设备接口转移速度
        return pdis


    def InitPopulation(self):

        FixedMes.distance = self.readDis()

        self.activities = read(self.filename2)
        self.geneN = len(self.activities)
        FixedMes.Activity_num = self.geneN

        FixedMes.act_info = self.activities
        num = 0
        print("正在生成种群。。。。")
        while num < FixedMes.populationnumber:

            iter = Chromosome()
            codes = self.encoder()

            iter.setcodes(codes)
            stationState = []

            MyInit.fitness(iter, stationState)
            FixedMes.AllFit[num] = copy.deepcopy(iter)
            num+=1

    def encoder(self):
        numbers = len(self.activities)
        cloneA = copy.deepcopy(self.activities)
        chromosome = []

        for a in range(numbers):
            Ei_0 = []  # 紧前任务数为0的任务集编号
            for key, Ei in cloneA.items():
                prece = cloneA[key].predecessor
                if prece is None:
                    continue

                Ei_number = len(prece)
                if Ei_number == 0:
                    Ei_0.append(key)
            random.shuffle(Ei_0)
            random_Ei_0 = Ei_0[0]
            # self.taskid = taskid
            # self.belong_plane_id = jzjId
            chromosome.append([random_Ei_0,cloneA[random_Ei_0].belong_plane_id,cloneA[random_Ei_0].taskid])
            for key, Ei in cloneA.items():
                prece = cloneA[key].predecessor
                if random_Ei_0 in prece:
                    prece.remove(random_Ei_0)
            del cloneA[random_Ei_0]
        return chromosome



    '''
    :param chromosome: 
    :param iter: 
    :param Humans: 
    :param Orders: 
    :return: 
    '''

    @staticmethod
    def fitness(iter,Stations):
        MyInit.initMess(Stations)

        newact = MyInit.serialGenerationScheme(copy.deepcopy(FixedMes.act_info), iter, Stations)
        iter.WorkTime = newact[FixedMes.Activity_num-1].ef
        # finishTimee,t,movetime, = MyInit.decoder(Humans1,newact)
        # iter.movetime = movetime
        # iter.t =t
        iter.setf()
        return Stations,newact


    @staticmethod
    def initMess(Stations):

        number = 0
        for i in range(len(FixedMes.total_station_resource)):
                Stations.append([])
                for j in range(FixedMes.total_station_resource[i]):
                    # ij都是从0开头 ,number也是
                    Stations[i].append(Station([i, j, number]))
                    number += 1

    #
    # @staticmethod
    # def initMessOrder(Orders, activities):
    #     for key , ac in activities.items():
    #         jzjN = ac.belong_plane_id
    #         Orders[jzjN].append(ac)

    '''
    串行调度生成机制，传入所有活动，资源限量，优先序列
    :param allTasks:
    :param resourceAvail:
    :param priority:
    :return:
    '''

    @staticmethod
    def judgeStation(allTasks, Station,  selectTaskID, now_pos, t, dur):
            resourceSumS = 0
            recordS= []
            needType = allTasks[selectTaskID].taskid -2
            for stationNum in allTasks[selectTaskID].avilableR:

                    station = Station[needType][stationNum-1]
                # 舰载机在这个加油站的覆盖范围内：

                    if (len(station.OrderOver) == 0):
                        resourceSumS += 1  # 该类资源可用+1
                        recordS.append(station)

                    if (len(station.OrderOver) == 1):
                        Activity1 = station.OrderOver[0]
                        from_pos = Activity1.belong_plane_id
                        to_pos = Activity1.belong_plane_id
                        movetime1 = 0 if from_pos == 0 else FixedMes.distance[from_pos][
                                                                now_pos] / FixedMes.human_walk_speed
                        movetime2 = 0 if to_pos == 0 else FixedMes.distance[to_pos][
                                                              now_pos] / FixedMes.human_walk_speed
                        if (Activity1.ef + round(movetime1, 0)) <= t \
                                or (t + dur) <= (Activity1.es - round(movetime2, 0)):

                            resourceSumS += 1  # 该类资源可用+1
                            if (Activity1.ef + round(movetime1, 0)) <= t:
                                station.NowJZJ = from_pos
                            else:
                                station.NowJZJ = now_pos
                            recordS.append(station)

                    if (len(station.OrderOver) >= 2):
                        flag = False
                        for taskIndex in range(len(station.OrderOver) - 1):
                            Activity1 = station.OrderOver[taskIndex]
                            Activity2 = station.OrderOver[taskIndex + 1]

                            from_pos = Activity1.belong_plane_id
                            to_pos = Activity2.belong_plane_id
                            movetime1 = 0 if from_pos == 0 else FixedMes.distance[from_pos][
                                                                    now_pos] / FixedMes.human_walk_speed
                            movetime2 = 0 if to_pos == 0 else FixedMes.distance[to_pos][
                                                                  now_pos] / FixedMes.human_walk_speed

                            if (Activity1.ef + round(movetime1, 0)) <= t \
                                    and (t + dur) <= (Activity2.es - round(movetime2, 0)):
                                flag = True
                                resourceSumS += 1  # 该类资源可用+1
                                station.NowJZJ = from_pos
                                recordS.append(station)
                                break

                        if flag == False:
                            Activity1 = station.OrderOver[0]
                            Activity2 = station.OrderOver[-1]
                            from_pos = Activity2.belong_plane_id
                            to_pos = Activity1.belong_plane_id
                            movetime2 = 0 if from_pos == 0 else FixedMes.distance[from_pos][
                                                                    now_pos] / FixedMes.human_walk_speed
                            movetime1 = 0 if to_pos == 0 else FixedMes.distance[to_pos][
                                                                  now_pos] / FixedMes.human_walk_speed

                            if (Activity2.ef + round(movetime2, 0)) <= t \
                                    or (t + dur) <= (Activity1.es - round(movetime1, 0)):
                                resourceSumS += 1  # 该类资源可用+1
                                if (Activity2.ef + round(movetime2, 0)) <= t:
                                    station.NowJZJ = from_pos
                                else:
                                    station.NowJZJ = now_pos
                                recordS.append(station)

            return resourceSumS, recordS

    @staticmethod
    def allocationStation(recordS, stations, allTasks, selectTaskID):
            type = allTasks[selectTaskID].taskid - 2
            now_pos = allTasks[selectTaskID].belong_plane_id
            need = 1
            if need > 0:
                alreadyWorkTime = math.inf
                index = 0
                recordS = sorted(recordS, key=lambda x: (x.alreadyworkTime,
                                                                       FixedMes.distance[x.NowJZJ][now_pos]))

                if len(recordS)!=0:
                    index = recordS[0].zunumber
                    recordS.remove(recordS[0])

                # 更新
                stations[type][index].update(allTasks[selectTaskID])
                allTasks[selectTaskID].SheiBei.append([type, index])
                # allTasks[selectTaskID].SNums.append(stations[type][index].number)
                need -= 1

    @staticmethod
    def serialGenerationScheme(allTasks, iter, stations):

        # 记录资源转移
        priorityToUse = iter.codes.copy()
        resourceAvailS = FixedMes.total_station_resource

        ps = [0]  # 局部调度计划初始化

        allTasks[0].es = 0  # 活动1的最早开始时间设为0
        allTasks[0].ef = allTasks[0].es + allTasks[0].duration

        for stage in range(0, len(priorityToUse)):
            selectTaskID = priorityToUse[stage][0]
            earliestStartTime =0
            # 当前jzj编号
            now_pos = allTasks[selectTaskID].belong_plane_id
            # jzj入场时间
            if now_pos!=0:
                earliestStartTime = FixedMes.jzjStartTime[now_pos-1]

            dur = allTasks[selectTaskID].duration
            for preTaskID in allTasks[selectTaskID].predecessor:
                if allTasks[preTaskID].ef > earliestStartTime:
                    earliestStartTime = allTasks[preTaskID].ef

            startTime = earliestStartTime
            # 检查满足资源限量约束的时间点作为活动最早开始时间，即在这一时刻同时满足活动逻辑约束和资源限量约束
            t = startTime
            recordS = []

            # 计算t时刻正在进行的活动的资源占用总量,当当前时刻大于活动开始时间小于等于活动结束时间时，说明活动在当前时刻占用资源
            while t >= startTime:
                resourceSumS, recordS = MyInit.judgeStation(allTasks, stations, selectTaskID, now_pos, t, dur)
                # 若资源不够，则向后推一个单位时间
                if (resourceSumS < allTasks[selectTaskID].needNums):
                        t = round(t+60, 0)
                else:
                    break
            # 若符合资源限量则将当前活动开始时间安排在这一时刻
            allTasks[selectTaskID].es = round(t, 0)
            allTasks[selectTaskID].ef = round(t + dur, 0)
            MyInit.allocationStation(recordS, stations, allTasks, selectTaskID)
            # 局部调度计划ps
            ps.append(selectTaskID)
        return allTasks

if __name__ == '__main__':
    m = MyInit("C:/Users/29639/Desktop/dis.csv","C:/Users/29639/Desktop/order.txt")
    m.InitPopulation()
    a=[[0,1,2],[[2,3,1]]]
    b=[[1,1,2],[[2,3,1]]]


    print(a==b)












