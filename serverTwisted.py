import sys
from twisted.internet import reactor
from twisted.web import server, resource
from twisted.web.static import File
from twisted.python import log
from datetime import datetime

from rule import Rules
from actionneurs import ActionneursFactory

from capteurs import CapteursHTML, CapteursFactory
from admin import AdminHTML
from statistique import StatistiqueHTML
from form import Form

# Main Serveur
class Root(resource.Resource):

    def render_GET(self, request):
        '''
        get response method for the root resource
        '''
        return 'Welcome to the REST API'
             

class PageNotFoundError(resource.Resource):

    def render_GET(self, request):
        return 'Page Not Found!'



if __name__ == '__main__':
    root = File("/home/tommi/INSA/4IF/GHome/ClientPC/") 
    
    # Objets requis par le serveur
    capteursFactory = CapteursFactory()
    actionneursFactory = ActionneursFactory()
    ensembleRules = Rules()
    
    # Initialisation de l'envoi des pages HTML
    root.putChild('', CapteursHTML(capteursFactory))
    root.putChild('capteurs', CapteursHTML(capteursFactory))
    root.putChild('stat', StatistiqueHTML())
    root.putChild('admin', AdminHTML(capteursFactory, actionneursFactory))
    root.putChild('form', Form(ensembleRules))
    
    log.startLogging(sys.stdout)
    log.msg('Starting server: %s' %str(datetime.now()))
    server = server.Site(root)
    reactor.listenTCP(8080, server) #@UndefinedVariable
    reactor.run() #@UndefinedVariable

