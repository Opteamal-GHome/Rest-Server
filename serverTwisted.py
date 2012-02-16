import sys
from twisted.internet import reactor
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS

from twisted.web import server, resource
from twisted.web.static import File
from twisted.python import log
from datetime import datetime
from rule import Rules
from actionneurs import ActionneursFactory
from capteurs import CapteursHTML, CapteursFactory
from admin import *
from statistique import StatistiqueHTML
from socketDonneeGHome import *
from form import *
from transport import TransportGHome
import constantes

import threading, time


if __name__ == '__main__':
    root = File("/home/tommi/INSA/4IF/GHome/ClientPC/") 
    server = server.Site(root)
        
    # Objets requis par le serveur
    capteursFactory = CapteursFactory()
    actionneursFactory = ActionneursFactory()
    #ensembleRules = Rules()
    
    # Serveur WebSockets
    #wsForm = WebSocketForm(ensembleRules)
    
    factory = WebSocketFactory("ws://localhost:9000")
    listenWS(factory)
    
    ensembleRules = factory.getEnsRules()
        
    # Thread sur le socket data
    socketData = SocketDataGHome(capteursFactory, actionneursFactory, factory)
    a = threading.Thread(None, socketData.connect, "Server Data", (), None)
    a.start()
    
    time.sleep(1)
    
    #transport = TransportGHome()
    transport = 2
    
    # Initialisation de l'envoi des pages HTML
    root.putChild('', CapteursHTML(capteursFactory, actionneursFactory, transport))
    root.putChild('capteurs', CapteursHTML(capteursFactory, actionneursFactory, transport))
    root.putChild('stat', StatistiqueHTML())
    root.putChild('temperature', StatistiqueHTML())
    root.putChild('create_rule', CreateRule(capteursFactory, actionneursFactory, ensembleRules))
    root.putChild('rules', DisplayRules(capteursFactory, actionneursFactory, ensembleRules))
    root.putChild('groups', Groups(capteursFactory, actionneursFactory, ensembleRules))
    
    log.startLogging(sys.stdout)
    log.msg('Starting server: %s' %str(datetime.now()))

    
    # Serveur Web
    reactor.listenTCP(constantes.portServeurWeb, server) #@UndefinedVariable
    reactor.run() #@UndefinedVariable
