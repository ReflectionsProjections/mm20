##
#   This is a basic socket server that connects to X clients, where X is passed in at runtime, and then stops accepting incoming connections.
#   It opens up the connection for each client on separate threads, so that it always knows which player it is communicating with,
#   and then sends turn information to the engine. It waits some small amount of time for a turn before assuming that none was sent.
#   It waits indefinitely for the engine to finish processing a turn, so it will never close if the engine crashes.
#   Upon receiving the turn data from the engine, it will ignore any messages sent while the turn was being processed,
#   and send a message back to the player to take their next turn.
#   If a connection is dropped, that player automatically 'forfeits'
#   When the game ends, the server should send a final status to all players and then shut down gracefully.
import config.handle_constants
import sys
import select
import socket
import time
import json
import game

constants = config.handle_constants.retrieveConstants("serverDefaults")


class _logger(object):
    """
    A simple logger that prints stuff out
    """

    def __init__(self, ):
        """
        Does nothing
        """

    def print_stuff(self, stuff):
        """
        prints stuff
        """
        print str(stuff)


class MMServer( object ):
    ##
    #   Constructs the server
    #   @param numPlayers number of players entering the game
    #   @param game Game object that holds the game state
    #   @param log location of the log file
    #   @param timeLimit
    #       The amount of time to wait for a player to make their turn
    #   @param maxDataSize
    #      The length in bytes of data received in one call to recv
    def __init__(self, numPlayers, game, logger=_logger(),
                 timeLimit=constants["time"], maxDataSize=constants["maxDataSize"]):
        self.maxPlayers = numPlayers
        self.game = game
        self.logger = logger
        self.timeLimit = timeLimit
        self.maxDataSize = maxDataSize
        self.initialTimeLimit = constants["initialConnectTime"]

    ##
    #   Runs the game
    #   @param port the port number to wait on
    def run(self, port, run_when_ready=None, run_for_each=None):
        #create an INET, STREAMing socket
        serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        #Set reuse address so that we don't have to wait before running again
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #bind the socket to localhost and the port
        serversocket.bind(('localhost', port))
        #become a server socket
        serversocket.listen(self.maxPlayers)
        playerConnections = [None for i in range(0, self.maxPlayers)]
        turnObjects = [None for i in range(0, self.maxPlayers)]
        recval = ["" for i in range(0, self.maxPlayers)]
        forfeit = [False for i in range(0, self.maxPlayers)]
        validTurns = 0
        print 'connecting ...'
        if run_when_ready:
            run_when_ready()
        #Accept connections from correct number of players
        for i in range(0, self.maxPlayers):
            if run_for_each:
                run_for_each()
            (clientsocket, address) = serversocket.accept()
            playerConnections[i] = clientsocket
        lookupPlayer = dict(zip(playerConnections, [i for i in range(0, self.maxPlayers)]))
        print 'sockets connected ...'
        #Accept starting connection first
        starting = True
        currTime = time.time()
        endTime = time.time() + self.initialTimeLimit
        while starting:
            ready = [[],[],[]]
            #Receive info
            if endTime - currTime > 0:
                ready = select.select(playerConnections, [], [], endTime - currTime)
            if ready[0] == [] :
                #Forfeits when there is a timeout on initial connection
                for i in range(0, self.maxPlayers):
                    if turnObjects[i] is None:
                        turnObjects[i] = json.loads('{ "status": "Failure", "errors" : ["Timeout on initial connection, auto-forfeit. '+
                        'Make sure that your starting message was formatted correctly. '+
                        'It should end with \'\\n\'"], "team_name": false }')
                        forfeit[i] = True
                        validTurns = validTurns + 1
            else:
                for connection in ready[0]:
                    #Receive data
                    player = lookupPlayer[connection]
                    try:
                        recval[player] += connection.recv(self.maxDataSize)
                    except socket.error as e:
                        forfeit[player] = True
                        continue
                    validJson = True
                    if turnObjects[player] is None and "\n" in recval[player]:
                        data = recval[player].split("\n")[0]
                        try:
                            jsonObject = json.loads(data)
                        except ValueError, TypeError:
                            jsonObject = {}
                            validJson = False
                        if validJson:
                            (success, response) = self.game.add_new_team(jsonObject, player)
                            if success:
                                turnObjects[player] = response
                                validTurns = validTurns+1
                            else:
                                try:
                                    connection.sendall(json.dumps(response, ensure_ascii=True)+"\n")
                                except IOError:
                                    pass
                        else:
                            try:
                                connection.sendall(json.dumps(json.loads('{ "status": "Failure", "errors" : ["Not valid JSON"], "team_name": false }'), ensure_ascii=True)+"\n")
                            except IOError:
                                pass
            if validTurns == self.maxPlayers:

                starting = False

                #Return turn info back to the clients
                for i in range(0, self.maxPlayers):
                    try:
                        playerConnections[i].sendall(json.dumps(turnObjects[i], ensure_ascii=True)+"\n")
                    except IOError:
                        pass
            currTime = time.time()
        self.logger.print_stuff(json.dumps(turnObjects))
        validTurns = 0
        for i in range(0, self.maxPlayers):
            turnObjects[i]=None
        for i in range(0, self.maxPlayers):
            recval[i]=""
        currTime = time.time()
        endTime = time.time() + self.timeLimit
        running = True
        errors = [[] for i in turnObjects]
        while running:
            #Receive info
            ready = [[],[],[]]
            if endTime - currTime > 0:
                ready = select.select(playerConnections, [], [], endTime - currTime)
            if ready[0] == []:
                #Timeout
                for i in range(0, self.maxPlayers):
                    if turnObjects[i] is None:
                        turnObjects[i] = {}
                        errors[i] = ["Timeout. Make sure that your message ends with '\n'"]
                        validTurns = validTurns + 1
            else:
                for connection in ready[0]:
                    #Receive data
                    player = lookupPlayer[connection]
                    try:
                        recval[player] += connection.recv(self.maxDataSize)
                    except socket.error as e:
                        forfeit[player] = True
                        continue
                    if turnObjects[player] is None and "\n" in recval[player]:
                        try:
                            turnObjects[player] = json.loads(recval[player])
                            validTurns = validTurns+1
                        except ValueError, TypeError:
                            turnObjects[player] = {}
                            errors[player] = ["Invalid JSON"]
                            validTurns = validTurns+1
            if validTurns == self.maxPlayers:
                #Send turns to engine
                for i in range(0, self.maxPlayers):
                    if not forfeit[i] and errors[i] == []:
                        errors[i] = self.game.queue_turn(turnObjects[i], i)

                running = self.game.execute_turn()

                # set up a buffer to hold what we need to send players
                player_data_for_turn = [None] * self.maxPlayers
                #Return turn info back to the clients
                for i in range(0, self.maxPlayers):
                    if not forfeit[i]:
                        try:
                            data = self.game.get_info(i)
                            if running:
                                data["errors"] = errors[i]
                            player_data_for_turn[i] = data
                            playerConnections[i].sendall(
                                json.dumps(player_data_for_turn[i], ensure_ascii = True) + "\n")
                        except IOError:
                            pass
                #log what infomation is sent to the clients
                self.logger.print_stuff(json.dumps(player_data_for_turn))

                #clear turn objects
                validTurns = 0
                for i in range(0, self.maxPlayers):
                    turnObjects[i]=None
                for i in range(0, self.maxPlayers):
                    recval[i]=""
                errors = [[] for i in turnObjects]
                #reset endtime
                currTime = time.time()
                endTime = time.time() + self.timeLimit
            else:
                currTime = time.time()
        #Close connections
        for conn in playerConnections:
            conn.close()
        serversocket.close()

if __name__ == "__main__":
    serv = MMServer(constants["players"], game.Game(constants["map"]))
    serv.run(constants["port"])
