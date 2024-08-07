import os
import sys
import ctypes
import subprocess
import urllib.request

class Startup:
    def __init__(self, service_name, executable_url, executable_path, display_name, description):
        self.service_name = service_name
        self.executable_url = executable_url
        self.executable_path = executable_path
        self.display_name = display_name
        self.description = description

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def run_as_admin(self):
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)

    def install_service(self):
        commands = [
            f'sc create {self.service_name} binPath= "{self.executable_path}" DisplayName= "{self.display_name}"',
            f'sc description {self.service_name} "{self.description}"',
            f'sc config {self.service_name} start= auto',  # Configure the service to start automatically at boot
            f'sc start {self.service_name}'
        ]

        for command in commands:
            try:
                print(f"Executing: {command}")
                subprocess.run(command, check=True, shell=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to execute: {command}")
                print(e)

        print(f"Service {self.service_name} installed and started.")

    def remove_service(self):
        try:
            subprocess.run(f'sc stop {self.service_name}', check=True, shell=True)
            subprocess.run(f'sc delete {self.service_name}', check=True, shell=True)
            print(f"Service {self.service_name} stopped and removed.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to remove the service: {e}")

        # Optionally remove the executable file
        if os.path.exists(self.executable_path):
            try:
                os.remove(self.executable_path)
                print(f"Executable file {self.executable_path} removed.")
            except Exception as e:
                print(f"Failed to remove executable file: {e}")

    def download_executable(self):
        try:
            print(f"Downloading executable from {self.executable_url}...")
            urllib.request.urlretrieve(self.executable_url, self.executable_path)
            print(f"Downloaded executable to {self.executable_path}.")
        except Exception as e:
            print(f"Failed to download the executable: {e}")

    def setup_and_install(self):
        if not self.is_admin():
            self.run_as_admin()
            return

        self.download_executable()
        self.install_service()

if __name__ == "__main__":
    # Configure these variables as needed
    service_name = "MyService"
    executable_url = "https://example.com/path/to/your/executable.exe"  # Replace with the actual URL of your executable
    executable_path = r"C:\path\to\dist\my_service_script.exe"  # Replace with the path where you want to save the executable
    display_name = "My Custom Service"
    description = "This is a custom service that runs a specific application."

    startup = Startup(service_name, executable_url, executable_path, display_name, description)

    # Perform setup and installation
    startup.setup_and_install()
