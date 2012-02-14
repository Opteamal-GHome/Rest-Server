import socket
import struct
import constantes

class SocketGHome :
    '''
    Client Socket to connect to server GHome developped with C language.
    '''
    
    def __init__(self) :
        self.hote = constantes.ipServeurGHome
        self.port = constantes.portServeurGHome
        self.connectServer()
        print("Connexion etablie avec le serveur sur le port {}".format(self.port))
        
    def connectServer(self):
        '''
        Connexion au serveur cible par socket
        '''
        self.connexionServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexionServer.connect((self.hote, self.port))
    
    def sendMsg (self, message):    
        '''
        Methode d'envoi d'un message
        Se connecte au serveur cible puis envoie le message
        '''    
        try:
            self.connectServer()
        except Exception:
            print 'Connection NOK'
            
        # On envoie la taille du message en octets dans un premier temps
        print str(len(message))
        self.connexionServer.send(struct.pack('!i',len(message)))
        
        # On envoie le message ensuite    
        print message
        message = message.encode()
        self.connexionServer.send(message)
                        
        
    def receiveMsg (self):
        '''
        Methode de reception d'un message
        '''
        msg_recu = self.connexionServer.recv(1024)
        return msg_recu 
    
    def closeServer (self):
        '''
        Ferme la connexion au serveur
        '''
        print("Fermeture de la connexion")
        self.connexionServer.close()
