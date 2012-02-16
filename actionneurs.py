class ActionneursFactory():
    '''
    Ensemble d'actionneurs
    '''
    
    def __init__(self):
        ''' Methode Initialisation de la classe '''
        actionneur1 = Actionneur(10, 'Salon')
        actionneur2 = Actionneur(2, 'Chambre')
        self.actionneurs=[actionneur1, actionneur2]
        #self.actionneurs = []
        
    def getActionneur (self, idA):
        ''' 
        Retourne le capteur designe par l'idC en parametre
        '''
        for actionneur in self.actionneurs:
            if (str(actionneur.id) == str(idA)):
                return actionneur
        
        
    def ajouterActionneur(self, actionneur):
        '''
        Ajout d'un actionneur
        Si l'actionneur n'existe pas deja, alors il est ajoute
        '''
        if actionneur.id not in self.getIDActionneurs():
            self.actionneurs.append(actionneur)
            
    def modifierActionneur(self, idA, value):
        '''
        Modifie la valeur de l'actionneur identifie par un id et une donnee
        Si l'actionneur existe, alors sa valeur est modifie avec le parametre "value"
        '''
        trouve = False
        for actionneur in self.actionneurs :
            if actionneur.id == idA:
                trouve = True
                actionneur.value = value
                
        return trouve
            
            
    def getIDActionneurs(self):
        '''
        Retourne la liste des ID des actionneurs connectes
        '''
        liste = []  
        for actionneur in self.actionneurs:
            liste.append(actionneur.id)
        return liste
    

    
class Actionneur():
    '''
    Classe Actionneur
    '''
    
    def __init__(self, idA = "", nom = "", typeC = "", value = ""):
        # ID de l'actionneur
        self.id = idA       
        # Nom de l'actionneur
        self.nom = nom
        # Type de l'actionneur
        self.type = typeC       
        # Valeur de l'actionneur
        self.value = value
    