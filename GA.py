from matplotlib import pyplot as plt
from Mythread import myRun,myInit
from FixedMess import FixedMes
import os

from draw import Draw_gantt_singe
from output.output import outputJson

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
class Ga(object):
    def __init__(self,dis_file,order_file):
        self.dis_file = dis_file
        self.order_file = order_file
        self.Init = myInit.MyInit(self.dis_file, self.order_file)
        #电、氧、氮、液压、空调、加油、挂弹、惯导
        #D  YQ DY  YY   KT   JY  HKGD  GD
        self.jineng1 = [12,12,12,12,12,12,12,12]

    def Run(self):

        FixedMes.my()
        self.run = myRun.MyRun()
        self.DCmin=10
        record=""
        for s in self.jineng1:
            record+=(str(s)+".")

        ds = "output/output"
        tu = "figure/banzu -" + record + ".png"
        self.first(ds, tu)

    def first(self, filename1, filename2):
        FixedMes.total_station_resource = self.jineng1
        self.Init.InitPopulation()

        for it in range(FixedMes.ge):

            self.run.RUN(it)
            print("------{}-------BestTime:{}----".format(it, FixedMes.Bestfit[it]))

        sortFit = sorted(FixedMes.AllFit,key=lambda x:x.WorkTime)
        pop = sortFit[0]
        print(pop.codes)

        Station = []
        Stations,allTasks = self.Init.fitness(pop, Station)
        print("BestTime:{}-----".format(pop.WorkTime))

        plt.rcParams['font.sans-serif'] = ['SimHei']
        print("正在记录。。。。。")

        outputJson(allTasks, filename1)
        Draw_gantt_singe(allTasks,filename2)

        print("记录成功")


if __name__ == '__main__':
   g = Ga("input/dis.csv", "input/input.json")
   g.Run()