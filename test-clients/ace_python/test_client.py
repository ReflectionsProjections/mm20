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

    # Find coding room if possible
    if not coding_room:
      for r_name, r in global_map.iteritems:

        # Coding room must have adjacent food
        if "FOOD" not in r.get("connectedRooms", dict()).get("resources", []):
          continue


    # Determine actions
    aiStats = value.get("aiStats")
    actions = []
    for m_id, m in members.iteritems():
        act = {}
        act["person_id"] = m["person_id"]

        # Get data
        room = global_map[m["location"]]
        friendsInRoom = sum(int(m["location"] == m2["location"]) for m2 in members) - 1

        actionSet = False

        # Get food
        if m["hunger"] > 75:

          # Eat if possible
          if "FOOD" in room["resources"]:
            actionSet = True
            act["action"] = "eat"

          # Move to snacktable room
          else:
            act["action"] = "move"
            connected_rooms = room["connectedRooms"]
            
            # Find room with food
            acmOffice = None
            for r in connected_rooms:
              if "FOOD" in global_map.get(r, dict()).get("resources", []):
                acmOffice = r
                break

            # Go to other room
            if acmOffice:
                actionSet = True
                act["room"] = acmOffice

            #sys.stderr.write("%s: %s --> %s \n" % (m["name"], debugRoomNames[m["location"]], debugRoomNames[act["room"]]));
            
        # Move to coding room
        elif coding_room and room != coding_room:
          if coding_room in room["connectedRooms"]:
            act["action"] = "move"
            act["room"] = coding_room
            actionSet = True

        # Code if in coding room
        elif coding_room and room == coding_room:

          # Basic needs
          if m["fatigue"] + m["hunger"] > 100:
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
    coding_room = None
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
