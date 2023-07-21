import json
from json import JSONEncoder
import FixedMess
from Activitity import jsonOrder

class MyEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__

def outputJson(allTasks,filename):

    orderDict = {
        2: "D",
        3: "YQ",
        4: "DQ",
        5: "YY",
        6: "KT",
        7: "JY",
        8: "HKDY",
        9: "GD"
    }
    jzjIds = list(FixedMess.FixedMes.jzjOrdersNum.keys())
    jsonObjects = [ jsonOrder() for i in jzjIds]
    for key, order in allTasks.items():
        if order.belong_plane_id == 0:
            continue
        jsonObject = jsonObjects[jzjIds.index(order.belong_plane_id)]
        jsonObject.type = order.jzjType
        if order.belong_plane_id < 10:
            jsonObject.no = "100"+str(order.belong_plane_id)
        else:
            jsonObject.no = "10" + str(order.belong_plane_id)
        action = {}
        # "name": "GD",
        # "resource": "GD01",
        # "start_time": 0,
        # "end_time": 120
        if order.taskid == 1 or order.taskid==0:
            continue
        action["name"] = orderDict[order.taskid]
        workIndex = order.SheiBei[0][1]+1
        if workIndex<10:
            resource = action["name"] + "0"+str(workIndex)
        else:
            resource = action["name"] + str(workIndex)
        action["resource"] = resource
        action["start_time"] = order.es
        action["end_time"] = order.ef
        jsonObject.action.append(action)

    with open("{}.json".format(filename), "w") as f:
            json.dump(jsonObjects, fp =f,cls=MyEncoder,indent=1)
            print("已生成output.json文件...")

if __name__ =='__main__':
    with open("news_json.json", "w") as f:
        json.dump({}, fp=f)
        print("已生成output.json文件...")