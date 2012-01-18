from socketGHome import SocketGHome


class CapteursHTML():
    '''
    Classe Capteurs. Est appele lorsque l'utilisateur souhaite la liste des capteurs present
    '''

    def render_GET(self, request):
        '''
        Methode de reponse pour localhost:8000/capteurs/
        '''
        
        headerFile = open("../ClientPC/header.html")
        headerHtml = headerFile.read()
        headerFile.close()      
          
        capteurFile = open("../ClientPC/corps_capteur.html")
        capteurHtml = capteurFile.read()
        capteurFile.close()

        footerFile = open("../ClientPC/footer.html")
        footerHtml = footerFile.read()
        footerFile.close()

        return (headerHtml + capteurHtml + footerHtml)
    
    def render_POST(self, request):
        return self.render_GET(request)





class Capteurs():
    '''
    Cette classe gere un ensemble de capteurs enregistres dans le systeme
    '''
    
    def __init__(self):
        ''' Methode Initialisation de la classe '''
        self.capteurs={}
        
        
    
    def ajouterCapteur(self, capteur):
        '''
        Ajout d'un capteur
        '''
        
        
    def supprimerCapteur(self,capteur):
        '''
        Suppression du capteur passe en parametre
        '''
        
    
    def nbCapteurs(self):
        '''
        Retourne le nombre de capteurs enregistres au niveau du serveur
        '''

        
    def getCapteurs(self):
        '''
        Demande de la liste des capteurs a l'application Serveur
        Envoi par socket du message et attente de la liste
        '''
        message = 'INFO,00'
        SocketGHome.sendMsg(self, message)
        messageRecu = SocketGHome.receiveMsg(self)
        
        liste = messageRecu.split(',')