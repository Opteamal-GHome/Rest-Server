from twisted.web import resource

class CapteursHTML(resource.Resource):
    '''
    Classe Capteurs. Est appele lorsque l'utilisateur souhaite la liste des capteurs present
    '''
    
    def __init__(self, capteurFactory):
        self.factory = capteurFactory
        

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
        capteurHtml = capteurHtml.replace("$LISTECAPTEURS$", self.renderCorpsHTML())
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
        page = ""
        for capteur in self.factory.capteurs:
            # Nom du capteur
            page +=  """<div class="capteur">
            <div class="nom_capteur">""" + str(capteur.nom) + """</div>"""
            
            # Image du capteur
            if capteur.type == 'T':
                page += """<img class="img_capteur" src="Thermometer_1_24282.png"> """
            elif capteur.type == 'P':
                page += """<img class="img_capteur" src="bulb.png">"""
                
            # Valeur Data du capteur
            page += """<div class="val_capteur">""" + str(capteur.data) + """</div>"""              
            page += """</div>"""


        return page


class CapteursFactory():
    '''
    Cette classe gere un ensemble de capteurs enregistres dans le systeme
    '''
    
    def __init__(self):
        ''' Methode Initialisation de la classe '''
        capteur1 = Capteur(1, 'Salon', 'T', 15)
        capteur2 = Capteur(2, 'Chambre', 'P', 35)
        capteur3 = Capteur(3, 'Salle de bain', 'T', 20)
        self.capteurs=[capteur1, capteur2, capteur3]
        
        
    
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
            
    def modifierCapteur(self, idC, dataC):
        '''
        Modifie la valeur du capteur identifie par un id et une donnee
        '''
        for capteur in self.capteurs :
            if capteur.id == idC:
                capteur.data = dataC
        
    
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
        
    