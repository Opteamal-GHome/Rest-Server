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
from socketDonneeGHome import *
from form import *
from transport import TransportGHome
import constantes
from websocket import *

import threading, time


if __name__ == '__main__':
    root = File("/home/tommi/INSA/4IF/GHome/ClientPC/") 
        
    # Objets requis par le serveur
    capteursFactory = CapteursFactory()
    actionneursFactory = ActionneursFactory()
    ensembleRules = Rules()
    
    factory = WebSocketInit(root) # handles websocket requests
    factory.addHandler('/form', WebSocketForm)
        
    # Thread sur le socket data
    socketData = SocketDataGHome()
    a = threading.Thread(None, socketData.connect, "Server Data", (), None)
    a.start()
    
    print "aie"
    
    time.sleep(3)
    
    transport = TransportGHome()
    #transport = 2
    
    # Initialisation de l'envoi des pages HTML
    root.putChild('', CapteursHTML(capteursFactory, actionneursFactory, transport))
    root.putChild('capteurs', CapteursHTML(capteursFactory, actionneursFactory, transport))
    root.putChild('stat', StatistiqueHTML())
    root.putChild('temperature', StatistiqueHTML())
    root.putChild('admin', AdminHTML(capteursFactory, actionneursFactory))
    root.putChild('create_rule', AdminHTML(capteursFactory, actionneursFactory))
    
    log.startLogging(sys.stdout)
    log.msg('Starting server: %s' %str(datetime.now()))

    
    # Serveur Web
    reactor.listenTCP(constantes.portServeurWeb, factory) #@UndefinedVariable
    reactor.run() #@UndefinedVariable
