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
            print client
        if numberOfClients < parameters.players:
            for x in xrange(numberOfClients, parameters.players):
                print x
    else:
        for x in xrange(0, parameters.players):
                print x


def parse_args():
    parser = argparse.ArgumentParser(
        description="Launches the server p clients which"
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
        "-p", "--players",
        help="Specifies the number of players. Defaults to {0}."
        .format(constants["players"]),
        default=constants["players"],
        type=int)
    parser.add_argument(
        "-c", "--client",
        help="Signifies this client to be run. " +
        "As an example ./gamerunner.py -p 2 -c ../test-clients/python/test_" +
        "client.py -c ../test_clients/java/test_client.jar\n" +
        "Any clients not specified will be replaced by the python test client",
        action="append")
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


def main():
    global parameters
    parameters = parse_args()
    sys.stdout.write("Creating server with {0} players, ".format(
        parameters.players))
    print "and {0} as the map\n".format(parameters.map)
    print "Running server on port {0}\n".format(parameters.port)

    serv = MMServer(parameters.players,
                    game.Game(parameters.map))
    serv.run(parameters.port, launch_clients)


if __name__ == "__main__":
    main()
