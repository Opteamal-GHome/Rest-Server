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
        dataMsg = json.loads(msgRcv)
        if dataMsg["msgType"] == "R_getAllDevices":
            for capteur in dataMsg["sensors"]:
                capteur1 = Capteur(capteur["id"], "", capteur["type"], capteur["data"])
                capts.ajouterCapteur(capteur1)
                
            for actuator in dataMsg["actuators"]:
                actuator1 = Actionneur(actuator["id"], "", actuator["type"], actuator["data"])
                actuators.ajouterActionneur(actuator1) 
                
    
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
                
        
                
    def sendRule(self, regle):
        '''
        Envoi d'une regle au serveur C
        '''
        self.transport.sendMsg(regle)
        
        
    def decode(self, msg):
        '''
        Trame entrante au format JSON
        '''
        if msg['msg'] == "rule":
            Rule.decodeJSONRule(msg)
   
   
