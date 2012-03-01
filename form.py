from rule import *
from group import *
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
        elif (data["msgType"] == "rule_removed"):
            nomRule = data["rule"]
            self.removeOneRule(nomRule)
        elif (data["msgType"] == "rename_device"):
            self.changeNameDevice(data)
        elif (data["msgType"] == "stat"):
            idCapteur = data["idC"]
            self.sendTemperature(idCapteur)
        elif (data["msgType"] == "priorities"):
            self.changePriorities(data["rules"])
        elif (data["msgType"] == "meteo"):
            self.changeMeteo(data["codePostal"])
        elif (data["msgType"] == "new_group"):
            self.createNewGroup(data["name"], data["type"], data["devices"])
        elif (data["msgType"] == "remove_group"):
            self.deleteGroup(data["name"])
            
    def createNewGroup(self, nom, typeG, devices):
        '''
        Nouveau groupe detecte
        '''
        # Remplissage newGroup
        newGroup = Group()
        newGroup.nom = nom
        newGroup.typeGroupe = typeG
        for device in devices:
            newGroup.ajouterPeriph(device)
            
        # Ajout du groupe dans l'ensemble des groupes existants
        self.ensembleGroupes.ajouterGroupe(newGroup)
        print 'Groupe ' + nom + ' ajoute'
        
    def deleteGroup(self, nomGroupe):
        '''
        Supprime un groupe dont le nom est passe en parametre
        '''
        
        trouve = self.ensembleGroupes.removeGroupe(nomGroupe)
        if trouve == True:
            print 'Groupe ' + nomGroupe + ' supprime'
        
            
    def changeMeteo(self,codePostal):
        ''' 
        Changement de la meteo 
        '''
        data = {}
        data["msgType"] = "meteo"
        data["codePostal"] = str(codePostal)
        jsonMsg = str(data)
        
        self.socketG.sendMsg(jsonMsg)
        
        
    def changeNameDevice(self, data):
        '''
        Change le nom d'un device
        '''
        idRecupere = data["id"]
        newName = data["name"]
        
        # On recupere le capteur correspondant
        device = self.capteursFactory.getCapteur(idRecupere)
        
        # Si la recuperation a echoue, c'est qu'on essaye de recuperer un actionneur
        if (device == None):
            device = self.actionneursFactory.getActionneur(idRecupere)
        
        # On change ensuite le nom
        device.nom = newName
        print 'Nom du device modifie'
        
    def changePriorities(self, rules):
        '''
        Changement des priorites des regles chez le client. Refactoring des priorites sur le serveur Python. Envoi au Serveur C
        '''
        # Change les priorites sur le serveur Python
        numPriorite = 0
        for nomRule in rules:
            self.ensembleRules.modifierPrioriteRule(str(nomRule),numPriorite)
            numPriorite = numPriorite + 1
            
        # Recree le fichier de rules
        self.saveFichier.removeAllRules()
        self.saveFichier.writeAllRules()
        
        # Envoie les nouvelles priorites au serveur C
        data = {}
        data["msgType"] = "changeRulesPriorities"
        data["rules"] = []
        for nomRule in rules:
            data["rules"].append(str(nomRule))
            
        jsonMsg = str(data)
        self.socketG.sendMsg(jsonMsg)
        
        
    def removeOneRule (self, name):
        ''' 
        Envoie au serveur C le nom de la regle a supprimer
        '''
        
        # Suppression d'une regle cote python
        self.ensembleRules.supprimerRule(name)
        
        # Envoi de la regle a supprimer au serveur C
        data = {}
        data["msgType"] = "removeRule"
        data["ruleName"] = str(name)
        
        jsonMsg = str(data)
        self.socketG.sendMsg(jsonMsg)
        
        # Reecriture du fichier de sauvegarde des regles
        self.saveFichier.removeAllRules()
        self.saveFichier.writeAllRules()
            
    
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
        
