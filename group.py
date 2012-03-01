'''
Created on 1 mars 2012

@author: tommi
'''

class Group():
    '''
    Groupe de peripheriques
    '''
    
    def __init__(self):
        # Nom du groupe
        self.nom = ""
        # Type du groupe
        self.typeGroupe = ""
        # Liste des peripheriques compris dans le groupe
        self.listePeriph = []
        
    def ajouterPeriph(self, idPeriph):
        '''
        Ajoute un peripherique dans la liste s'il n'y est pas deja
        '''
        if str(idPeriph) not in self.listePeriph:
            self.listePeriph.append(str(idPeriph))
            
    
class GroupFactory():
    '''
    Ensemble de groupes
    '''
    
    def __init__(self):
        # Liste de groupe
        self.listeGroupe = []
        
    def ajouterGroupe(self, groupe):
        '''
        Ajoute un groupe dans la factory
        '''
        self.listeGroupe.append(groupe)
        
    def removeGroupe(self, nomGroupe):
        '''
        Supprime le groupe dont le nom est passe en parametre
        '''
        
        trouve = False
        for device in self.listeGroupe:
            if (device.nom == str(nomGroupe)):
                trouve = True
                self.listeGroupe.remove(device)
                
        return trouve