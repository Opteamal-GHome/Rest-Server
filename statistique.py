from twisted.web import resource
import constantes
import netifaces as ni


class StatistiqueHTML(resource.Resource):
    
    def __init__(self, capteursFactory, webS):
        resource.Resource.__init__(self)
        self.capteursFactory = capteursFactory
        self.ws = webS
    
    def render_GET(self, request):
        '''
        Methode de reponse a /stat
        '''
        
        headerFile = open("../ClientPC/header.html")
        headerHtml = headerFile.read()
        headerHtml = headerHtml.replace("$STYLE$", "core_stats.css")
        headerHtml = headerHtml.replace("$JS_TO_INCLUDE$", "client_stats_script.js")
        headerHtml = headerHtml.replace("$IPSERVEUR$", str(ni.ifaddresses(constantes.typeLiaison)[2][0]['addr'])+":" + str(constantes.portServeurWeb))
        headerFile.close()      
        
        statFile = open("../ClientPC/core_stats.html")
        statHtml = statFile.read()
        statFile.close()

        footerFile = open("../ClientPC/footer.html")
        footerHtml = footerFile.read()
        footerFile.close()

        return (headerHtml + statHtml + footerHtml)
        

    def render_POST(self, request):
        return self.render_GET(request)
    
    
    
    
class StatistiqueTemperatureHTML(resource.Resource):
    '''
    Classe Statistique pour les temperatures
    '''
    
    def __init__(self, capteursFactory):
        resource.Resource.__init__(self)
        self.capteursFactory = capteursFactory
    
    def render_GET(self, request):
        '''
        Methode de reponse a /stat
        '''
        
        headerFile = open("../ClientPC/header.html")
        headerHtml = headerFile.read()
        headerHtml = headerHtml.replace("$STYLE$", "core_stats.css")
        headerHtml = headerHtml.replace("$JS_TO_INCLUDE$", "client_stats_script.js")
        headerHtml = headerHtml.replace("$IPSERVEUR$", str(ni.ifaddresses(constantes.typeLiaison)[2][0]['addr'])+":" + str(constantes.portServeurWeb))
        headerFile.close()      
        
        statFile = open("../ClientPC/core_stats.html")
        statHtml = statFile.read()
        statHtml = statHtml.replace("$LISTEPERIPH$", self.renderListePeriph())
        statFile.close()

        footerFile = open("../ClientPC/footer.html")
        footerHtml = footerFile.read()
        footerFile.close()

        return (headerHtml + statHtml + footerHtml)
        

    def render_POST(self, request):
        return self.render_GET(request)
    
    def renderListePeriph(self):
        '''
        Retourne la liste des peripheriques de type temperature
        '''
        page = ""
        
        for capt in self.capteursFactory.capteurs:
            if capt.type == "T":
                page += """<li><a href="#">""" + str(capt.nom) + """</a><div class="id_periph" style="display:none">""" + str(capt.id) + """</div></li>"""
                
        return page
