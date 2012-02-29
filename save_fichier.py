import pickle
import constantes
import os

class SaveFichier():
    
    def __init__(self, ensembleRules):
        '''
        Initialisation d'un fichier. Ouverture en mode 'w'
        '''
        self.ensRules = ensembleRules
        
        # Ouverture du fichier en mode ajout
        self.file = open(constantes.nomFichierRules, "a")
        
    def writeNouvelleRule(self, rule):
        '''
        Ajoute une nouvelle regle dans le fichier
        '''
        
        # On ouvre le fichier en mode ecriture ajout apres
        with open(constantes.nomFichierRules, 'a') as fichier:
            pick = pickle.Pickler(fichier)
            
            # On ecrit l'objet rule dans le fichier
            pick.dump(rule)
            
            
    def writeAllRules(self):
        '''
        Ecrit toutes les regles existantes dans le fichier
        '''            
        # On ecrit toutes les regles
        for rule in self.ensRules.rules:
            self.writeNouvelleRule(rule)
        
        
    def recreateRules(self):
        '''
        Recupere les regles depuis le fichier
        '''  
        # On ouvre le fichier en mode lecture
        with open(constantes.nomFichierRules, 'r') as fichier:
            depick = pickle.Unpickler(fichier)
            
            try:
                # On charge toutes les regles jusqu'a EOF
                while (True):
                    # On ouvre un objet
                    rule = depick.load()
        
                    # Et on le sauvegarde
                    self.ensRules.ajouterRule(rule)
            except EOFError:
                print 'Fin de fichier'
                
    def removeAllRules(self):
        '''
        Supprime toutes les regles contenus dans le fichier --> fichier vide
        '''
        # On supprime le fichier
        os.remove(constantes.nomFichierRules)
        
        # On recree le fichier
        self.file = open(constantes.nomFichierRules, "a")
        self.file.close()
            
        
    def closeFile(self):
        '''
        Fermeture du fichier
        '''
        
        self.file.close()