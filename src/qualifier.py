#!/usr/bin/env python2
import os
import gamerunner
import signal
import json
import sys
import socket

FNULL = open(os.devnull, 'w')
port = 8000

path, filename = os.path.split(os.path.abspath(__file__))
path += "/mm20-competitors"
teams = {}
OUTPUT_NAME = "qualified_teams.txt"
OUTPUT_NAME2 = "qualified_names.txt"

TIMEOUT = 120   # two minute timeout make that 4 min
skip = ["passwords.txt", "plog", "pull_from_git.py", "push_to_git.py", "team_member.py", "action_handler.py"]

class Alarm(Exception):
    pass


def alarm_handler(signum, frame):
    raise Alarm

signal.signal(signal.SIGALRM, alarm_handler)


def add_team(team,team_dir,testGame):
    name = team
    if qualify(name, team_dir):
        teams[name] = team_dir
    else:
        print name+" failed to qualify"


def qualify(name, team_dir):
    signal.alarm(TIMEOUT)  # set timeout
    try:
        stdout = sys.stderr
        global port
        port +=1
        result = gamerunner.test_game(name, team_dir, port)
        signal.alarm(0)  # cancel alarm
        sys.stdout = sys.__stdout__ 
        print name + "works"
        return result
    except Alarm:
        sys.stdout = sys.__stdout__ 
        print name + " timed out"
        for c in gamerunner.client_list:
            c.stop()
            c.kill()
        return False
    except socket.timeout:
        sys.stdout = sys.__stdout__ 
        print name + "socket timed out"
        for c in gamerunner.client_list:
            c.stop()
            c.kill()
        return False

def qualifyed_teams(testGame=True):
    for dir_entry in os.listdir(path):
        if dir_entry in skip:
            continue
        dir_entry_path = os.path.join(path, dir_entry)
        files = os.listdir(dir_entry_path)
       
        if "run.sh" in files:
            add_team(dir_entry,
                     dir_entry_path, testGame)
        else:
            print "error missing run.sh for entry " + dir_entry

            
    return teams
    

if __name__ == "__main__":
    qualifyed_teams()
    with open(OUTPUT_NAME, 'w') as f:
        f.write(json.dumps(teams))

    with open(OUTPUT_NAME2, 'w') as f:
        f.write(json.dumps(teams.keys()))
