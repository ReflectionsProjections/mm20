import json

constantsLoaded = False
constants = {}


def retrieveConstants(key):
    global constants
    if constantsLoaded:
        return constants[key]
    constantsFile = open('constants.json', 'r')
    jsonConstantsString = constantsFile.read()
    constants = json.loads(jsonConstantsString)
    return constants[key]
