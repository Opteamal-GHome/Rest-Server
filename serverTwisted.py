import sys
from twisted.internet import reactor
from twisted.web import server, resource
from twisted.web.static import File
from twisted.python import log
from datetime import datetime

from capteurs import CapteursHTML, CapteursFactory
from admin import AdminHTML
from statistique import StatistiqueHTML
from socketGHome import *

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
    capteursFactory = CapteursFactory()
    
    # Initialisation de l'envoi des pages HTML
    root.putChild('', CapteursHTML(capteursFactory))
    root.putChild('capteurs', CapteursHTML(capteursFactory))
    root.putChild('stat', StatistiqueHTML())
    root.putChild('admin', AdminHTML())

    # Demarrage du socket GHome
    
    
    log.startLogging(sys.stdout)
    log.msg('Starting server: %s' %str(datetime.now()))
    server = server.Site(root)
    reactor.listenTCP(8080, server) #@UndefinedVariable
    reactor.run() #@UndefinedVariable

