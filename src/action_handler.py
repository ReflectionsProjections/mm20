"""@actionHandler Handles the client's actions sent to the engine from the server.
"""
from config.handle_constants import retrieveConstants
from objects.client_action import Action
from unittest import TestCase, main

actionBuffer = {}
actionDispatch = {}


def response(status_code, **kwargs):
    """Creates a response formatted to be understood by the server.
    """
    kwargs["status"] = status_code
    return kwargs

_TODO = response(500, message="not yet implemented")
_INVALID = response(404, message="invalid call")


def handleTurn(game, listOfAction):
    """Takes in a list of json actions taken by all of the clients and executes them.
    """
    # TODO
    # go through the list, json loads the action and buffer it.
    # sort the buffered actions by priority
    # execute the buffered actions and store their responses in a dictionary
    # return a the response dictionary to the server
    return


def sortActions():
    """Sort the actions in the action buffer by their priority attribute
    """
    # TODO
    # sort the actions in actionBuffer by priority, see the python
    # built-in sort function
    return


def bufferAction(action, *args, **kwargs):
    """Adds the action to a buffered list of actions so that it can be executed later.
    """
    action = Action(action, args, kwargs)
    actionBuffer[action.key] = action


def executeAction(game, action):
    """Executes the given action.
    """
    if action in actionDispatch:
        return actionDispatch[action.key](game, action.args, action.kwargs)
    else:
        return response(404, message="invalid call")


def _movePlayer(game, *args, **kwargs):
    """Attempts to move a player from one room to another
    """
    if 'room' in kwargs and 'player' in kwargs:
        return game.people[kwargs['player']].move(kwargs['room'])
    else:
        return _INVALID
    # return _TODO
actionDispatch['movePlayer'] = _movePlayer


def _eatFood(game, *args, **kwargs):
    """Attempts to have a player eat the food from FoodTable
    """
    if 'foodTable' in kwargs and 'player' in kwargs:
        return game.people[kwargs['player']].eat(kwargs['foodTable'])
    else:
        return _INVALID
    # return _TODO
actionDispatch['eatFood'] = _eatFood


def _sleep(game, *args, **kwargs):
    """Attempts to tell a player to sleep
    """
    if 'player' in kwargs and 'hours' in kwargs:
        return game.people[kwargs['player']].sleep(kwargs['hours'])
    else:
        return _INVALID

    # return _TODO
actionDispatch['sleep'] = _sleep


def _code(game, *args, **kwargs):
    """Attempts to tell a player to code
    """
    if 'player' in kwargs and 'team' in kwargs and 'attribute' in kwargs:
        return game.people[kwargs['player']].code(kwargs['team'], kwargs['attribute'])
    else:
        return _INVALID
    # return _TODO
actionDispatch['code'] = _code


def _getMap(game, *args, **kwargs):
    """Returns a json version of the current game maps
    """
    # This should be the same json interpretation that the logger uses.
    return _TODO
actionDispatch['getMap'] = _getMap


def _info(game, *args, **kwargs):
    """What does this do?
    """
    return _TODO
actionDispatch['info'] = _info


def _serverInfo(game, *args, **kwargs):
    """Returns information about the server
    """
    constants = retrieveConstants('generalInfo')
    return response(200, version=constants.VERSION, name=constants.NAME)
actionDispatch['serverInfo'] = _serverInfo


class TestaActionHandler(TestCase):
    """Holds the test cases to test the Action Handler
    """
    def placeholder(self):
        pass

if __name__ == "__main__":
    # Run all of the test cases
    main()
