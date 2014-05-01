#!/usr/bin/python2
import game
from server.server import MMServer
import config.handle_constants

constants = config.handle_constants.retrieveConstants("serverDefaults")


def launch_clients():
    print "Test"


def main():
    serv = MMServer(constants["players"],
                    game.Game(constants["map"]))
    serv.run(constants["port"], launch_clients)


if __name__ == "__main__":
    main()
