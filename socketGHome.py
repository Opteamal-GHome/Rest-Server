import socket

class SocketGHome :
    '''
    Client Socket to connect to server GHome developped with C language.
    '''
    
    def __init__(self) :
        self.hote = "localhost"
        self.port = 12800
        self.connexionServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexionServer.connect((self.hote, self.port))
        print("Connexion établie avec le serveur sur le port {}".format(self.port))
    
    def sendMsg (self, message):
        message = message.encode()
        self.connexionServer.send(message)
        
    def receiveMsg (self):
        msg_recu = self.connexionServer.recv(1024)
        return msg_recu.decode() 
    
    def closeServer (self):
        print("Fermeture de la connexion")
        self.connexionServer.close()
