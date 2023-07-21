import random

import matplotlib as plt

def getRandNum(start,end):
    return (random.random() *100000) % (end -start)


def Dominate(Pop1, Pop2):
    '''
    :param Pop1:
    :param Pop2:
    :return: If Pop1 dominate Pop2, return True
    '''
    if (Pop1.f[0] < Pop2.f[0] and Pop1.f[1] < Pop2.f[1]) or \
            (Pop1.f[0] <= Pop2.f[0] and Pop1.f[1] < Pop2.f[1]) or \
            (Pop1.f[0] < Pop2.f[0] and Pop1.f[1] <= Pop2.f[1]):
        return True
    else:
        return False

def crowding_distance(NDSet):
    Distance = [0] * len(NDSet)
    NDSet_obj = {}

    for i in range(len(NDSet)):
        NDSet_obj[i] = NDSet[i].f

    ND = sorted(NDSet_obj.items(), key=lambda x: (x[1][0],x[1][1]))

    Distance[ND[0][0]] = 1e+20
    NDSet[0].c_distance = 1e+20
    Distance[ND[-1][0]] = 1e+20
    NDSet[-1].c_distance = 1e+20
    for i in range(1, len(ND) - 1):
        if Distance[ND[i][0]] == 0:
            Distance[ND[i][0]] = abs(ND[i + 1][1][0] - ND[i - 1][1][0]) + abs(ND[i + 1][1][1] - ND[i - 1][1][1])
            NDSet[i].c_distance = Distance[ND[i][0]]
    distance = dict(enumerate(Distance))
    New_distance = sorted(distance.items(), key=lambda x: x[1], reverse=True)
    L = [A[0] for A in New_distance]
    return L

def fast_non_dominated_sort(Pop):
            S = [[] for i in range(len(Pop))]
            front = [[]]
            n = [0 for i in range(len(Pop))]
            rank = [0 for i in range(len(Pop))]

            for p in range(len(Pop)):
                S[p] = []
                n[p] = 0
                for q in range(len(Pop)):
                    if Dominate(Pop[p], Pop[q]):
                        if q not in S[p]:
                            S[p].append(q)
                            Pop[p].sp.append(q)

                    elif Dominate(Pop[q], Pop[p]):
                        n[p] = n[p] + 1
                        Pop[p].np+=1
                if n[p] == 0:
                    rank[p] = 0
                    if p not in front[0]:
                        front[0].append(p)
            i = 0
            while (front[i] != []):
                Q = []
                for p in front[i]:
                    for q in S[p]:
                        n[q] = n[q] - 1
                        if (n[q] == 0):
                            rank[q] = i + 1
                            Pop[q].rank = i+1
                            if q not in Q:
                                Q.append(q)
                i = i + 1
                front.append(Q)
            del front[len(front) - 1]
            NDSet = []
            for Fi in front:
                NDSeti = []
                for pi in Fi:

                    NDSeti.append(Pop[pi])
                NDSet.append(NDSeti)
            return NDSet

def getTwoDimensionListIndex(L, value):
    index1 = -1
    index2 = -1
    """获得二维列表某个值的一维索引值的另一种方法"""
    for i in range(len(L)):
        for j in range(len(L[i])):
            if len(L[i][j]):
                for m in range(len(L[i][j])):
                    if L[i][j][m] == value:
                        index1 = i
                        index2 = j
    return index1, index2

#判断是否存在重复
def judgeDuplicated(array):
    array.sort()
    count=0
    while count<len(array)-1:
        if array[count]==array[count+1]:
            return True
        else:
            count+=1
    return False

#多目标 帕累托前沿画图
def Plot_NonDominatedSet(EP):
    x = []
    y = []
    for i in range(len(EP)):
        x.append(EP[i].f[0])
        y.append(EP[i].f[1])
    plt.plot(x, y, '*')
    plt.xlabel('makespan')
    plt.ylabel('Average Load')
    plt.legend()
    plt.savefig(r'obj_result/'+'first'+'.png')
    plt.close()


def writeTxt(filename,content):
    with open(filename, 'w') as f:
        for i in content:
            f.write(i + '\n')

if __name__ == '__main__':
    cotent=[]
    cotent.append("2 3 4 ")
    cotent.append("2 3 4")

    writeTxt("1.txt", cotent)
