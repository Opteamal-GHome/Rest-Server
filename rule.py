class Rule():


    def __init__(self, data):
        '''
        Initialisation des Rules 
        '''
        # Tableau des conditions et Tableau des actions
        self.conditions=[]
        self.actions = []
        self.name=""
        self.priority=""
        self.decodeJSONRule(data)
        
        
    def decodeJSONRule(self, msg):
        print('decode')
    
        # Extraction du nom du message
        self.name = msg['ruleName']
    
        # Extraction des conditions      
        for conditionMsg in msg['conditions']:
            # Si la condition est une date
            if conditionMsg.type[4:8] == "date":
                condition = ConditionDate(conditionMsg.type[0:3], conditionMsg.date)
            
            else :
                leftOp = conditionMsg.leftOp
                rightOp = conditionMsg.rightOp
                typeC = conditionMsg.type
          
                condition = Condition(leftOp, typeC, rightOp)
                
            self.conditions.append(condition)
            
        # Extraction des actions
        for actionMsg in msg['actions']:
            levier = actionMsg.actuator
            valeur = actionMsg.value
            
            action = Action(levier,valeur)
            self.actions.append(action)
                    
    def createJsonRule(self):
        '''
        Cree une chaine de caractere correspondant a une regle au format JSON (envoi au serveur GHome)
        '''
        # Creation de la structure de depart du message JSON
        data = {}
        data["msgType"] = "newRule"
        data["priority"] = self.priority
        
        data["rule"] = {}
        data["rule"]["ruleName"] = self.name
                
        # Ajout des conditions
        data["rule"]["conditions"] = []
        for condition in self.conditions:
            data["rule"]["conditions"].append(condition.encodeJSON())
            
        # Ajout des actions
        data["rule"]["actions"] = []
        for action in self.actions:
            data["rule"]["actions"].append(action.encodeJSON())
        
        # Remplacement des ' par des "
        jsonRule = str(data)
        jsonRule = jsonRule.replace('\'','\"')
        
            
        # Transformation au format JSON et retour
        return jsonRule          
        
    
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
        
    def supprimerRule(self, nomRule):
        '''
        Supprimer une regle parmi la liste de regles. La regle supprimee est identifiee par son nom
        '''
        for rule in self.rules:
            if rule.name == nomRule:
                self.rules.remove(rule)
        


class Action():
    '''
    Classe Action. Une action survient lorsque des conditions sont respectees. Fait parti d'une Rule.
    '''

    def __init__(self, levier="",valeur=""):
        # Levier
        self.actuator = levier
        # Valeur du levier
        self.value = valeur
        
    def encodeJSON (self):
        return {'actuator':self.actuator, 'value':self.value}

    
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
        
    def encodeJSON (self):
        return {'type':self.type, 'leftOp':self.leftOp, 'rightOp':self.rightOp}
            
        
class ConditionDate(Condition):
    '''
    Classe Condition pour une date. Herite de la classe Condition
    '''
    
    def __init__(self, typeC="", date=""):
        # Type Condition
        self.type = typeC
        # Date de la condition
        self.date = date
        
    def encodeJSON (self):
        return {'type':self.type, 'date':self.date}

