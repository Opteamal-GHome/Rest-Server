class ActionneursFactory():
    '''
    Ensemble d'actionneurs
    '''
    
    def __init__(self):
        ''' Methode Initialisation de la classe '''
        actionneur1 = Actionneur(10, 'Salon')
        actionneur2 = Actionneur(2, 'Chambre')
        self.actionneurs=[actionneur1, actionneur2]
        
        
    def ajouterActionneur(self, actionneur):
        if actionneur.id not in self.getIDActionneurs():
            self.actionneurs.append(actionneur)
            
    def modifierActionneur(self, idA, value):
        '''
        Modifie la valeur de l'actionneur identifie par un id et une donnee
        '''
        for actionneur in self.actionneurs :
            if actionneur.id == idA:
                actionneur.value = value
            
            
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
    