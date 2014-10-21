#!/usr/bin/env python2
from subprocess import Popen
import vis.visualizer
from urllib2 import urlopen, URLError
import json
import pickle
import argparse
import os
import game
import config.handle_constants
import sys
import time

FNULL = open(os.devnull, 'w')
constants = config.handle_constants.retrieveConstants("serverDefaults")
vis_constants = config.handle_constants.retrieveConstants("visualizerDefaults")
parameters = None


class Scoreboard(object):
    def __init__(self, url=None):
        self.lunched = False
        self.url = url
        if url is None:
            self.url = "http://localhost:7000"
            self.lunched = True
            self.board = self.bot = Popen([sys.executable, "scoreServer.py"],
                                          stdout=FNULL, stderr=FNULL)
            time.sleep(1)
        
    def turn(self, turn):
        try:
            r = urlopen(self.url, turn)
            if(r.getcode() != 200):
                raise Exception("Scoreboard update failed!")

        except URLError:
            if not self.lunched:
                self.stop()
                raise  # Exception("Scoreboard update failed!")

    def kill(self):
        if (self.lunched and not self.board.poll()):
            try:
                self.board.kill()
            except OSError:
                pass

    def stop(self):
        """
        """
        if self.lunched:
            try:
                self.board.terminate()
            except OSError:
                pass
                
    def __del__(self):
        self.kill()


def parse_args():
    parser = argparse.ArgumentParser(
        description="play a preran game")
    parser.add_argument(
        "-w", "--debug-view",
        help="Runs the debug view to help you find your problem!",
        const=True,
        default=False,
        action="store_const",
    )
    parser.add_argument(
        "-l", "--log",
        help="Specifies a log file where the game log will be written. " +
        "For example, ./gamerunner.py --log BUTT.out, Defaults to {0}".
        format(constants["log"]),
        default=constants["log"])
    parser.add_argument(
        "-m", "--map",
        help="Specifies the map file on which the game should run. " +
        "Defaults to {0}".format(constants["map"]),
        default=constants["map"])
    parser.add_argument(
        "-o", "--mapOverlay",
        help="Specifies the overlay map file on which the game should be shown. " +
        "Defaults to {0}".format(vis_constants["map_overlay"]),
        default=vis_constants["map_overlay"])
    parser.add_argument(
        "-b", "--scoreboard",
        help="Set this to have the scoreboard pop up in a window. " +
        "Fun to watch and helpful for debugging!",
        const=True,
        default=False,
        action="store_const")
    parser.add_argument(
        "--scoreboard-url",
        help="Connect to a running scoreboard server",
        default=None)
    parser.add_argument(
        "-C", "--cached-map",
        help="Speeds up the launch time of the server by using a cached map. " +
        "If you are having any sort of problem try launching without this!",
        const=True,
        default=False,
        action="store_const")
    args = parser.parse_args()
    return args


def main():
    parameters = parse_args()
    json_file = open(parameters.log)
    map_cache_str = "map.cache"

    if os.path.isfile(map_cache_str) and parameters.cached_map:
            with open(map_cache_str, 'r') as f:
                rooms = pickle.load(f)
    else: 
        rooms = game.Game(parameters.map, 60).rooms


    if parameters.scoreboard:
        score = Scoreboard(parameters.scoreboard_url)
    v = vis.visualizer.Visualizer(rooms, parameters.mapOverlay, debug=parameters.debug_view)
    for i, turn_str in enumerate(json_file):
        turn = json.loads(turn_str)
        v.turn(turn_str)
        turn.append(60 * 24)
        turn.append(i)
        if parameters.scoreboard:
            score.turn(json.dumps(turn))
    if parameters.scoreboard:
        score.stop()

if __name__ == "__main__":
    main()
