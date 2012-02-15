import SocketServer
import constantes, json

from form import WebSocketForm

class TCPServer(SocketServer.BaseRequestHandler) :
    '''
    Client Socket to connect to server GHome developped with C language.
    '''
    
    def __init__(self, factoryCapteurs, factoryActionneurs, ws):
        self.capteursFactory = factoryCapteurs
        self.actionneursFactory = factoryActionneurs
        self.ws = ws
        
    
    def setup(self):
        print self.client_address, 'connected!'
        
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024)
        print "{} wrote:".format(self.client_address[0])
        print self.data

    def finish(self):
        print self.client_address, 'disconnected!'
        
    def decode(self, msg):
        data = json.loads(msg)
        if data["msgType"] == "device_updated":
            # Device modifie : On le change au niveau du serveur et on envoie la MAJ au websocket
            if (self.capteursFactory.modifierCapteur(data["id"], data["data"]) == False):
                # Si aucun capteur n'a ete modifie, le device est un actionneur
                self.actionneursFactory.modifierActionneur(data["id"], data["data"])
                
            self.ws.changedDevice(data["id"], data["data"])


class SocketDataGHome:

    def __init__(self, factoryCapteurs, factoryActionneurs, form):
        self.port = constantes.portServerData
        self.capteursFactory = factoryCapteurs
        self.actionneursFactory = factoryActionneurs
        self.ws = WebSocketForm
        
        
    def connect(self):
        server = SocketServer.ThreadingTCPServer(('', self.port), TCPServer(self.capteursFactory, self.actionneursFactory, self.ws))
        
        print 'Serveur TCP Data demarre sur le port ' + str(constantes.portServerData)
        
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever(1)
