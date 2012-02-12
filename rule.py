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
        self.error=""
        self.decodeJSONRule(data)
        
        
    def decodeJSONRule(self, msg):
        '''
        Check si les champs de la regle sont vides / si ils sont inexistants
        '''
        
        print('decode')
        
        regleOk = True
    
        # Extraction du nom du message
        if (msg['ruleName'] == "" or msg['ruleName'] == None):
            regleOk = False
            erreur = "nom_regle_vide"
        self.name = msg['ruleName']
    
        # Extraction des conditions      
        for conditionMsg in msg['conditions']:
            # Si la condition est une date
            if conditionMsg['type'][4:8] == "date":
                condition = ConditionDate(conditionMsg['type'][0:3], conditionMsg['date'])
            
            else :
                leftOp = conditionMsg['leftOp']
                if (leftOp == ""):
                    regleOk = False
                    erreur = "capteur_non_present"
                
                rightOp = conditionMsg['rightOp']
                if (rightOp == ""):
                    regleOk = False
                    erreur = "valeur_non_present" 
                              
                typeC = conditionMsg['type']
                if (typeC == ""):
                    regleOk = False
                    erreur = "operateur_non_present" 
          
                condition = Condition(leftOp, typeC, rightOp)
                
            self.conditions.append(condition)
            
        # Extraction des actions
        for actionMsg in msg['actions']:
            levier = actionMsg['actuator']
            valeur = actionMsg['value']
            
            if (levier == ""):
                regleOk = False
                erreur = "actionneur_non_present" 
            
            action = Action(levier,valeur)
            self.actions.append(action)
        
        if regleOk == False:
            self.error = erreur 
                    
    def createJsonRule(self):
        '''
        Cree une chaine de caractere correspondant a une regle au format JSON (envoi au serveur GHome)
        '''
        # Creation de la structure de depart du message JSON
        data = {}
        data["msgType"] = "newRule"
        data["priority"] = str(self.priority)
        
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
        jsonRule = jsonRule.replace('"type": u', '"type": ');
        jsonRule = jsonRule.replace('"rightOp": u', '"rightOp": ');
        jsonRule = jsonRule.replace('"leftOp": u', '"leftOp": ');
        jsonRule = jsonRule.replace('"actuator": u', '"actuator": ');
        jsonRule = jsonRule.replace('"value": u', '"value": ');
        jsonRule = jsonRule.replace('"ruleName": u', '"ruleName": ');
            
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
        '''
        Ajoute la rule en debut de liste
        '''
        self.rules.insert(0,rule);
        
    def supprimerRule(self, nomRule):
        '''
        Supprimer une regle parmi la liste de regles. La regle supprimee est identifiee par son nom
        '''
        for rule in self.rules:
            if str(rule.name) == str(nomRule):
                self.rules.remove(rule)
                
    def modifierPrioriteRule(self, nomRule, priorite):
        '''
        Change la priorite de la regle intitulee nomRule
        '''
        for rule in self.rules:
            if str(rule.name) == str(nomRule):
                rule.priority = priorite 
        
        


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
        return {'type':self.type, 'leftOp':'@'+self.leftOp, 'rightOp':self.rightOp}
            
        
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

