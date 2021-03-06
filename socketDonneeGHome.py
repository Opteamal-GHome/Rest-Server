import constantes, json

from twisted.internet.protocol import Protocol, Factory

from form import WebSocketForm
from capteurs import *
from actionneurs import *

class SocketDataGHome(Protocol) :
    '''
    Client Socket to connect to server GHome developped with C language.
    '''
    
    def connectionMade(self):
        print "Connected from", self.transport.client
                
    def dataReceived(self, data):
        print 'Data Socket Data : ' + str(data)
        self.factory.decode(data)

    def connectionLost(self, reason):
        print "Disconnected from", self.transport.client
        


class SocketDataGHomeFactory(Factory):
    
    protocol = SocketDataGHome

    def __init__(self, factoryCapteurs, factoryActionneurs, ensRules, transport, ws):
        self.port = constantes.portServerData
        self.capteursFactory = factoryCapteurs
        self.actionneursFactory = factoryActionneurs
        self.ensRules = ensRules
        self.transport = transport
        self.ws = ws
        print 'Initialisation du socket Data GHome sur '
        
        
    def decode(self, msg):
        print 'Recu de la socket Donnee : ' + str(msg)
        data = json.loads(msg)
        
        # Un dispositif a vu sa valeur changer
        if data["msgType"] == "device_updated":
        
            # Si le dispositif est un capteur
            if data["role"] == "S":
                capteur = self.capteursFactory.getCapteur(data["id"])
                
                # Ajout d'un nouveau capteur
                if capteur == None:
                    print 'Ajout Nouveau Capteur Socket Donnee'
                    newCapt = Capteur(data["id"], "", data["type"], data["data"])
                    self.capteursFactory.ajouterCapteur(newCapt)
                # Modification d'un capteur existant
                else:
                    print 'Modification Capteur Socket Donnee'
                    self.capteursFactory.modifierCapteur(data["id"], data["data"])
                    
                    print self.capteursFactory.getCapteur(data["id"]).data
            
            
            # Si le dispositif est un actionneur
            elif data["role"] == "A":
                actionneur = self.actionneursFactory.getActionneur(data["id"])
                
                # Ajout d'un nouveau capteur
                if actionneur == None:
                    newAct = Actionneur(data["id"], "", data["type"], data["data"])
                    self.actionneursFactory.ajouterActionneur(newAct)
                # Modification d'un capteur existant
                else:
                    self.actionneursFactory.modifierActionneur(data["id"], data["data"])
        
            print 'Data : ' + data["data"]        
            self.ws.changedDevice(data["id"], data["type"], data["data"])
            
            
        # Demande de toutes les regles par le serveur C
        elif data["msgType"] == "get_rules":
            
            # On doit envoyer toutes les regles au serveur C
            for rule in self.ensRules.rules:
                self.transport.sendRule(rule.createJsonRule())
