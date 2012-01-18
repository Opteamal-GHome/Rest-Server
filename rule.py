from xml.dom.minidom import Document
import json

class Rule():


    def __init__(self, transport):
        '''
        Initialisation des Rules 
        '''
        # Tableau des conditions et Tableau des actions
        self.conditions=[]
        self.actions = []
        self.name=""
        self.priority=""
        
        # Transport
        self.transport = transport
        
        
    def decodeJSONRule(self, msg):
        print('decode')
    
        # Extraction du nom du message
        self.name = msg['ruleName']
    
        # Extraction des conditions      
        for conditionMsg in msg['condition']:
            # Si la condition est une date
            if conditionMsg.getType()[4:8] == "date":
                condition = ConditionDate(conditionMsg.getType()[0:3], conditionMsg.getDate())
            
            else :
                leftOp = conditionMsg.getLeftOp()
                rightOp = conditionMsg.getRightOp()
                typeC = conditionMsg.getType()
          
                condition = Condition(leftOp, typeC, rightOp)
                
            self.conditions.append(condition)
            
        # Extraction des actions
        for actionMsg in msg['actions']:
            levier = actionMsg.getLevier()
            valeur = actionMsg.getValue()
            
            action = Action(levier,valeur)
            self.actions.append(action)
        
    def createJsonRule(self):
        '''
        Cree une chaine de caractere correspondant a une regle au format JSON (envoi au serveur GHome)
        '''
        # Creation de la structure de depart du message JSON
        data = {}
        data["msgType"] = "newRule"
        
        data['rule'] = {}
        data["rule"]["ruleName"] = self.name
        
        # Ajout des conditions
        data['rule']['conditions'] = []
        for condition in self.conditions:
            data["rule"]["conditions"].append(condition)
            
        # Ajout des actions
        data['rule']['actions'] = []
        for action in self.actions:
            data["rule"]["actions"].append(action)
            
        #print(data['rule']['conditions'][0].encodeJSON())
            
        # Transformation au format JSON et retour
        #return json.dumps(data)
        
        
    def sendRule(self, ruleJson):
        '''
        Envoi d'une regle sur le socket GHome
        '''
        self.transport.sendRule(ruleJson)
            
        
    
class Rules() :
    ''' 
    Ensemble de rule
    '''
    
    def __init__(self):
        '''
        Initialisation du tableau de Rule 
        '''
        self.rules=[]
        
    def ajouterRule (self, rule):
        self.rules.append(rule);
        


class Action():
    '''
    Classe Action. Une action survient lorsque des conditions sont respectees. Fait parti d'une Rule.
    '''

    def __init__(self, levier="",valeur=""):
        # Levier
        self.actuator = levier
        # Valeur du levier
        self.value = valeur
        
    def getLevier(self):
        return self.actuator
        
    def getValue(self):
        return self.value

    
class Condition():
    '''
    Classe Condition. La condition entraine l'action dans le moteur de regle du serveur C
    '''

    def __init__(self, leftOp="", typeC="", rightOp=""):
        # Operande de gauche
        self.leftOp = leftOp
        # Type de la condition : operateur
        self.type = typeC
        # Operande de droite
        self.rightOp = rightOp
        
    def getType(self):
        return self.type
        
    def getLeftOp(self):
        return self.leftOp
        
    def getRightOp(self):
        return self.rightOp
        
    def encodeJSON (self):
        return [ { 'type':self.type, 'leftOp':self.leftOp, 'rightOp':self.rightOp } ]
        
        
class ConditionDate(Condition):
    '''
    Classe Condition pour une date. Herite de la classe Condition
    '''
    
    def __init__(self, typeC="", date=""):
        # Type Condition
        self.type = typeC
        # Date de la condition
        self.date = date
        
    def getDate(self):
        return self.date
        
    def encodeJSON (self):
        return [ { 'type':self.type, 'date':self.date } ]

