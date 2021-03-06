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
from group import GroupFactory
from statistique import *
from socketDonneeGHome import *
from form import *
from transport import TransportGHome
from save_fichier import *
import constantes

import time


if __name__ == '__main__':
    root = File(constantes.cheminLocal) 
    server = server.Site(root)
        
    # Objets requis par le serveur
    capteursFactory = CapteursFactory()
    actionneursFactory = ActionneursFactory()
    ensembleRules = Rules()
    ensembleGroupes = GroupFactory()
    
    # Sauvegarde des regles
    saveFichier = SaveFichier(ensembleRules)
    saveFichier.recreateRules()
    
    # Serveur WebSockets
    factory = WebSocketFactory("ws://localhost:" + str(constantes.portWebSocket))
    listenWS(factory)
    
    factory.ensembleRules = ensembleRules
    factory.capteursFactory = capteursFactory
    factory.actionneursFactory = actionneursFactory
    factory.saveFichier = saveFichier
    factory.ensembleGroupes = ensembleGroupes
         
    transport = TransportGHome()
    #transport = 2
    
    # Socket data    
    reactor.listenTCP(constantes.portServerData, SocketDataGHomeFactory(capteursFactory, actionneursFactory, ensembleRules, transport, factory))

    # Acces a la socket GHome pour les websockets
    factory.socketG = transport
    
    # Suppression de toutes les regles du serveur C et reenvoi des regles
    #transport.reinitialisationRegles(ensembleRules, saveFichier)
    
    # Initialisation de l'envoi des pages HTML
    root.putChild('', CapteursHTML(capteursFactory, actionneursFactory, transport))
    root.putChild('capteurs', CapteursHTML(capteursFactory, actionneursFactory, transport))
    root.putChild('stat', StatistiqueHTML(capteursFactory, factory))
    root.putChild('temperature', StatistiqueTemperatureHTML(capteursFactory))
    root.putChild('create_rule', CreateRule(capteursFactory, actionneursFactory, ensembleRules, transport))
    root.putChild('rules', DisplayRules(capteursFactory, actionneursFactory, ensembleRules, transport))
    root.putChild('groups', GroupsHtml(capteursFactory, actionneursFactory, ensembleRules, transport, ensembleGroupes))
    
    log.startLogging(sys.stdout)
    log.msg('Starting server: %s' %str(datetime.now()))

    
    # Serveur Web
    reactor.listenTCP(constantes.portServeurWeb, server) #@UndefinedVariable
    reactor.run() #@UndefinedVariable
