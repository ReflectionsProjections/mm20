#!/usr/bin/python2
import socket
import json

HOST = 'localhost'
PORT = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall('{"team":"test", "members":[{"name":"test1", "class":"Coder"},{"name":"test2", "class":"Architect"},{"name":"test3", "class":"Theorist"}]}')
data = s.recv(1024)
game_running = True
members = None
while len(data) > 0 and game_running:
    value = None
    try:
        value = json.loads(data)
        print 'Received', repr(data)
        if 'winner' in value:
            game_running = False
        else:
            if members == None:
                members = []
                for person in value["team"]:
                    members.append(person)
            actions = []
            for m in members:
                act = {}
                act["member"] = m["person_id"]
                if "messages" in value:
                    for message in value["messages"]:
                        if message["success"] == False and message["reason"] == "HUNGRY":
                            act["action"] = "eat"
                if "action" not in act:
                    if m["archetype"]["theorize"] == 10:
                        act["action"] = "theorize"
                    elif m["archetype"]["test"] == 10:
                        act["action"] = "code"
                        act["type"] = "test"
                    else:
                        act["action"] = "code"
                        act["type"] = "implement"
                actions.append(act)
            s.sendall(json.dumps(actions))
            data = s.recv(1024)
    except ValueError:
        data += s.recv(1024)
s.close()
