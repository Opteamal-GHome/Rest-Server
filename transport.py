from socketGHome import SocketGHome
import simplejson as json
from rule import Rule
from actionneurs import Actionneur
from capteurs import Capteur

class TransportGHome():
    '''
    Envoi et Reception de Messages vers/depuis le serveur GHome
    '''
    
    def __init__(self):
        self.transport = SocketGHome()
    
    def getAllDevices(self, capts, actuators):
        '''
        Demande de la liste des capteurs a l'application Serveur
        Envoi par socket du message et attente de la liste
        '''
        # Message d'envoi
        data = {}
        data["msgType"] = "getAllDevices"
        jsonRule = str(data)
        
        # Envoi Message
        self.transport.sendMsg(jsonRule)
        
        # Reception Message : Parsage
        msgRcv = self.transport.receiveMsg()
        print msgRcv
        dataMsg = json.loads(msgRcv)
        if dataMsg["msgType"] == "R_getAllDevices":
            for capteur in dataMsg["sensors"]:
                capteur1 = Capteur(capteur["id"], "", capteur["type"], capteur["data"])
                
                # Si le capteur n'existe pas deja, on l'ajoute
                if (capts.getCapteur(capteur["id"]) == None):
                    capts.ajouterCapteur(capteur1)
                # Sinon, on le modifie
                else:
                    capts.modifierCapteur(capteur["id"], capteur["data"])
                
            for actuator in dataMsg["actuators"]:
                actuator1 = Actionneur(actuator["id"], "", actuator["type"], actuator["data"])
                
                # Si l'actionneur n'existe pas deja, on l'ajoute
                if (actuators.getActionneur(actuator["id"]) == None):
                    actuators.ajouterActionneur(actuator1)
                # Sinon, on le modifie
                else:
                    actuators.modifierActionneur(actuator["id"], actuator["data"])
                
    
    def getDevice(self, idDevice, tab):
        '''
        Demande des informations d'un dispositif dont l'id est passe en parametre
        On considere que ce capteur est deja connu par le serveur Rest
        '''
        # Message d'envoi
        data = {}
        data["msgType"] = "getDevice"
        data["id"] = str(idDevice)
        jsonRule = str(data)
        
        # Envoi Message
        self.transport.sendMsg(jsonRule)
        
        # Reception Message : Parsage
        msgRcv = self.transport.receiveMsg()
        dataMsg = json.loads(msgRcv)
        if dataMsg["msgType"] == "getDevice":
            if dataMsg["id"] == idDevice:
                if dataMsg["typeDevice"] == "sensor":
                    tab.modifierCapteur(idDevice,dataMsg["data"])
                elif dataMsg["typeDevice"] == "actuator":
                    tab.modifierActionneur(idDevice, dataMsg["data"])
     
    def getAllRules(self, ensRules):
        '''
        Demande au serveur C l'ensemble des regles enregistrees
        '''     
        # Message d'envoi       
        data = {}
        data["msgType"] = "getAllRules"
        jsonData = str(data)
        
        # Envoi message
        self.transport.sendMsg(jsonData)
        
        # Reception message
        msgRcv = self.transport.receiveMsg()
        dataMsg = json.loads(msgRcv)
        
        
                
    def sendRule(self, regle):
        '''
        Envoi d'une regle au serveur C
        '''
        self.transport.sendMsg(regle)
        
    def receiveAnswer(self):
        '''
        Reception d'un message par le serveur C
        '''
        return self.transport.receiveMsg()
        
        
    def decode(self, msg):
        '''
        Trame entrante au format JSON
        '''
        if msg['msg'] == "rule":
            Rule.decodeJSONRule(msg)
   
   
