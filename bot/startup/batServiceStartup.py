import os
import sys
import ctypes
import subprocess

class Startup:
    def __init__(self, service_name, display_name, description):
        self.service_name = service_name
        self.executable_path = os.path.abspath(sys.argv[0])
        self.display_name = display_name
        self.description = description
        self.program_files_path = r"C:\Program Files\MyService"
        self.batch_file_path = os.path.join(self.program_files_path, 'install_service.bat')

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def run_as_admin(self):
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        sys.exit()  # Exit the current script to allow the elevated one to run

    def create_batch_file(self):
        batch_content = f"""
@echo off
sc create {self.service_name} binPath= "{self.executable_path}" DisplayName= "{self.display_name}"
sc description {self.service_name} "{self.description}"
sc config {self.service_name} start= auto
sc start {self.service_name}
        """
        with open(self.batch_file_path, 'w') as batch_file:
            batch_file.write(batch_content)
        print(f"Batch file created at {self.batch_file_path}")

    def install_service(self):
        self.create_batch_file()
        try:
            subprocess.run(self.batch_file_path, check=True, shell=True)
            print(f"Service {self.service_name} installed and started.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to execute batch file: {e}")

    def move_to_program_files(self):
        if not os.path.exists(self.program_files_path):
            os.makedirs(self.program_files_path)
        new_executable_path = os.path.join(self.program_files_path, os.path.basename(self.executable_path))
        try:
            subprocess.run(f'copy "{self.executable_path}" "{new_executable_path}"', check=True, shell=True)
            print(f"Copied executable to {new_executable_path}")
            self.executable_path = new_executable_path  # Update the executable path to the new location
        except subprocess.CalledProcessError as e:
            print(f"Failed to copy executable: {e}")

    def remove_service(self):
        try:
            try:
                subprocess.run(f'sc stop {self.service_name}', check=True, shell=True)
            except:
                subprocess.run(f'sc delete {self.service_name}', check=True, shell=True)
            print(f"Service {self.service_name} stopped and removed.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to remove the service: {e}")
            import time
            time.sleep(10)

        # Optionally remove the batch file
        if os.path.exists(self.batch_file_path):
            try:
                os.remove(self.batch_file_path)
                print(f"Batch file {self.batch_file_path} removed.")
            except Exception as e:
                print(f"Failed to remove batch file: {e}")

        # Optionally remove the executable
        if os.path.exists(self.executable_path):
            try:
                os.remove(self.executable_path)
                print(f"Executable {self.executable_path} removed.")
            except Exception as e:
                print(f"Failed to remove executable: {e}")

    def setup(self):
        if not self.is_admin():
            self.run_as_admin()
            return

        self.move_to_program_files()
        self.install_service()

    def remove(self):
        if not self.is_admin():
            self.run_as_admin()
            return

        self.remove_service()

if __name__ == "__main__":
    # Configure these variables as needed
    service_name = "ChromautoUpdate"
    display_name = "Chorme Auto Update"
    description = "This is a custom service that runs a specific application."

    startup = Startup(service_name, display_name, description)

    # Perform setup and installation
    # startup.setup()

    # Perform removal of the service
    startup.remove()
