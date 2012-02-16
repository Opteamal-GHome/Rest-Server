from twisted.web import resource, http, server
import netifaces as ni
import constantes


class DisplayRules(resource.Resource):
    '''
    Affichage des regles
    '''

    def __init__(self,capteursFactory, actionneursFactory, ensRules):
        resource.Resource.__init__(self)
        self.capteursFactory = capteursFactory
        self.actionneursFactory = actionneursFactory
        self.ensembleRules = ensRules
        
    def corpsDisplayRules(self):
        '''
        Methode de reponse a localhost:5000/admin/rules
        Cree un objet de type PageIndex et renvoie la page principale
        ''' 
        reponse = ""
        
        reponse += """<ul id="liste_regles">"""

        # On tourne sur les regles existantes
        for rule in self.ensembleRules.rules:
            reponse += """<li class="regle_desc">
			    <div class="top_regle">""" + str(rule.name)
                    
            reponse += """<img class="btn_close_regle" src="images/moblin-close2.png">"""

            reponse += """</div>
			
			    <div class="corps_regle">
				    <ul class="liste_conditions">"""
   
            # On tourne sur les conditions d'une regle
            for condition in rule.conditions:
                reponse += """
					    <li class="ligne_regle">
						    <div class="capteur">"""

                # On envoie la bonne image par rapport au type de l'operateur de gauche
                capteur = self.capteursFactory.getCapteur(condition.leftOp)
                print capteur.type
                if capteur.type == 'T':
                    reponse += """<img class="img_capteur" src="images/Thermometer_1_24282.png"> """
                elif capteur.type == 'P':
                    reponse += """<img class="img_capteur" src="images/bulb.png">"""

                # Operateur de gauche
                reponse += """<div class="nom_capteur">""" + str(capteur.nom) + """</div>
						    </div>"""
    
                # Operateur du milieu
                if condition.type == 'inf':
                    reponse += """<div class="operateur" title=\"""" + str(condition.type) + """\"><</div>"""
                elif condition.type == 'equ':
                    reponse += """<div class="operateur" title=\"""" + str(condition.type) + """\">=</div>"""
                elif condition.type == 'sup':
                    reponse += """<div class="operateur" title=\"""" + str(condition.type) + """\">></div>"""
    
    
                # Operateur de droite : TODO Voir pour les capteurs a droite
                reponse += """<div class="value_condition">""" + str(condition.rightOp) + """</div>"""
  
                reponse += """</li>"""

            # Fin des conditions
            reponse += """</ul>"""	

            # Affichage de la fleche
            reponse += """ <img class="fleche_implique" src="images/arrow black2.gif">"""

            # Affichage des actions
            reponse += """<div class="pres_action">"""
            action = self.actionneursFactory.getActionneur(rule.actions[0].actuator)
            #for action in self.actionneursFactory.actionneurs:
            reponse += """<div class="capteur">
					    <img class="img_capteur" src="images/C315b.png"> 
					    <div class="nom_capteur">""" + str(action.nom) + """</div>
				        </div>"""

            # Fin de la pres_action
            reponse += """</div>"""
            
            # Fin du bloc regle
            reponse += """<div style="clear:both"></div>
                </div>"""
            
            # Fin de la ligne regle
            reponse += """</li>"""
            
            
   
        # Fin de la liste des regles
        reponse += """</ul>"""
        
        
        return reponse
        
    def render_GET(self, request):
        headerFile = open("../ClientPC/header.html")
        headerHtml = headerFile.read()
        headerHtml = headerHtml.replace("$STYLE$", "core_admin.css")
        headerHtml = headerHtml.replace("$JS_TO_INCLUDE$", "client_admin_script.js")
        headerHtml = headerHtml.replace("$IPSERVEUR$", str(ni.ifaddresses(constantes.typeLiaison)[2][0]['addr'])+":" + str(constantes.portServeurWeb))
        headerFile.close()      
        
        corpsHtml = self.corpsDisplayRules()

        footerFile = open("../ClientPC/footer.html")
        footerHtml = footerFile.read()
        footerFile.close()

        return (headerHtml + corpsHtml + footerHtml)
        
            
    def getChild(self, path, request):
        return ""
        
        
    def render_POST(self, request):
        return self.render_GET(request)
        
           
       
class Groups(resource.Resource):
    '''
    Affichage des groupes
    ''' 
    def __init__(self,capteursFactory, actionneursFactory, ensRules):
        self.captFactory = capteursFactory
        self.actionFactory = actionneursFactory 
        self.ensembleRules = ensRules
        resource.Resource.__init__(self)
        

    def render_GET(self, request):
        '''
        Methode de reponse a localhost:5000/admin/rules
        Cree un objet de type PageIndex et renvoie la page principale
        '''       
        return ""
        
        
    def render_POST(self, request):
        return self.render_GET(request)
    


class CreateRule(resource.Resource):
    '''
    Creation d'une regle
    '''

    def __init__(self,capteursFactory, actionneursFactory, ensRules):
        self.captFactory = capteursFactory
        self.actionFactory = actionneursFactory 
        self.ensembleRules = ensRules
        resource.Resource.__init__(self)
        

    def render_GET(self, request):
        '''
        Creation de la page admin - RuleCreation 
        /admin
        '''
        headerFile = open("../ClientPC/header.html")
        headerHtml = headerFile.read()
        headerHtml = headerHtml.replace("$STYLE$", "core_admin.css")
        headerHtml = headerHtml.replace("$JS_TO_INCLUDE$", "client_admin_script.js")
        headerHtml = headerHtml.replace("$IPSERVEUR$", str(ni.ifaddresses(constantes.typeLiaison)[2][0]['addr'])+":" + str(constantes.portServeurWeb))
        headerFile.close()      
        
        adminFile = open("/home/tommi/INSA/4IF/GHome/ClientPC/core_admin.html")
        adminHtml = adminFile.read()
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
             <img class="img_capteur" src="images/Thermometer_1_24282.png"> 
             <div class="nom_capteur">Salon</div>
        </li>
        '''
        
        page = ""
        for capteur in self.captFactory.capteurs:
            # Nom du capteur
            page +=  """<li id=\"""" + str(capteur.id) +  """\" class="capteur">"""
            
            # Image du capteur
            if capteur.type == 'T':
                page += """<img class="img_capteur" src="images/Thermometer_1_24282.png"> """
            elif capteur.type == 'P':
                page += """<img class="img_capteur" src="images/bulb.png">"""
                
            # Valeur Nom du capteur
            page += """<div class="nom_capteur">""" + str(capteur.nom) + """</div>"""              
            
            
            # Fermeture de la balise li
            page += """</li>"""
            

        return page
    
    
    def renderListeActionneursExistants (self):
        '''
        Modification de la page corps_admin pour ajouter les actionneurs
        <li id="2" class="capteur">
             <img class="img_capteur" src="images/C315b.png"> 
             <div class="nom_capteur">Salon</div>
        </li>
        '''
        
        page = ""
        for actionneur in self.actionFactory.actionneurs:
            # Nom de l'actionneur
            page +=  """<li id=\"""" + str(actionneur.id) +  """\" class="capteur">"""
            
            # Image de l'actionneur
            page += """<img class="img_capteur" src="images/C315b.png"> """
                
            # Valeur Nom de l'actionneur
            page += """<div class="nom_capteur">""" + str(actionneur.nom) + """</div>"""              
            
            # Fermeture de la balise li
            page += """</li>"""
            

        return page
    
        
