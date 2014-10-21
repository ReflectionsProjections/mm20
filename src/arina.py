import gamerunner
import random
import json
OUTPUT_NAME = "qualified_teams.txt"

with open(OUTPUT_NAME, 'r') as f:
    teams = json.load(f)

gamerunner.arina_game([random.choice(teams.values()) for _ in range(8)], 8083)
