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

    aiStats = value.get("aiStats")
    actions = []
    for m_id, m in members.iteritems():
        act = {}
        act["person_id"] = m["person_id"]

        # Move into room with a snacktable
        if "FOOD" not in global_map[m["location"]]["resources"]:
            act["action"] = "move"
            connected_rooms = global_map[m["location"]]["connectedRooms"]
            
            # Find room with food
            acmOffice = None
            for r in connected_rooms:
              if "FOOD" in global_map.get(r, dict()).get("resources", []):
                acmOffice = r
                break

            # Go to room with food if one is visible
            if acmOffice:
                act["room"] = acmOffice

            # Randomly explore
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

                # Basic needs
                if m["hunger"] > 75:
                    act["action"] = "eat"
                elif m["fatigue"] + m["hunger"] > 100:
                    act["action"] = "sleep"

                # AI work
                elif m["stats"]["theorize"] == 10:
                    act["action"] = "theorize"
                elif m["stats"]["test"] == 10:
                    act["action"] = "code"
                    if aiStats and aiStats["optimization"] < aiStats["implementation"]:
                      act["type"] = "refactor"
                    else:
                      act["type"] = "test"
                else:
                    act["action"] = "code"
                    act["type"] = "implement"
        actions.append(act)
    return actions

if __name__ == "__main__":

    # Connection config
    HOST = 'localhost'
    PORT = 8080

    # Connect
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall('{"team":"ace_test", "members":[{"name":"atest1", "archetype":"Coder"},{"name":"atest2", "archetype":"Architect"},{"name":"atest3", "archetype":"Theorist"}]}\n')
    data = s.recv(1024)

    # Start game
    global_map = dict()
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
                        global_map.update(map_dict)
                
                    members = updateMembers(members, value)
                    actions = setActions(members, value, map_dict)
                    
                    s.sendall(json.dumps(actions)+'\n')
                    data = s.recv(1024)
        else:
            data += s.recv(1024)
    s.close()
