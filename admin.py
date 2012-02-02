from twisted.web import resource
import netifaces as ni

class AdminHTML(resource.Resource):
    
    def __init__(self,capteursFactory, actionneursFactory):
        self.captFactory = capteursFactory
        self.actionFactory = actionneursFactory
        
    
    def render_GET(self, request):
        '''
        Methode de reponse a localhost:5000/admin
        '''
        
        headerFile = open("../ClientPC/header.html")
        headerHtml = headerFile.read()
        headerHtml = headerHtml.replace("$STYLE$", "core_admin.css")
        headerFile.close()      
        
        adminFile = open("../ClientPC/core_admin.html")
        adminHtml = adminFile.read()
        adminHtml = adminHtml.replace("$IPSERVEUR$", str(ni.ifaddresses('eth0')[2][0]['addr'])+":8080")
        adminHtml = adminHtml.replace("$LISTECAPTEURS$", self.renderListeCapteursExistants())
        adminHtml = adminHtml.replace("$LISTEACTIONNEURS$", self.renderListeActionneursExistants())
        adminFile.close()

        footerFile = open("../ClientPC/footer.html")
        footerHtml = footerFile.read()
        footerFile.close()
        
        return headerHtml + adminHtml + footerHtml
        
        
    def render_POST(self, request):
        return self.render_GET(request)
    
    def renderListeCapteursExistants(self):
        '''
        Modification de la page corps_admin pour ajouter les capteurs
        <li id="2" class="capteur">
             <img class="img_capteur" src="Thermometer_1_24282.png"> 
             <div class="nom_capteur">Salon</div>
        </li>
        '''
        
        page = ""
        for capteur in self.captFactory.capteurs:
            # Nom du capteur
            page +=  """<li id=\"""" + str(capteur.id) +  """\" class="capteur">"""
            
            # Image du capteur
            if capteur.type == 'T':
                page += """<img class="img_capteur" src="Thermometer_1_24282.png"> """
            elif capteur.type == 'P':
                page += """<img class="img_capteur" src="bulb.png">"""
                
            # Valeur Nom du capteur
            page += """<div class="nom_capteur">""" + str(capteur.nom) + """</div>"""              
            
            
            # Fermeture de la balise li
            page += """</li>"""
            

        return page
    
    
    def renderListeActionneursExistants (self):
        '''
        Modification de la page corps_admin pour ajouter les actionneurs
        <li id="2" class="capteur">
             <img class="img_capteur" src="C315b.png"> 
             <div class="nom_capteur">Salon</div>
        </li>
        '''
        
        page = ""
        for actionneur in self.actionFactory.actionneurs:
            # Nom de l'actionneur
            page +=  """<li id=\"""" + str(actionneur.id) +  """\" class="capteur">"""
            
            # Image de l'actionneur
            page += """<img class="img_capteur" src="C315b.png"> """
                
            # Valeur Nom de l'actionneur
            page += """<div class="nom_capteur">""" + str(actionneur.nom) + """</div>"""              
            
            # Fermeture de la balise li
            page += """</li>"""
            

        return page
