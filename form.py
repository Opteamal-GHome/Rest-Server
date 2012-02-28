from rule import *
from transport import TransportGHome
import json
from twisted.internet import task

from twisted.internet import reactor
from twisted.web.static import File

from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS


class WebSocketForm (WebSocketServerProtocol): 

    def onOpen(self):
        self.factory.register(self)  
    
    def onMessage(self, msg, binary):
        print 'reception : ' + str(msg)
        msg = json.loads(msg)
        #print msg["type"]
        self.factory.decode(msg)
        #self.sendMessage("Ca marche", binary)
               
    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class WebSocketFactory (WebSocketServerFactory):
    protocol = WebSocketForm   

    def __init__(self, url):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []
        

    def register(self, client):
        if not client in self.clients:
            print "registered client " + client.peerstr
            self.clients.append(client)
    
    def unregister(self, client):
        if client in self.clients:
            print "unregistered client " + client.peerstr
            self.clients.remove(client)
             
    def broadcast(self, msg):
        print "broadcasting message '%s' .." % msg
        print 'nbr Clients : ' + str(len(self.clients))
        for c in self.clients:
            print "send to " + c.peerstr
            c.sendMessage(json.dumps(msg))
                
    ###### RECEPTION DU CLIENT ######
    
    def decode(self, data):
        '''
        Decode le tableau recu
        '''
        if (data["msgType"] == "newRule"):
            # Nouvelle regle donnee par le client ; A envoyer au serveur GHome
            self.msgNewRuleC(data)    
        elif (data["msgType"] == "supprRule"):
            # Suppression d'une regle
            nomRule = data["ruleName"]
            self.ensembleRules.supprimerRule(nomRule)
        elif (data["msgType"] == "rename_device"):
            self.changeNameDevice(data)
        elif (data["msgType"] == "stat"):
            idCapteur = data["idC"]
            self.sendTemperature(idCapteur)
        
    def changeNameDevice(self, data):
        '''
        Change le nom d'un device
        '''
        capteurId = data["id"]
        newName = data["name"]
        
        capteur = self.capteursFactory.getCapteur(capteurId)
        capteur.nom = newName
        print 'Nom du capteur modifie'
            
    
    def msgNewRuleC (self, data):
        '''
        Cree une nouvelle regle et l'envoie au serveur C
        '''
        rule = Rule(data["rule"])  
        
        # On regarde si la regle n'est pas correcte
        if rule.error != "":
            self.msgAnswer("REFUSED", rule.error)
            
        # Si elle est correcte, on l'envoie au serveur C
        else:
            rule.priority = "1"
            rule.name = rule.name
            jsonMsg = rule.createJsonRule()
            
            jsonMsg = jsonMsg.replace('"type": u', '"type": ');
            jsonMsg = jsonMsg.replace('"rightOp": u', '"rightOp": ');
            jsonMsg = jsonMsg.replace('"leftOp": u', '"leftOp": ');
            jsonMsg = jsonMsg.replace('"actuator": u', '"actuator": ');
            jsonMsg = jsonMsg.replace('"value": u', '"value": ');
            jsonMsg = jsonMsg.replace('"ruleName": u', '"ruleName": ');
            
            print jsonMsg
            
            # Envoi de la regle au serveur C
            self.socketG.sendRule(jsonMsg)
            
            # Reception de la reponse
            answer = self.socketG.receiveAnswer()
            print 'Answer : ' + str(answer)
            answer = json.loads(answer)
            if answer["msgType"] == "R_newRule":
                if answer["status"] == "ACCEPTED":
                    # La regle a ete acceptee par le serveur
                    # On l'ajoute dans le fichier de sauvegarde des regles
                    self.saveFichier.writeNouvelleRule(rule)
                    
                    self.ensembleRules.ajouterRule(rule)
                    self.msgAnswer(answer["status"], "")
                else:
                    # La regle a ete refusee par le serveur
                    self.msgAnswer(answer["status"], answer["error"])
        
        
        
    ###### VERS LE CLIENT ######
    
    
    def changedDevice(self, idD, typeD, donnee):
        '''
        Envoye a l'utilisateur via les websockets lorsque la valeur d'un device a change
        '''
        data = {}
        data["msgType"] = "device_updated"
        data["id"] = idD
        data["data"] = donnee
        data["typeDevice"] = typeD
        
        print 'Changed Device Websocket : ' + str(data)
        self.broadcast(data)
        
    def msgAnswer(self, status, error):
        data = {}
        data["msgType"] = "answerRule"
        data["status"] = str(status)
        data["error"] = str(error)
        
        print 'data answer : ' + str(data)
        self.broadcast(data)
        
        
    def sendTemperature(self, idC):
        data = {}
        data["msgType"] = "tabStat"
        data["typeStat"] = "T"
        data["data"] = []
        
        # On va chercher le capteur concerne par la temperature
        capteur = self.capteursFactory.getCapteur(idC)
        for donnee in capteur.data:
            data["data"].append(donnee)
            
        self.broadcast(data)
        
