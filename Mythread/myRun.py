import copy
import math

import numpy as np

from Mythread.myInit import MyInit

from util import *
from FixedMess import *
from util import utils
from util.utils import *

class MyRun(object):
    def __init__(self):

        self.cur=0
        self.jzjs = FixedMes.jzjNumbers


    def RUN(self,i):

        self.cur=i
        self.Pop = FixedMes.AllFit
        self.select()
        # print("----------- select ----------")
        self.Crossover()
        # print("----------- Crossover ----------")
        self.Variation()
        # print("----------- Variation ----------")
        self.updata()
        # print("----------- updata ----------")


    def select(self):
        fitness = []
        for p in self.Pop:
            fitness.append(p.WorkTime)

        pp = []
        secret_p = 1.5  # 选择压力

        sortF=sorted(fitness,reverse=True)

        # sorted = sorted.numpy()
        for i in range(len(fitness)):
            for j in range(len(sortF)):
                if fitness[i] == sortF[j]:
                    pp.append(j + 1)
                    break

        fitness = [(2 - secret_p + (2 * (p - 1) * (secret_p - 1)) / (len(self.Pop) - 1)) for p in pp]
        s = sum(fitness)
        p = [fitness[i] / s for i in range(len(fitness))]
        index = []
        # 通过赌盘法选择NP个染色体
        for i in range(len(self.Pop)):
            cum = 0
            m = random.random()
            for j in range(len(self.Pop)):
                cum += p[j]
                if cum >= m:
                    index.append(j)
                    break

        for i in range(len(FixedMes.Paternal)):
            two = np.random.choice(index, 2, False)
            FixedMes.Paternal[i] = two

        SumTime = 0
        BestTime = 9999999

        for i in FixedMes.AllFit:
            if i.WorkTime< BestTime:
                BestTime = i.WorkTime
            SumTime += i.WorkTime

        FixedMes.AverPopTime = SumTime / len(FixedMes.AllFit)
        FixedMes.Avufit[self.cur] = FixedMes.AverPopTime
        FixedMes.Bestfit[self.cur] = BestTime

    def Crossover(self):

        num_sonfit=0
        ge = FixedMes.ge

        for two in FixedMes.Paternal:
            # if two[0] == 0 and two[1]==0:
            #     break

            if self.cur<=FixedMes.AgenarationIten:
                k1 = FixedMes.cross
            else:
                k1 = FixedMes.cross*(FixedMes.cross1 - 2 * math.pow(math.e,-(float(self.cur)/float(ge))) / (1+math.pow(math.e,- (float(self.cur) / float(ge)))))
            num = utils.getRandNum(0, 100)
            if (k1 >= 0.99) :
                k1 = 0.99
            if (k1 <= 0.05):
                k1 = 0.05
            k1 = int((k1 * 100) % 100)
            if num <=k1:

                # 交叉
                temp1,temp2 = self.cr(FixedMes.AllFit[two[0]],FixedMes.AllFit[two[1]])

            else:
                temp1, temp2 = FixedMes.AllFit[two[0]], FixedMes.AllFit[two[1]]
            FixedMes.AllFitSon[num_sonfit]=copy.deepcopy(temp1)
            num_sonfit+=1
            FixedMes.AllFitSon[num_sonfit]=copy.deepcopy(temp2)
            num_sonfit+=1

    def cr(self,pop1,pop2):

        a = copy.deepcopy(pop1.codes)
        b = copy.deepcopy(pop2.codes)
        actsNum = len(FixedMes.act_info.keys())
        pos = random.randint(1,  actsNum - 1)
        # pos
        temp1 = copy.deepcopy(b[:pos])
        temp2 = copy.deepcopy(a[:pos])
        temp = copy.deepcopy(b[pos:])
        tempx = copy.deepcopy(a[pos:])
        for j in range(actsNum):
                for k in range(len(temp)):
                    if a[j][0] == temp[k][0]:
                        temp1 = np.concatenate((temp1, [temp[k]]))
                        break

        for j in range(actsNum):
                for k in range(len(tempx)):
                    if b[j][0] == tempx[k][0]:
                        temp2 = np.concatenate((temp2, [tempx[k]]))
                        break

        pop11 = Chromosome()
        pop11.setcodes(temp1.tolist())

        pop22 = Chromosome()
        pop22.setcodes(temp2.tolist())

        MyInit.fitness(pop11,[])
        MyInit.fitness(pop22, [])

        return pop11,pop22

    def Variation(self):
        ge = FixedMes.ge
        for i in range(len(FixedMes.AllFitSon)):
            k2=0
            if self.cur<=FixedMes.AgenarationIten:
                k2 = FixedMes.MutationRate
            else:
                k2 = FixedMes.MutationRate *(2 * math.pow(math.e,-(float(self.cur)/float(ge))) / (1+math.pow(math.e,- (float(self.cur) / float(ge)))))

            num = utils.getRandNum(0, 100)
            if (k2 >= 0.99):
                k2 = 0.99
            if (k2 <= 0.05):
                k2 = 0.05
            k2 = int((k2 * 100) % 100)

            if num <= k2:
                FixedMes.AllFitSon[i] = copy.deepcopy(self.var1(FixedMes.AllFitSon[i]))
    '''
    子图拓扑排序
    '''
    def  daluan(self,duan_code):
        newcode =[]
        newActs = defaultdict(lambda: [])
        for c in duan_code:
            newActs[c[0]] = []

        for act in duan_code:
            for i in duan_code:
                if act[0]==i[0]:
                    continue
                else:

                    if len(FixedMes.act_info[i[0]].predecessor)>0:
                        for o in FixedMes.act_info[i[0]].predecessor:
                            if act[0]==o:
                                newActs[i[0]].append(act[0])

        for a in range(len(duan_code)):
            random_Ei_0 = 0
            Ei_0 = []  # 紧前任务数为0的任务集编号
            for key, Ei in newActs.items():
                Ei_number = len(Ei)

                if Ei_number == 0:
                    Ei_0.append(key)
            random.shuffle(Ei_0)
            try:
               random_Ei_0 = Ei_0[0]
            except:
                print(duan_code)
                print(newActs)
            # self.taskid = taskid
            # self.belong_plane_id = jzjId
            newcode.append([random_Ei_0, FixedMes.act_info[random_Ei_0].belong_plane_id, FixedMes.act_info[random_Ei_0].taskid])
            for key, Ei in newActs.items():
                prece = newActs[key]
                if random_Ei_0 in prece:
                    prece.remove(random_Ei_0)
            del newActs[random_Ei_0]
        return newcode

    def var1(self,pop):

        newpop = copy.deepcopy(pop)
        a =newpop.codes
        duan_code = []
        i = np.random.choice(list(FixedMes.jzjOrdersNum.keys()), 1, replace=False)
        jzj = i[0]
        jzjOrdersNum = FixedMes.jzjOrdersNum[jzj]
        actsNum = len(FixedMes.act_info.keys())
        poslist = []  # 记录飞机i各工序在a中的位置
        for m in range(actsNum):
            # print("Varition",a[m])
            try:
                if a[m][1] == jzj:
                    poslist.append(m)
            except:
                print(len(a),m)

        # dr = np.random.choice([x for x in range(2,6)], 1, replace=False)[0]
        # TI = np.random.choice([x for x in range(1, FixedMes.planeOrderNum - 3 - dr)], 1, replace=False)

        Td = poslist
        x1 = Td[0]
        x2 = Td[-1]

        for gongxu in Td:
            duan_code.append(a[gongxu])

        newcode = self.daluan(duan_code)
        for q in range(len(poslist)):
            a.pop(Td[q] - q)

        number = [0]
        for i in range(len(poslist)):
            num = np.random.randint(number[-1]+1, len(a))
            number.append(num)
            a.insert(num, newcode[i])
        MyInit.fitness(newpop,[])

        return newpop


    def updata(self):
        FixedMes.AllFit = sorted(FixedMes.AllFit,key=lambda x:x.WorkTime)
        best = copy.deepcopy(FixedMes.AllFit[0])
        FixedMes.AllFitSon = sorted(FixedMes.AllFitSon,key=lambda x:-x.WorkTime)

        FixedMes.AllFit = copy.deepcopy(FixedMes.AllFitSon)
        FixedMes.AllFit[0] = copy.deepcopy(best)


if __name__ == '__main__':
    m = MyInit("C:/Users/29639/Desktop/dis.csv","C:/Users/29639/Desktop/order.txt")
    m.InitPopulation()
    run = MyRun()
    run.select()
    run.Crossover()
    ppp=FixedMes.AllFitSon[0]

    nwee = run.var1(ppp)
    run.updata()
    m.fitness(nwee,[],[])


    print(nwee.codes==ppp.codes)



































