from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from FixedMess import FixedMes

def judge0(time1,time2,bar):
    flag=True
    for i in range(time1,time2):
        if bar[i] == 1:
            flag =False
            break
    return flag

def modify(time1,time2,bar):
    for i in range(time1, time2):
        bar[i] = 1
def Draw_gantt_singe(allTask,ds):
    plt.clf()
    colors = ['red', 'dodgerblue', 'mediumseagreen', 'blueviolet', 'orange',  # 主体颜色
             'darkred', 'blue', 'green', 'indigo', 'orangered',  # 边框颜色
             'salmon', 'lightskyblue', 'aquamarine', 'plum', 'moccasin']

    bar1 = [0 for _ in range(3000)]
    bar2 = [0 for _ in range(3000)]
    bar3 = [0 for _ in range(3000)]
    bar4 = [0 for _ in range(3000)]
    bars = [0, 0.25, 0.5, 0.75]
    Bars = []
    Bars.append(bar1)
    Bars.append(bar2)
    Bars.append(bar3)
    Bars.append(bar4)
    allTask = sorted(allTask.items(), key=lambda d: d[0], reverse=False)
    listJzj = list(FixedMes.jzjOrdersNum.keys())
    for i in range(len(allTask)):

        jzjNumber = allTask[i][1].belong_plane_id
        if jzjNumber==0:
            continue
        indexn = listJzj.index(jzjNumber)

        op =  len(allTask[i][1].predecessor)
        if op ==1 and allTask[i][1].predecessor[0]==0:
            bar1 = [0 for _ in range(3000)]
            bar2 = [0 for _ in range(3000)]
            bar3 = [0 for _ in range(3000)]
            bar4 = [0 for _ in range(3000)]
            bars = [0, 0.25, 0.5, 0.75]
            Bars = []
            Bars.append(bar1)
            Bars.append(bar2)
            Bars.append(bar3)
            Bars.append(bar4)

        time1 = allTask[i][1].es
        time2 = allTask[i][1].ef
        if (time2 - time1) != 0 :
            tsk = allTask[i][1].taskid-2

            for Bar in range(len(Bars)):
                if judge0(time1,time2,Bars[Bar]):
                        plt.barh((indexn+1)-bars[Bar], time2 - time1,height=0.3,
                         left=time1, color=colors[tsk],edgecolor='b',linewidth=0.03)
                        # news = str(op)
                        infmt = '(' + str(tsk+1) + ')'
                        plt.text(x=time1, y=(indexn+1)-bars[Bar]-0.06, s=infmt, fontsize=6,
                                 color='white')
                        modify(time1,time2,Bars[Bar])
                        break

    label_name = ['开电','充氧','充氮','液压','空调','加油','挂弹','惯导']
    patches = [mpatches.Patch(color=colors[i], label=label_name[i]) for i in range(len(label_name))]
    plt.legend(handles=patches, loc=0)
    y = range(1,len(listJzj)+1,1)
    # x = range(1,100,5)
    plt.yticks(y,["jzj"+ str(i)  for i in listJzj])
    # plt.xticks(x)
    # plt.show()
    plt.savefig(ds)


