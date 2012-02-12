from twisted.web import resource, http, server
import netifaces as ni
import constantes


class DisplayRules(resource.Resource):
    '''
    Affichage des regles
    '''

    def __init__(self,capteursFactory, actionneursFactory, ensRules, transport):
        resource.Resource.__init__(self)
        self.capteursFactory = capteursFactory
        self.actionneursFactory = actionneursFactory
        self.ensembleRules = ensRules
        self.transport = transport
        
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
                if str(capteur.type) == "T":
                    reponse += """<img class="img_capteur" src="images/Thermometer_1_24282.png"> """
                elif str(capteur.type) == "P":
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
    
    
                # Operateur de droite                
                if (str(condition.rightOp[0]) == "@"):
                    # Si presence d'un @, alors c'est un capteur
                    
                    capteurDroite = self.capteursFactory.getCapteur(condition.rightOp[1:])
                    if str(capteurDroite.type) == "T":
                        reponse += """<img class="img_capteur" src="images/Thermometer_1_24282.png"> """
                    elif str(capteurDroite.type) == "P":
                        reponse += """<img class="img_capteur" src="images/bulb.png">"""
                        
                    reponse += """<div class="nom_capteur">""" + str(capteurDroite.nom) + """</div>"""
                
                else:
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
    
        self.transport.getAllDevices(self.capteursFactory, self.actionneursFactory)
    
        headerFile = open("../ClientPC/header.html")
        headerHtml = headerFile.read()
        headerHtml = headerHtml.replace("$STYLE$", "core_admin.css")
        headerHtml = headerHtml.replace("$JS_TO_INCLUDE$", "client_admin_regle_script.js")
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
        
           
       
class GroupsHtml(resource.Resource):
    '''
    Affichage des groupes
    ''' 
    def __init__(self,capteursFactory, actionneursFactory, ensRules, transport, ensGroups):
        self.captFactory = capteursFactory
        self.actionFactory = actionneursFactory 
        self.ensembleRules = ensRules
        self.transport = transport
        self.ensGroups = ensGroups
        resource.Resource.__init__(self)
        

    def render_GET(self, request):
        '''
        Creation de la page des groupes
        '''
        
        self.transport.getAllDevices(self.captFactory, self.actionFactory)
        
        # On reutilise des methodes qui affiche des box de la page de creation des regles
        createRule = CreateRule(self.captFactory, self.actionFactory, self.ensembleRules, self.transport)
        
        headerFile = open("../ClientPC/header.html")
        headerHtml = headerFile.read()
        headerHtml = headerHtml.replace("$STYLE$", "core_groups.css")
        headerHtml = headerHtml.replace("$JS_TO_INCLUDE$", "client_admin_groups_script.js")
        headerHtml = headerHtml.replace("$IPSERVEUR$", str(ni.ifaddresses(constantes.typeLiaison)[2][0]['addr'])+":" + str(constantes.portServeurWeb))
        headerFile.close()      
        
        groupFile = open("/home/tommi/INSA/4IF/GHome/ClientPC/core_groups.html")
        groupHtml = groupFile.read()
        groupHtml = groupHtml.replace("$LISTECAPTEURS$", createRule.renderListeCapteursExistants())
        groupHtml = groupHtml.replace("$LISTEACTIONNEURS$", createRule.renderListeActionneursExistants())
        groupHtml = groupHtml.replace("$LISTEGROUPES$", self.renderListeGroupe())
        groupFile.close()

        footerFile = open("../ClientPC/footer.html")
        footerHtml = footerFile.read()
        footerFile.close()
   
        return (headerHtml + groupHtml + footerHtml)
        
        
    def render_POST(self, request):
        return self.render_GET(request)
    
    def renderListeGroupe(self):
        '''
        Renvoie la liste des groupes
        '''
        page = ""
        
        print str(len(self.ensGroups.listeGroupe))
        # On vient ajouter chaque groupe
        for groupe in self.ensGroups.listeGroupe:
            page += """<li class="group"><img class="btn_del_grp" src="images/moblin-close2.png" /><img src="images/ring-icon.png" />"""
            
            # Ajout du nom du groupe
            page += str(groupe.nom)
            
            # Fermeture de la balise
            page += """</li>"""
        
        print page
        return page


class CreateRule(resource.Resource):
    '''
    Creation d'une regle
    '''

    def __init__(self,capteursFactory, actionneursFactory, ensRules, transport):
        self.captFactory = capteursFactory
        self.actionFactory = actionneursFactory 
        self.ensembleRules = ensRules
        self.transport = transport
        resource.Resource.__init__(self)
        

    def render_GET(self, request):
        '''
        Creation de la page admin - RuleCreation 
        /admin
        '''
        self.transport.getAllDevices(self.captFactory, self.actionFactory)
        
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
        <li id="2" class="periph">
             <img class="img_periph" src="images/Thermometer_1_24282.png"> 
             <div class="nom_periph">Salon</div>
        </li>
        '''
        
        page = ""
        for capteur in self.captFactory.capteurs:
            # Nom du capteur
            page +=  """<li id=\"""" + str(capteur.id) +  """\"  alt=\"""" + str(capteur.type) + """\"  class="periph">"""
            
            # Image du capteur
            if capteur.type == 'T':
                page += """<img class="img_periph" src="images/Thermometer_1_24282.png"> """
            elif capteur.type == 'L':
                page += """<img class="img_periph" src="images/bulb.png">"""
            elif capteur.type == 'U':
                page += """<img class="img_periph" src="images/meteo_variable.png">"""
            elif capteur.type == 'H':
                page += """<img class="img_periph" src="images/Rain.png">"""
            elif capteur.type == 'C':
                page += """<img class="img_periph" src="images/touch_up.png">"""
            elif capteur.type == 'I':
                page += """<img class="img_periph" src="images/1.png">"""
            else:
                page += """<img class="img_periph" alt=\"""" + capteur.type + """" src="images/inexistant.png">"""
                
            # Valeur Nom du capteur
            page += """<div class="nom_periph">""" + str(capteur.nom) + """</div>"""              
            
            
            # Fermeture de la balise li
            page += """</li>"""
            

        return page
    
    
    def renderListeActionneursExistants (self):
        '''
        Modification de la page corps_admin pour ajouter les actionneurs
        <li id="2" class="capteur">
             <img class="img_capteur" src="images/C315b.png"> 
             <div class="nom_periph">Salon</div>
        </li>
        '''
        
        page = ""
        for actionneur in self.actionFactory.actionneurs:
            # Nom de l'actionneur
            page +=  """<li id=\"""" + str(actionneur.id) +  """\"  alt=\"""" + str(actionneur.type) + """\"  class="periph">"""
            
            # Image de l'actionneur
            page += """<img class="img_periph" src="images/C315b.png"> """
                
            # Valeur Nom de l'actionneur
            page += """<div class="nom_periph">""" + str(actionneur.nom) + """</div>"""              
            
            # Fermeture de la balise li
            page += """</li>"""
            

        return page
    
        
