from socketGHome import SocketGHome
from capteurs import Capteur
from rule import Rule

class TransportGHome():
    '''
    Envoi et Reception de Messages vers/depuis le serveur GHome
    '''
    
    def getCapteurs(self, ensembleCapteurs):
        '''
        Demande de la liste des capteurs a l'application Serveur
        Envoi par socket du message et attente de la liste
        '''
        message = 'INFO,00'
        SocketGHome.sendMsg(self, message)
        messageRecu = SocketGHome.receiveMsg(self)
        
        liste = messageRecu.split(',')
        typeMessage = liste[0]
        if typeMessage == 'CAPTEURS' :
            nbCapteurs = liste[1]

            # On cree une sous liste compose de liste de 3 elements            
            subList = [liste[n:n+3] for n in range(2, len(liste), 3)]
            
            # On cree des objets Capteur
            for sub in range(0,nbCapteurs):
                idCapteur = subList[sub][0]
                nomCapteur = subList[sub][1]
                typeCapteur = subList[sub][2]
                capteur = Capteur(idCapteur, nomCapteur, typeCapteur)
                
                ensembleCapteurs.ajouterCapteur(capteur)
                
    
    def getCapteur(self, idCapteur):
        '''
        Demande des informations d'un capteur dont l'id est passe en parametre
        '''
        message = 'INFO,' + idCapteur
        SocketGHome.sendMsg(self, message)
        messageRecu = SocketGHome.receiveMsg(self)
        
        liste = messageRecu.split(',')
        typeMessage = liste[0]
        numCapteur = liste[1]
        
        if typeMessage == 'CAPTEUR':
            if numCapteur == idCapteur :
                return liste[2]
                
                
    def sendRule(self, regle):
        '''
        Envoi d'une regle au serveur C
        '''
        SocketGHome.sendMsg(self,regle)
        
        
    def decode(self, msg):
        '''
        Trame entrante au format JSON
        '''
        if msg['msg'] == "rule":
            Rule.decodeJSONRule(msg)
   
   
