from twisted.web import resource
import simplejson as json
from rule import Rule
from transport import TransportGHome

class Form (resource.Resource):
    
    def __init__(self,ensRules):
        self.ensembleRules = ensRules
        #self.transport = TransportGHome()
    
    def render_GET(self, request):
        '''
        Methode de reponse pour localhost:8000/form
        '''
        # On recupere le json de la requete POST
        datapost = request.content.getvalue()
        data = json.loads(datapost)
        
        # On envoie le tableau a une methode de decodage
        self.decode(data)
                
        return "";
    
    def render_POST(self, request):
        return self.render_GET(request)
    
    def decode(self, data):
        '''
        Decode le tableau recu
        '''
        
        if (data["type"] == "newRule"):
            rule = Rule(data["rule"])     
            self.ensembleRules.ajouterRule(rule)
            jsonMsg = rule.createJsonRule()
            self.transport.sendRule(jsonMsg)
        elif (data["type"] == "supprRule"):
            nomRule = data["ruleName"]
            self.ensembleRules.supprimerRule(nomRule)