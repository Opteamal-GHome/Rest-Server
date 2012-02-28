import pickle
import constantes

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
        
        # On ouvre le fichier en mode ecriture
        with open(constantes.nomFichierRules, 'w') as fichier:
            pick = pickle.Pickler(fichier)
            
            # On ecrit l'objet rule dans le fichier
            pick.dump(rule)
        
        
    def recreateRules(self):
        '''
        Recupere les regles depuis le fichier
        '''  
        # On ouvre le fichier en mode lecture
        with open(constantes.nomFichierRules, 'r') as fichier:
            depick = pickle.Unpickler(fichier)
            
            # On ouvre un objet
            rule = depick.load()

            # Et on le sauvegarde
            self.ensRules.ajouterRule(rule)
            
        
    def closeFile(self):
        '''
        Fermeture du fichier
        '''
        
        self.file.close()