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

timeLimit = 30
maxDataSize = 1024

class MMServer():
    def __init__(self, numPlayers):
        self.maxPlayers = numPlayers

    def run(self):
        #create an INET, STREAMing socket
        serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        #bind the socket to a public host,
        # and a well-known port
        serversocket.bind(('localhost', 8080))
        #become a server socket
        serversocket.listen(5)
        playerConnections = [None for i in range(0, self.maxPlayers)]
        turnObjects = [None for i in range(0, self.maxPlayers)]
        for i in range(0, self.maxPlayers):
            (clientsocket, address) = serversocket.accept()
            playerConnections[i] = clientsocket
        while 1:
            ready = select.select(playerConnections, [], [], timeLimit)
            data = '{}'
            for connection in ready[0]:
                data = connection.recv(maxDataSize)
            print data

if __name__ == "__main__":
    serv = MMServer(2)
    serv.run()
