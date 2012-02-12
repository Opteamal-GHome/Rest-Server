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
from form import *
from transport import TransportGHome

from websocket import *

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
    
    factory = WebSocketInit(root) # handles websocket requests
    factory.addHandler('/form', WebSocketForm)
    
    #transport = TransportGHome()
    transport = 2
    
    # Initialisation de l'envoi des pages HTML
    root.putChild('', CapteursHTML(capteursFactory, actionneursFactory, transport))
    root.putChild('capteurs', CapteursHTML(capteursFactory, actionneursFactory, transport))
    root.putChild('stat', StatistiqueHTML())
    root.putChild('temperature', StatistiqueHTML())
    root.putChild('admin', AdminHTML(capteursFactory, actionneursFactory))
    root.putChild('create_rule', AdminHTML(capteursFactory, actionneursFactory))
    
    log.startLogging(sys.stdout)
    log.msg('Starting server: %s' %str(datetime.now()))
    
    
    
    reactor.listenTCP(8080, factory) #@UndefinedVariable
    reactor.run() #@UndefinedVariable
