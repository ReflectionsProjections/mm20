#!/usr/bin/python2
import socket
import json

HOST = 'localhost'
PORT = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall('{"team":"test", "members":[{"name":"test1", "class":"Coder"},{"name":"test2", "class":"Coder"},{"name":"test3", "class":"Coder"}]}')
data = s.recv(1024)
game_running = True
while len(data) > 0 and game_running:
    value = None
    try:
        value = json.loads(data)
        print 'Received', repr(data)
        if 'winner' in json.loads(data):
            game_running = False
        else:
            s.sendall('[{"action":"theorize", "member":0}]')
            data = s.recv(1024)
    except ValueError:
        data += s.recv(1024)
s.close()
