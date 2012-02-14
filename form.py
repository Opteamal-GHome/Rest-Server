from rule import Rule
from transport import TransportGHome
import json

from websocket import *

class WebSocketInit (WebSocketSite):
    '''
    Initialisation des webSockets
    '''
    def __init__(self, resource):
        WebSocketSite.__init__(self, resource)


class WebSocketForm (WebSocketHandler):
    '''
    Reception des trames JSON et re-envoi via les websockets conformement au protocole defini.
    '''
    def __init__(self, tran):
        WebSocketHandler.__init__(self, tran)
        # Socket vers le serveur C
        self.socketG = TransportGHome

    
    def send(self, msgJSON):
        """
        Envoie un message JSON au client.
        """
        self.transport.write(json.dumps(msgJSON))
        
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
        self.socketG.sendRule(jsonMsg)
        
        # Reception de la reponse
        print self.socketG.receiveAnswer()
    
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
            


    def frameReceived(self, frame):
        #Called by the websocket library when a new frame is received.
        self.decode(json.loads(frame))
        
       
    def connectionMade(self):
        #Called by the websocket library when the connection with the client has been established.
        print 'Connected to client.'
        

    def connectionLost(self, reason):
        #Called by the websocket library, the connection has been lost
        print 'Deconnected of client'