from rule import *
from transport import TransportGHome
import socket, sys

#condition1 = Condition("1","inf","10")
#condition2 = ConditionDate("sup_date","08:00")
#action1 = Action("20","21")
#action2 = Action("14","27")
#ensemble = Rules()
#transport = TransportGHome()
#
## create data message
#data = {}
#data['msgType'] = 'newRule'
#data['rule'] = {}
#data["rule"]["ruleName"] = "Regle 1"
#data['rule']['conditions'] = []
#data["rule"]["conditions"].append(condition1)
#data["rule"]["conditions"].append(condition2)
#
##print(data['rule']['condition'][1].type)
#
#data['rule']['actions'] = []
#data["rule"]["actions"].append(action1)
#data["rule"]["actions"].append(action2)
#
## print(data["rule"])
#
## enregistrement du message
#rule1 = Rule(data['rule'])
#
## creation du message json
#jsonMsg = rule1.createJsonRule()
#transport.sendRule(jsonMsg)


 
HOST = '134.214.167.59'
GET = '/rss.xml'
PORT = 421
 
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    sys.stderr.write("[ERROR] %s\n" % msg[1])
    sys.exit(1)
 
try:
    sock.connect((HOST, PORT))
except socket.error, msg:
    sys.stderr.write("[ERROR] %s\n" % msg[1])
    sys.exit(2)
 
#sock.send("GET %s HTTP/1.0\r\nHost: %s\r\n\r\n" % (GET, HOST))
sock.send("coucou autre ordi")
 
data = sock.recv(1024)
string = ""
while len(data):
    string = string + data
    data = sock.recv(1024)
sock.close()
 
print string
 
sys.exit(0)
