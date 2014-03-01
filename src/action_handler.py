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


def _serverInfo(game, *args, **kwargs):
    """Returns information about the server
    """
    constants = retrieveConstants('generalInfo')
    return response(200, version=constants.VERSION, name=constants.NAME)
actionDispatch['serverInfo'] = _serverInfo


class TestaActionHandler(TestCase):
    """Holds the test cases to test the Action Handler
    """
    def respone(self):
        """Test that the respone function formats the response correctly.
        """
        self.assertTrue(False)

    def sortAction(self):
        """Test that the sortActions function correctly sorts the actions.
        """
        self.assertTrue(False)

    def bufferAction(self):
        """Tests that the bufferAction function correctly adds an action to the buffer.
        """
        self.assertTrue(False)

    def executeActionExists(self):
        """Tests that the execeuteAction function correctly executes the function given a valid function
        """
        self.assertTrue(False)

    def executeActionNotExists(self):
        """Tests that the executeAction function correctly respons given an invalid action
        """
        self.assertTrue(False)

    def _movePlayerValid(self):
        """Tests that the _movePlayer function returns the same thing as the player.move function given valid parameters.
        """
        self.assertTrue(False)

    def _movePlayerInvalid(self):
        """Tests that the _movePlayer function returns _INVALID given invalid parameters
        """
        self.assertTrue(False)

    def _eatFoodValid(self):
        """Tests that the _eatFood function returns the same thing as the player.eat function given valid parameters.
        """
        self.assertTrue(False)

    def _eatFoodInvalid(self):
        """Tests that the _eatFood function returns _INVALID given invalid parameters
        """
        self.assertTrue(False)

    def _sleepValid(self):
        """Tests that the _sleep function returns the same thing as the player.sleep function given valid parameters.
        """
        self.assertTrue(False)

    def _sleepInvalid(self):
        """Tests that the _sleep function returns _INVALID given invalid parameters
        """
        self.assertTrue(False)

    def _codeValid(self):
        """Tests that the _code function returns the same thing as the player.code function given valid parameters.
        """
        self.assertTrue(False)

    def _codeInvalid(self):
        """Tests that the _code function returns _INVALID given invalid parameters
        """
        self.assertTrue(False)

    def _getMap(self):
        """Tests that the _getMap function returns the same thing as the loggers mapToJson function
        """
        self.assertTrue(False)

    def _serverInfo(self):
        """Tests that the _serverInfo function returns correct information on the server from constants.json
        """
        self.assertTrue(False)

    def testhHandleTurn(self):
        """Test that handleTurn returns the correct list of responses.
        """
        self.assertTrue(False)

if __name__ == "__main__":
    # Run all of the test cases
    main()
