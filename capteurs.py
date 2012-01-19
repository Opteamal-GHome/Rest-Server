from twisted.web import resource
import cgi

class CapteursHTML(resource.Resource):
    '''
    Classe Capteurs. Est appele lorsque l'utilisateur souhaite la liste des capteurs present
    '''

    def render_GET(self, request):
        '''
        Methode de reponse pour localhost:8000/capteurs/
        '''
        
        print("passe")
        
        headerFile = open("../ClientPC/header.html")
        headerHtml = headerFile.read()
        headerHtml = headerHtml.replace("$STYLE$", "core_capteurs.css")
        headerFile.close()      
        
        capteurFile = open("../ClientPC/core_capteurs.html")
        capteurHtml = capteurFile.read()
        capteurFile.close()

        footerFile = open("../ClientPC/footer.html")
        footerHtml = footerFile.read()
        footerFile.close()

        return (headerHtml + capteurHtml + footerHtml)
    
    def render_POST(self, request):
        return self.render_GET(request)

    def renderCorpsHTML (self):
        '''
        Modification de la page corps_capteurs pour ajouter les capteurs dans les box
        '''
        



class CapteursFactory():
    '''
    Cette classe gere un ensemble de capteurs enregistres dans le systeme
    '''
    
    def __init__(self):
        ''' Methode Initialisation de la classe '''
        capteur1 = Capteur(1, 'Salon', 'T', 15)
        capteur2 = Capteur(2, 'Chambre', 'P', 35)
        self.capteurs=[capteur1, capteur2]
        
        
    
    def ajouterCapteur(self, capteur):
        '''
        Ajout d'un capteur
        '''        
        if capteur.id not in self.getIDCapteurs():
            self.capteurs.append(capteur)
        
        
    def supprimerCapteur(self, idC):
        '''
        Suppression du capteur dont l'id est passe en parametre
        '''
        for capteur in self.capteurs :
            if capteur.id == idC:
                self.capteurs.remove(capteur)
            
    
    def nbCapteurs(self):
        '''
        Retourne le nombre de capteurs enregistres au niveau du serveur
        '''
        return len(self.capteurs)

                
    def getIDCapteurs(self):
        '''
        Renvoie la liste de tous les ID des capteurs presents sur le serveur Rest
        ''' 
        liste = []  
        for capteur in self.capteurs:
            liste.append(capteur.id)
        return liste
        
        
class Capteur():
    '''
    Classe Capteur
    '''
    
    def __init__(self, idC = "", nom = "", typeC = "", data = ""):
        # ID du capteur
        self.id = idC       
        # Nom du capteur
        self.nom = nom
        # Type du capteur
        self.type = typeC
        # Donnee (temperature, luminosite, etc.) du capteur
        self.data = data
        
    