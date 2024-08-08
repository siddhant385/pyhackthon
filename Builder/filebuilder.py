


#FOLDERS
output = "../output/"

#PATHS
mainfile = "../bot/gmail.py"
pythonpayloadfile = output+"gmail.py"


class Builder:
    def __init__(self,botemail,botpass,youremail) -> None:
        self.BOTEMAIL = botemail
        self.BOTPASSWORD = botpass
        self.YOUREMAIL = youremail
    
    def setCreds(self):
        with open(mainfile,'r')as f:
            code = f.read()
            f.close()
        code = code.replace("###Username",self.BOTEMAIL)
        code = code.replace('###Password',self.BOTPASSWORD)
        code = code.replace("###YourEmail",self.YOUREMAIL)
        with open(mainfile,'w')as f:
            f.write(code)
            f.close()

if __name__ == "__main__":
    b = Builder('ssiddhant.ssharma@gmail.com','Hellow world','kriyaporu@gmail.com')
    b.setCreds()