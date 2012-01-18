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
        
        # Transport
        self.transport = transport
        
        
    def decodeJSONRule(self, msg) :
        # Extraction du nom du message
        self.name = msg["nomRule"]
    
        # Extraction des conditions      
        for conditionMsg in msg.condition:
            typeRightOp = conditionMsg["typeRightOp"]      
            leftOp = conditionMsg["leftOp"]
            rightOp = conditionMsg["rightOp"]
            operator = conditionMsg["operator"]
          
            condition = Condition(leftOp, operator, typeRightOp, rightOp)
            self.conditions.append(condition)
            
        # Extraction des actions
        for actionMsg in msg.action:
            levier = actionMsg["levier"]
            valeur = actionMsg["valeur"]
            
            action = Action(levier,valeur)
            self.actions.append(action)
        
    def createJsonRule(self) :
        '''
        Cree une chaine de caractere correspondant a une regle au format JSON (envoi au serveur GHome)
        '''
        # Creation de la structure de depart du message JSON
        data["msgType"] = "newRule"
        
        data["rule"]["ruleName"] = self.name
        
        # Ajout des conditions
        for condition in self.conditions:
            data["rule"]["condition"].append(condition)
            
        # Ajout des actions
        for action in self.actions:
            data["rule"]["actions"].append(action)
            
        # Transformation au format JSON et retour
        return json.dumps(data)
        
        
     def sendRule(self, ruleJson) :
        '''
        Envoi d'une regle sur le socket GHome
        '''
        self.transport.sendRule(ruleJson)
            
        
    
class Rules() :
    ''' 
    Ensemble de rule
    '''
    
    def __init__():
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

    def __init__(levier="",valeur=""):
        # Levier
        self.levier = levier
        # Valeur du levier
        self.valeur = valeur

    
class Condition():
    '''
    Classe Condition. La condition entraine l'action dans le moteur de regle du serveur C
    '''

    def __init__(leftOp="", operator="", typeRightOp="", rightOp=""):
        # Operande de gauche
        self.leftOp = leftOp
        # Operateur
        self.operator = operator
        # Operande de droite
        self.rightOp = rightOp
        # Type de l'operande de droite
        self.type = typeRightOp
