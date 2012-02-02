from rule import *
from transport import TransportGHome

condition1 = Condition("1","inf","10")
condition2 = ConditionDate("sup_date","08:00")
action1 = Action("20","21")
action2 = Action("14","27")
ensemble = Rules()
transport = TransportGHome()

# create data message
data = {}
data['msgType'] = 'newRule'
data['rule'] = {}
data["rule"]["ruleName"] = "Regle 1"
data['rule']['conditions'] = []
data["rule"]["conditions"].append(condition1)
data["rule"]["conditions"].append(condition2)

#print(data['rule']['condition'][1].type)

data['rule']['actions'] = []
data["rule"]["actions"].append(action1)
data["rule"]["actions"].append(action2)

# print(data["rule"])

# enregistrement du message
rule1 = Rule(data['rule'])

# creation du message json
jsonMsg = rule1.createJsonRule()
transport.sendRule(jsonMsg)
