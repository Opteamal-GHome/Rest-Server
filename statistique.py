from twisted.web import resource

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
        headerHtml = headerHtml.replace("$STYLE$", "core_capteurs.css")
        headerHtml = headerHtml.replace("$JS_TO_INCLUDE$", "client_stats_script.js")
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
    
    
    
    
class Statistique():
    '''
    Classe Statistique
    '''
