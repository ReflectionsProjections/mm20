##
#   This is a basic socket server that connects to X clients, where X is passed in at runtime, and then stops accepting incoming connections.
#   It opens up the connection for each client on separate threads, so that it always knows which player it is communicating with,
#   and then sends turn information to the engine. It waits some small amount of time for a turn before assuming that none was sent.
#   It waits indefinitely for the engine to finish processing a turn, so it will never close if the engine crashes.
#   Upon receiving the turn data from the engine, it will ignore any messages sent while the turn was being processed,
#   and send a message back to the player to take their next turn.
#   If a connection is dropped, that player automatically 'forfeits'
#   When the game ends, the server should send a final status to all players and then shut down gracefully.
import sys
import json
import select
import socket
from threading import Timer, Lock
import time

timeLimit = 30
maxDataSize = 1024

class MMServer():
    def __init__(self, numPlayers):
        self.maxPlayers = numPlayers

    def run(self):
        #create an INET, STREAMing socket
        serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        #Set reuse address so that we don't have to wait before running again
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #bind the socket localhost port 8080
        serversocket.bind(('localhost', 8088))
        #become a server socket
        serversocket.listen(5)
        playerConnections = [None for i in range(0, self.maxPlayers)]
        turnObjects = [None for i in range(0, self.maxPlayers)]
        validTurns = 0
        #Accept connections from correct tnumber of players
        for i in range(0, self.maxPlayers):
            (clientsocket, address) = serversocket.accept()
            playerConnections[i] = clientsocket
        lookupPlayer = dict(zip(playerConnections, [i for i in range(0, self.maxPlayers)]))
        currTime = time.time()
        endTime = time.time() + timeLimit
        while 1:
            #Receive info
            ready = None
            if endTime - currTime > 0:
                ready = select.select(playerConnections, [], [], endTime - currTime)
            if ready is None:
                #Timeout
                for i in range(0, self.maxPlayers):
                    if turnObjects[i] is None:
                        turnObjects[i] = '{}'
                        validTurns = validTurns + 1
            for connection in ready[0]:
                #Receive data
                data = connection.recv(maxDataSize)
                player = lookupPlayer[connection]
                if turnObjects[player] is None:
                    turnObjects[player] = data
                    validTurns = validTurns+1
            if validTurns == self.maxPlayers:
                #TODO: send data to engine
                #clear turn objects
                validTurns = 0
                for i in range(0, self.maxPlayers):
                    turnObjects[i]=None
                #reset endtime
                currTime = time.time()
                endTime = time.time() + timeLimit
            else:
                currTime = time.time()

if __name__ == "__main__":
    serv = MMServer(2)
    serv.run()
