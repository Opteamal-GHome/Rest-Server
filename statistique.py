from twisted.web import resource

class StatistiqueHTML(resource.Resource):
    def render_GET(self, request):
        '''
        Methode de reponse a localhost:5000/stat
        '''
        

    def render_POST(self, request):
        return self.render_GET(request)
    
    
    
    
class Statistique():
    '''
    Classe Statistique
    '''