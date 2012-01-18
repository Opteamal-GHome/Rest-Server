import socket
import sys

class SocketGHome :
    '''
    Client Socket to connect to server GHome developped with C language.
    '''
    
    def __init__(self) :
        self.hote = "localhost"
        self.port = 12800
        self.connexionServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexionServer.connect((self.hote, self.port))
        print("Connexion etablie avec le serveur sur le port {}".format(self.port))
    
    def sendMsg (self, message):
        # On envoie la taille du message en octets dans un premier temps
        tailleMessage = sys.getsizeof(message)
        self.connexionServer.send(tailleMessage)
        
        # On envoie le message ensuite    
        message = message.encode()
        self.connexionServer.send(message)
        
    def receiveMsg (self):
        msg_recu = self.connexionServer.recv(1024)
        return msg_recu.decode() 
    
    def closeServer (self):
        print("Fermeture de la connexion")
        self.connexionServer.close()
