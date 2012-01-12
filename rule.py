from xml.dom.minidom import Document

class Rule():


    def __init__():
        '''
        Initialisation des Rules 
        '''
        # Tableau des conditions
        self.conditions=[]
        
        
    def decodeJSONRule(self, msg) :
        typeRightOp = msg["typeRightOp"]      
        leftOp = msg["leftOp"]
        rightOp = msg["rightOp"]
        operator = msg["operator"]
      
        condition = Condition(leftOp, operator, typeRightOp, rightOp)
        self.conditions.append(condition)
        
    def createXMLRule(self) :
        '''
        Cree une chaine de caractere correspondant a une regle au format XML
        '''
        # Creation de la base
        doc = Document()
        
        # Creation du <rule>
        rule = doc.createElement("rule")
        doc.appendChild(rule)
        
        # Creation de la balise <conditions>
        bConditions = doc.createElement("conditions")
        rule.appendChild(bConditions)
        
        # Creation des conditions
        for condition in self.conditions:
            # Creation de la balise sup, inf, equ ...
            operator = doc.createElement(condition.operator)
            
            # Ajout des attributs
            if condition.typeRightOp != "date" :
                operator.setAttribute("leftOp", condition.leftOp)
                operator.setAttribute("rightOp", condition.rightOp)
            else:
                operator.setAttribute("date", condition.rightOp)   
                
            bConditions.appendChild(operator)
        
        
         # Creation de l'action
         
         
         # Envoi au socket GHome
        
    
    
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
        self.typeRightOp = typeRightOp
