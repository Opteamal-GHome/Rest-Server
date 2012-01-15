class Capteurs():
    '''
    Classe Capteurs. Est appele lorsque l'utilisateur souhaite la liste des capteurs present
    '''

    def render_GET(self, request):
        '''
        get response method for the Capteurs resource
        localhost:8000/capteurs/
        '''
        
        headerFile = open("../ClientPC/header.html")
        headerHtml = headerFile.read()
        headerFile.close()      
          
        capteurFile = open("../ClientPC/corps_capteur.html")
        capteurHtml = capteurFile.read()
        capteurFile.close()

        footerFile = open("../ClientPC/footer.html")
        footerHtml = footerFile.read()
        footerFile.close()

        return (headerHtml + capteurHtml + footerHtml)