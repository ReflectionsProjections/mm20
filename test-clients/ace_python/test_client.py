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

    debugRoomNames = {
      "234 100 100 255": "Hallway",
      "186 255 0 255": "Key Lime Pie",
      "252 255 0 255": "Sunny Side Up",
      "255 114 0 255": "Pride without the Blue",
      "0 12 255 255": "Pride without the Orange",
      "128 83 183 255": "Lighter Purple",
      "180 0 255 255": "Actually Purple",
      "52 6 71 255": "The darker side of Purple",
      "111 92 76 255": "Graybrown",
      "255 180 119 255": "Puke Orange",
      "221 255 119 255": "Puke Green",
      "207 177 219 255": "Lightest Purple",
      "118 131 83 255": "Army Green",
      "161 164 154 255": "Overcast",
      "198 221 229 255": "Light Baby Blue",
      "0 186 255 255": "Halfway to Cyan",
      "0 255 204 255": "Cyan",
      "183 108 67 255": "Stairwell",
      "41 249 0 255": "Background Green",
      "240 240 240 255": "Out There"
    }

    actions = []
    for m_id, m in members.iteritems():

        act = {}
        act["person_id"] = m["person_id"]

        # Move into room with a snacktable
        TARGET = "255 114 0 255" # Has a snacktable
        if m["location"] != TARGET:
            act["action"] = "move"
            connected_rooms = map_dict[m["location"]]["connectedRooms"]
            
            if TARGET in connected_rooms:
                act["room"] = TARGET
            else:
                act["room"] = random.choice(connected_rooms)

            #sys.stderr.write("%s: %s --> %s \n" % (m["name"], debugRoomNames[m["location"]], debugRoomNames[act["room"]]));
            
        # Standard actions
        else:
            if "messages" in value:
                for message in value["messages"]:
                    if message["success"] is False and\
                            message["reason"] == "HUNGRY":
                        act["action"] = "eat"
            if "action" not in act:
                if m["hunger"] > 75:
                    act["action"] = "eat"
                if m["stats"]["theorize"] == 10:
                    act["action"] = "theorize"
                elif m["stats"]["test"] == 10:
                    act["action"] = "code"
                    act["type"] = "test"
                else:
                    act["action"] = "code"
                    act["type"] = "implement"
        actions.append(act)
    return actions

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall('{"team":"ace_test", "members":[{"name":"atest1", "archetype":"Coder"},{"name":"atest2", "archetype":"Architect"},{"name":"atest3", "archetype":"Theorist"}]}\n')
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
