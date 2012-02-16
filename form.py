from rule import *
from transport import TransportGHome
import json
from twisted.internet import task

from twisted.internet import reactor
from twisted.web.static import File

from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS


class WebSocketForm (WebSocketServerProtocol):   
    
    def onMessage(self, msg, binary):
        print 'reception'
        msg = json.loads(msg)
        #print msg["type"]
        self.factory.decode(msg)
        #self.sendMessage("Ca marche", binary)


               


class WebSocketFactory (WebSocketServerFactory):
    protocol = WebSocketForm   

    def __init__(self, url):
        WebSocketServerFactory.__init__(self, url)
        
        # Creation d'un nouveau tableau de rule
        self.ensembleRules = Rules()
        
        
    def getEnsRules(self):
        return self.ensembleRules
                
    ###### RECEPTION DU CLIENT ######
    
    def decode(self, data):
        '''
        Decode le tableau recu
        '''
        if (data["type"] == "newRule"):
            # Nouvelle regle donnee par le client ; A envoyer au serveur GHome
            self.msgNewRuleC(data)    
        elif (data["type"] == "supprRule"):
            # Suppression d'une regle
            nomRule = data["ruleName"]
            self.ensembleRules.supprimerRule(nomRule)
        #elif (data["type"] == "getStatTemp"):
            
    
    def msgNewRuleC (self, data):
        '''
        Cree une nouvelle regle et l'envoie au serveur C
        '''
        rule = Rule(data["rule"])     
        rule.priority = "1"
        rule.name = "Nouvelle"
        self.ensembleRules.ajouterRule(rule)
        jsonMsg = rule.createJsonRule()
        
        jsonMsg = jsonMsg.replace('"type": u', '"type": ');
        jsonMsg = jsonMsg.replace('"rightOp": u', '"rightOp": ');
        jsonMsg = jsonMsg.replace('"leftOp": u', '"leftOp": ');
        jsonMsg = jsonMsg.replace('"actuator": u', '"actuator": ');
        jsonMsg = jsonMsg.replace('"value": u', '"value": ');
        
        print jsonMsg
        
        # Envoi de la regle au serveur C
        #self.socketG.sendRule(jsonMsg)
        
        # Reception de la reponse
        #print self.socketG.receiveAnswer()
        
        
    ###### VERS LE CLIENT ######
    
    
    def changedDevice(self, idD, data):
        '''
        Envoye a l'utilisateur via les websockets lorsque la valeur d'un device a change
        '''
        data = {}
        data["msgType"] = "device_updated"
        data["id"] = idD
        data["data"] = data
        self.send(data)
        
        
            
            
    ###### WEBSOCKETS OUTILS ######