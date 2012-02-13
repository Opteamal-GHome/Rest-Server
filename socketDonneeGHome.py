import SocketServer
import constantes

class TCPServer(SocketServer.BaseRequestHandler) :
    '''
    Client Socket to connect to server GHome developped with C language.
    '''
    
    def setup(self):
        print self.client_address, 'connected!'
        
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024)
        print "{} wrote:".format(self.client_address[0])
        print self.data

    def finish(self):
        print self.client_address, 'disconnected!'


class SocketDataGHome:

    def __init__(self):
        self.port = constantes.portServerData
        
        
    def connect(self):
        server = SocketServer.ThreadingTCPServer(('', self.port), TCPServer)
        
        print 'Serveur TCP Data demarre sur le port ' + str(constantes.portServerData)
        
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever(1)
        #server.server_activate()