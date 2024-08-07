import json
import os
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

# Load the bot token from a JSON configuration file
class config:
    def __init__(self):
        self.EMAIL = ""
        self.PASSWORD = ""
        self.YOUREMAIL =""
        self.path = path
        self.getcreds()
        
    
    def getcreds(self):
        with open(self.path, 'r') as config_file:
            config = json.load(config_file)
            self.EMAIL = config['BOT_EMAIL']
            self.PASSWORD = config['BOT_PASSWORD']
            self.YOUREMAIL = config['YOUR EMAIL']
            config_file.close()
        return True
    
    def update(self,email,password,youremail):
        self.EMAIL = email
        self.PASSWORD = password # type: ignore
        self.YOUREMAIL = youremail
        self.changemail()
        return True
    
    def changemail(self):
        with open(self.path, 'r') as config_file:
            config = json.load(config_file)
            config_file.close()
        config['BOT_EMAIL'] = self.EMAIL
        config['BOT_PASSWORD'] = self.PASSWORD
        config['YOUR EMAIL'] = self.YOUREMAIL
        with open('config.json','w')as config_file:
            dconfig = json.dump(config,config_file)
            config_file.close()
        return True
        
        

if __name__ == "__main__":
    c = config()
    print(c.update(
        email="ssiddhant.ssharma@gmail.com",
        password="xzrn zhtk xclv vccz",
        youremail="kriyaporu@gmail.com"
    ))
    print(c.EMAIL)
    print(c.PASSWORD)
            

    

