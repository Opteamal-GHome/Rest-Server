from twisted.web import resource

class AdminHTML(resource.Resource):
    def render_GET(self, request):
        '''
        Methode de reponse a localhost:5000/admin
        '''
        
        headerFile = open("../ClientPC/header.html")
        headerHtml = headerFile.read()
        headerHtml = headerHtml.replace("$STYLE$", "core_admin.css")
        headerFile.close()      
        
        adminFile = open("../ClientPC/core_admin.html")
        adminHtml = adminFile.read()
        adminFile.close()

        footerFile = open("../ClientPC/footer.html")
        footerHtml = footerFile.read()
        footerFile.close()
        
        return headerHtml + adminHtml + footerHtml
        

    def render_POST(self, request):
        return self.render_GET(request)
    
    
    
    
    
    
class Admin():
    '''
    Classe Admin
    '''
