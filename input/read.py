import json
from collections import defaultdict

import FixedMess
from Activitity import Order


def read(filename):
    id = 0
    ## 电、氧气、氮气、液压、空调、加油、挂弹、惯导
    orderDict = {
        'D': 2,
        'YQ': 3,
        'DQ': 4,
        'YY': 5,
        'KT': 6,
        'JY': 7,
        'HKDY': 8,
        'GD': 9
    }
    sucDict = defaultdict(lambda: [])
    preDict = defaultdict(lambda: [])
    activities = {}
    infos = json.load(open(filename, 'r', encoding='utf-8'))
    planeNums = len(infos)
    #每个舰载机的首节点ID
    startIDs = []
    endIDs = []
    for i in range(planeNums):
        jzjInfo = infos[i]
        # 舰载机编号
        jzjNumber = jzjInfo['no']-1000
        # 舰载机类型
        jzjType = jzjInfo['type']
        # 最早开始保障时间
        es = jzjInfo['start_time']
        FixedMess.FixedMes.jzjStartTime[jzjNumber-1] = es
        # 最晚保障结束时间
        lf = jzjInfo['launch_time']
        # 工序集合
        orders = jzjInfo['action']
        record = {}
        Orders=[]
        #虚节点
        id += 1
        Orders.append(Order(id, 0, jzjNumber, jzjType, 0, [], 0, 0))

        startIDs.append(id)
        for j in range(len(orders)):
            id += 1
            # 工序名称
            orderName = orders[j]['name']
            # 工序id
            taskId = orderDict[orderName]
            record[taskId] = id
            # 工序可用设备编号
            avilableResource = strList(orders[j]['resource'])
            # 时长
            durtion = orders[j]['cost']
            # id, taskid , jzjId, duration, resourceRequestS, successor,es,lf
            newOrder = Order(id, taskId, jzjNumber,jzjType, durtion, avilableResource, es, lf)
            newOrder.needNums =1
            Orders.append(newOrder)
        # 虚节点
        id += 1

        Orders.append(Order(id, 0, jzjNumber, jzjType, 0, [], 0, 0))
        endIDs.append(id)
        FixedMess.FixedMes.jzjOrdersNum[jzjNumber] = endIDs[-1]-startIDs[-1]+1

        for order in Orders[1:-1]:
            taskId = order.taskid
            iid = order.id
            for sucOrderId in FixedMess.FixedMes.SUCOrder[taskId]:
                if sucOrderId in record.keys():
                    sucDict[iid].append(record[sucOrderId])

            for s in sucDict[iid]:
                    preDict[s].append(iid)

        for Id in record.values():
            if Id not in preDict.keys():
                preDict[Id] = []
            if Id not in sucDict.keys():
                sucDict[Id] = []

        for order in Orders[1:-1]:
            if len(preDict[order.id]) == 0:
                sucDict[Orders[0].id].append(order.id)
                preDict[order.id].append(Orders[0].id)
            if len(sucDict[order.id]) == 0:
                preDict[Orders[-1].id].append(order.id)
                sucDict[order.id].append(Orders[-1].id)
            order.successor = sucDict[order.id]
            order.predecessor = preDict[order.id]
            activities[order.id] = order

        Orders[0].successor = sucDict[Orders[0].id]
        activities[Orders[0].id] = Orders[0]
        Orders[-1].predecessor = preDict[Orders[-1].id]
        activities[Orders[-1].id] = Orders[-1]

    for Id in startIDs:
        activities[Id].predecessor=[0]
    for Id in endIDs:
        activities[Id].successor=[id+1]
    # 总的虚拟头结点
    activities[0] = Order(0, 0, 0, '', 0, [], 0, 0)
    activities[0].predecessor = []
    activities[0].successor = [id for id in startIDs]

    # 总的虚拟尾结点
    activities[id+1] = Order(id , 0, 0, '', 0, [], 0, 0)
    activities[id+1].successor = []
    activities[id+1].predecessor = [id for id in endIDs]
    return activities
import re

def remove_letters_and_convert_to_numbers(string):
    pattern = '[a-zA-Z]'  # 匹配字母的正则表达式模式
    result = re.sub(pattern, '', string)  # 替换字母为空字符串
    return int(result)  # 将结果转换为整数

def strList(strlist):
    nums=[]
    for shebeiName in strlist:
        nums.append(remove_letters_and_convert_to_numbers(shebeiName))
    return nums

if __name__ == '__main__':
    print(strList(['GD01','GD02']))

    avilableResource = int('03')
    print(avilableResource)
    read("input.json")
