#!/usr/bin/python2
from server.server import MMServer
import config.handle_constants
import argparse
import game
import sys

constants = config.handle_constants.retrieveConstants("serverDefaults")
parameters = None


def launch_clients():
    if parameters.client:
        numberOfClients = len(parameters.client)
        for client in parameters.client:
            launch_client(client)
    else:
        numberOfClients = 0
    for x in xrange(numberOfClients, parameters.players):
        launch_client(parameters.defaultClient)


def launch_client(client):
    print client


def parse_args():
    parser = argparse.ArgumentParser(
        description="Launches the server with p clients which "
        + "connect to it.")
    parser.add_argument(
        "-u", "--port",
        help="Specifies the port on which the server should run. " +
        "Defaults to {0}".format(constants["port"]),
        default=constants["port"],
        type=int)
    parser.add_argument(
        "-m", "--map",
        help="Specifies the map file on which the game should run. " +
        "Defaults to {0}".format(constants["map"]),
        default=constants["map"])
    parser.add_argument(
        "-l", "--log",
        help="Specifies a log file where the game log will be written. " +
        "Defaults to {0}".format(constants["log"]),
        default=constants["log"])
    parser.add_argument(
        "-p", "--players",
        help="Specifies the number of players. Defaults to {0}."
        .format(constants["players"]),
        default=constants["players"],
        type=int)
    parser.add_argument(
        "-c", "--client",
        help="Signifies this client to be run. " +
        "As an example ./gamerunner.py -p 3 -c myClient.py -c jimsClient.py " +
        "The gamerunner will run a number of test clients (which can be " +
        "specified with -d) equal to players - specified clients",
        action="append")
    parser.add_argument(
        "-d", "--defaultClient",
        help="The default client to launch when no specific clients " +
        "are given. Defaults to {0}".format(constants["defaultClient"]),
        default=constants["defaultClient"])
    args = parser.parse_args()
    if args.players < 2:
        sys.stdout.write(parser.format_usage())
        print "{0}: error: Cannot run with less than two players".format(
            parser.prog)
        exit(1)
    if args.client and len(args.client) > args.players:
        sys.stdout.write(parser.format_usage())
        print "{0}: error: More clients specified than players".format(
            parser.prog)
        exit(1)
    return args


## A simple logger that writes things to a file
class FileLogger(object):
    def __init__(self, fileName):
        self.file = fileName

    ## The function that logs will be sent to
    # @param stuff
    #   The stuff to be printed
    def print_stuff(self, stuff):
        with open(self.file, 'a') as f:
            f.write(stuff)


def main():
    global parameters
    parameters = parse_args()
    sys.stdout.write("Creating server with {0} players, ".format(
        parameters.players))
    print "and {0} as the map\n".format(parameters.map)
    print "Running server on port {0}\n".format(parameters.port)
    print "Writing log to {0}".format(parameters.log)

    with open(parameters.log, 'w'):
        pass
    fileLog = FileLogger(parameters.log)

    serv = MMServer(parameters.players,
                    game.Game(parameters.map),
                    logger=fileLog)
    serv.run(parameters.port, launch_clients)


if __name__ == "__main__":
    main()
