import importlib


from mods.screenshot import screenshot
from mods.systeminfo import systeminfo
from mods.urlDownload import urlDownload
from mods.urlUploader import UrlUploader



class Helper:
    def __init__(self):
        self.info = ""

    def helpfunctions(self):
        self.info = """
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        h1 { color: #333; }
        h3 { color: #666; }
        .module { margin-bottom: 20px; border-bottom: 1px solid #ccc; padding-bottom: 10px; }
        .command { font-weight: bold; color: #0066cc; }
        .args { margin-left: 20px; }
    </style>
</head>
<body>
    <h1 align="center">Information about Modules</h1>

    <div class="module">
        <p><b>help</b> - Lends you a helping Hand</p>
        <p class="command">Commands- <i>:help</i></p>
    </div>
"""

        listOfClasses = [screenshot, systeminfo, urlDownload, UrlUploader]
        for classes in listOfClasses:
            Class = classes()
            self.info += f"""
    <div class="module">
        <h2><b>{Class.name}</b> - {Class.info}</h2>
        <p class="command">Commands - <i>{Class.command}</i></p>
        <p>Args:</p>
        <ul class="args">
"""
            if Class.args == []:
                self.info += "<li>No Arguments</li>\n"
            else:
                for arg in Class.args:
                    self.info += f"<li>{arg}</li>\n"
        
            self.info += """
        </ul>
    </div>
"""

        self.info += """
    <h3>FOR TRIAL PURPOSE SEND TEXT :help</h3>
</body>
</html>
"""
        return self.info
    
    def run(self,EmailHandler,msgId):
        EmailHandler.send_email(
            message = self.helpfunctions(),
            msgId=msgId,
            reply=True
        )

if __name__ == "__main__":
    help = Helper()
    print(help.helpfunctions())
    


        
        

    

