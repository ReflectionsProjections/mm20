#!/usr/bin/python2
import socket
import json
import sys
import random

def updateMembers(members, value):
    if members is None:
        members = {}
        for person in value["team"].values():
            members[person["person_id"]] = person
    if "people" in value:
        for person in value["people"].values():
            if person["person_id"] in members:
                members[person["person_id"]] = person
    return members



#This function determines what actions should be performed each turn
#
#Edit this to change the behavior of the client
#
#@param members A dictionary of team member's current state indexed by their person_id
#@param value The dictionary with turn info sent by the server
def setActions(members, value, map_dict):

    actions = []
    for m_id, m in members.iteritems():
        act = {}
        act["person_id"] = m["person_id"]

        my_room = value["map"][m["location"]]
        for person in my_room["peopleInRoom"]:
            if not person in members:
                act["action"] = "distract"
                act["victim"] = person
                break

        actions.append(act)
    return actions

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall('{"team":"kirby_bot", "members":[{"name":"atest1", "archetype":"Coder"},{"name":"atest2", "archetype":"Architect"},{"name":"atest3", "archetype":"Theorist"}]}\n')
    data = s.recv(1024)
    game_running = True
    members = None
    map_dict = None
    while len(data) > 0 and game_running:

        value = None
        if "\n" in data:
            data = data.split('\n')
            if len(data) > 1 and data[1] != "":
                data = data[1]
                data += s.recv(1024)
            else:
                value = json.loads(data[0])
                if 'winner' in value:
                    game_running = False
                else:
                    if 'map' in value:
                        map_dict = value["map"]
                
                    members = updateMembers(members, value)

                    actions = setActions(members, value, map_dict)
                    
                    s.sendall(json.dumps(actions)+'\n')
                    data = s.recv(1024)
        else:
            data += s.recv(1024)
    s.close()