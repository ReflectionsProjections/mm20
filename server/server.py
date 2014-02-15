##
#   This is a basic socket server that connects to X clients, where X is passed in at runtime, and then stops accepting incoming connections.
#   It opens up the connection for each client on separate threads, so that it always knows which player it is communicating with,
#   and then sends turn information to the engine. It waits some small amount of time for a turn before assuming that none was sent.
#   It waits indefinitely for the engine to finish processing a turn, so it will never close if the engine crashes.
#   Upon receiving the turn data from the engine, it will ignore any messages sent while the turn was being processed, 
#   and send a message back to the player to take their next turn.
#   If a connection is dropped, that player automatically 'forfeits'
#   When the game ends, the server should send a final status to all players and then shut down gracefully.
import SocketServer
import sys
import json
from threading import Timer

turnObjects = None
validTurns = 0
maxPlayers = 0
currPlayers = 0

##
#   This class holds onto objects needed to run the game
class MMRunServer():

    ##
    #   Constructor.
    #   @param numPlayers number of players to enter the game
    def __init__(self, numPlayers):
        global maxPlayers
        maxPlayers = numPlayers
        turnObjects = [None for i in range(0, numPlayers)]
        server = MMServer(("localhost", 8080), TCPHandler)
        # terminate with Ctrl-C
        timer = Timer(1, self.timeup)
        timer.start()
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            sys.exit(0)
        timer = Timer(1, self.timeup)
        timer.start()
    def timeup(self):
        print "TIME'S UP"


##
#   Handles requests
class TCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global currPlayers
        if(maxPlayers == currPlayers):
            return
        currPlayers+=1
        while 1:
            data = self.request.recv(1024)
            if not data:
                break
            print data

class MMServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True
    connectedClients = 0
    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":
    runner = MMRunServer(1)