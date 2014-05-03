#!/usr/bin/python2
import socket
import json

TeamName = "Runners"
TeamMembers = [
    {'name': "Joe", 'archetype': "Coder"},
    {'name': "Kim", 'archetype': "Theorist"},
    {'name': "Mortimer", 'archetype': "Architect"},
    {'name': "Sasha", 'archetype': "Informant"}]


## Communicates with the server and runs the client
class Client(object):
    def __init__(self):
        self.host = 'localhost'
        self.port = 8080
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.team = Team(TeamName)
        for member in TeamMembers:
            self.team.addMember(member['name'], member['archetype'])

    def connect(self):
        self.socket.connect((self.host, self.port))
        self.socket.sendall(self.team.getAddTeamJSON())
        data = self.recieve()
        print data
        self.run()

    def recieve(self):
        data = ""
        while data[-1:] != '\n':
            data += self.socket.recv(1024)
        return data

    def run(self):
        while True:
            pass


## Holds information on this client's team
class Team(object):
    def __init__(self, name):
        self.name = name
        self.members = {}
        self.AI = AI()

    def addMember(self, name, archetype):
        self.members[name] = TeamMember(name, archetype)

    def getAddTeamJSON(self):
        ret = {}
        ret['team'] = self.name
        members = list()
        for member in self.members.itervalues():
            members.append(
                {'name': member.name,
                 'archetype': member.archetype})
        ret['members'] = members
        return json.dumps(ret)


## Holds information on each team member in this client's team
class TeamMember(object):
    def __init__(self, name, archetype):
        self.name = name
        self.archetype = archetype


## Holds information on this client's AI
class AI(object):
    def __init__(self):
        self.optimization = None
        self.stability = None
        self.complexity = None
        self.theory = None
        self.implementation = None

if __name__ == "__main__":
    client = Client()
    client.connect()
