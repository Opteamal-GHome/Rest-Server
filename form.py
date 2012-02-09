from twisted.web import resource
from rule import Rule

class Form (resource.Resource):
    
    def __init__(self,ensRules, transport):
        resource.Resource.__init__(self)
        self.ensembleRules = ensRules
        self.transport = transport

    
    def render_GET(self, request):
        '''
        Methode de reponse pour localhost:8000/form
        '''
        
        print "recu requete"
        
        # On recupere le json de la requete POST
        #datapost = request.content.getvalue()
        #data = json.loads(datapost)
        
        # On envoie le tableau a une methode de decodage
        #self.decode(data)
                
        return "";
    
    def render_POST(self, request):
        return self.render_GET(request)
        
    def getChild(self, path, request):
        return "Halleluia"
    
    def decode(self, data):
        '''
        Decode le tableau recu
        '''
        
        if (data["type"] == "newRule"):
            # Nouvelle regle donnee par le client ; A envoyer au serveur GHome
            rule = Rule(data["rule"])     
            rule.priority = "1"
            rule.name = "Nouvelle"
            self.ensembleRules.ajouterRule(rule)
            jsonMsg = rule.createJsonRule()
            
            jsonMsg = jsonMsg.replace('"type": u', '"type": ');
            jsonMsg = jsonMsg.replace('"rightOp": u', '"rightOp": ');
            jsonMsg = jsonMsg.replace('"leftOp": u', '"leftOp": ');
            jsonMsg = jsonMsg.replace('"actuator": u', '"actuator": ');
            jsonMsg = jsonMsg.replace('"value": u', '"value": ');
            
            print jsonMsg
            
            # Envoi de la regle
            self.transport.sendRule(jsonMsg)
            
            # Reception de la reponse
            print self.transport.receiveAnswer()
            
        elif (data["type"] == "supprRule"):
            # Suppression d'une regle
            nomRule = data["ruleName"]
            self.ensembleRules.supprimerRule(nomRule)
            
