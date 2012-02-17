import constantes, json

from twisted.internet.protocol import Protocol, Factory

from form import WebSocketForm

class SocketDataGHome(Protocol) :
    '''
    Client Socket to connect to server GHome developped with C language.
    '''
                
    def dataReceived(self, data):
        print 'Data Socket Data : ' + str(data)
        self.factory.decode(data)

        


class SocketDataGHomeFactory(Factory):
    
    protocol = SocketDataGHome

    def __init__(self, factoryCapteurs, factoryActionneurs, form):
        self.port = constantes.portServerData
        self.capteursFactory = factoryCapteurs
        self.actionneursFactory = factoryActionneurs
        self.ws = form
        print 'Initialisation du socket Data GHome'
        
        
    def decode(self, msg):
        data = json.loads(msg)
        if data["msgType"] == "device_updated":
            # Device modifie : On le change au niveau du serveur et on envoie la MAJ au websocket
            if (self.capteursFactory.modifierCapteur(data["id"], data["data"]) == False):
                # Si aucun capteur n'a ete modifie, le device est un actionneur
                self.actionneursFactory.modifierActionneur(data["id"], data["data"])
                
            self.ws.changedDevice(data["id"], data["data"])