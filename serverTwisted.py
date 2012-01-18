import sys
from twisted.internet import reactor
from twisted.web import server, resource
from twisted.web.static import File
from twisted.python import log
from datetime import datetime

from capteurs import CapteursHTML
from admin import AdminHTML
from statistique import StatistiqueHTML

# Main Serveur
class Root(resource.Resource):

    def render_GET(self, request):
        '''
        get response method for the root resource
        localhost:5000/
        '''
        return 'Welcome to the REST API'

    def getChild(self, name, request):
        '''
        We overrite the get child function so that we can handle invalid
        requests
        '''
        if name == '':
            return self
        else:
            if name in VIEWS.keys():
                return resource.Resource.getChild(self, name, request)
            else:
                return PageNotFoundError()
              

class PageNotFoundError(resource.Resource):

    def render_GET(self, request):
        return 'Page Not Found!'


# List of views the server can distribute
VIEWS = {
    'capteurs': CapteursHTML(),
    'stat': StatistiqueHTML(),
    'admin': AdminHTML()
}

if __name__ == '__main__':
    root = File("/home/tommi/INSA/4IF/GHome/ClientPC/") # root of the webserver
    for viewName, className in VIEWS.items():
        #add the view to the web service
        root.putChild(viewName, className)
    log.startLogging(sys.stdout)
    log.msg('Starting server: %s' %str(datetime.now()))
    server = server.Site(root)
    reactor.listenTCP(5000, server) #@UndefinedVariable
    reactor.run() #@UndefinedVariable

