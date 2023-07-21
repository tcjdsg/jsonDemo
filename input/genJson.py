
import json
from json import JSONEncoder

import pandas as pd
from Activitity import genjsonOrder

# 读取 Excel 文件的多个工作表
# 要读取的工作表列表
data_lists = []  # 用于存储每个工作表的数据帧字典
orderDict = {
    1: "D",
    2: "YQ",
    3: "DQ",
    4: "YY",
    5: "KT",
    6: "JY",
    7: "HKDY",
    8: "GD"
}


class MyEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__
sheets_to_read = ['actions', 'resources']
# 逐个读取工作表并存储到字典中

df = pd.read_excel('info.xlsx', sheet_name='actions')
df = df.iloc[1:]  # 去除第一行数据
actions = df.values.tolist()  # 将数据转换为列表

df = pd.read_excel('info.xlsx', sheet_name='resources')
df = df.iloc[1:]  # 去除第一行数据
resources = df.values.tolist()  # 将数据转换为列表

jsonObjects = [ genjsonOrder() for i in range(len(actions))]
for i in range(len(actions)):
    jsonOrder = jsonObjects[i]

    jzjInfo = actions[i]

    jsonOrder.no = jzjInfo[0]
    jsonOrder.type = jzjInfo[1]

    # 工序
    orders = jzjInfo[4:]
    for taskId in range(len(orders)):
        record = {}
        if orders[taskId] > 0:
            record["name"] = orderDict[taskId + 1]
            #resource:
            r = resources[i][taskId+1]
            record["resource"] = list(r.split(','))
            record["cost"] = orders[taskId]
            jsonOrder.action.append(record)

    jsonOrder.start_time = jzjInfo[2]
    jsonOrder.launch_time = jzjInfo[3]

with open("input.json", "w") as f:
            json.dump(jsonObjects, fp =f,cls=MyEncoder,indent=1)
            print("已生成intput.json文件...")




