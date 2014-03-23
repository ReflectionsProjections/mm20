# actionHandler - Handles the client's actions sent to the engine from the server.
from config.handle_constants import retrieveConstants
from objects.client_action import Action
from unittest import TestCase, main

actionDispatch = {}

## Create a response (on the client) to be sent to the server.
# @param status_code TODO
def response(status_code, **kwargs):
    """
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

## Sort the actions in the action buffer by their priority.
# @param actionBuffer The buffered list of actions to sort.
# @returns TODO
def sortActions(actionBuffer):

    # TODO
    # sort the actions in actionBuffer by priority, see the python
    # built-in sort function
    return

## Adds the action to a buffered list of actions so that it can be executed later.
# @param actionBuffer The buffered list of actions to add the action to
# @param action The action to add to the actionBuffer
# @param args TODO
# @param kwargs TODO
def bufferAction(actionBuffer, action, *args, **kwargs):
    """
    """
    action = Action(action, *args, **kwargs)
    actionBuffer.append({action.key: action})

## Attempts to execute the given action. If it is invalid, a 404 response is returned.
# @param game TODO The current game state?
# @param action The action to execute
# @returns An actionDispatch object indicating (TODO - indicating what?) if the action is successful, a 404 "Invalid Call" response otherwise
def executeAction(game, action):
    if action in actionDispatch:
        return actionDispatch[action.key](game, action.args, action.kwargs)
    else:
        return response(404, message="Invalid call.") # TODO move this to a constants file

## Attempts to move a player. If the move is invalid, a 404 "Invalid Call" response is returned.
# @param action The action to execute
def _movePlayer(game, *args, **kwargs):
    if 'room' in kwargs and 'player' in kwargs:
        return game.people[kwargs['player']].move(kwargs['room'])
    else:
        return _INVALID
    # return _TODO
actionDispatch['movePlayer'] = _movePlayer

## Attempts to eat food from FoodTable
# @param args TODO - Explain valid args
# @param kwargs TODO - Explain valid KWArgs
def _eatFood(game, *args, **kwargs):
    """Attempts to have a player eat the food from FoodTable
    """
    if 'foodTable' in kwargs and 'player' in kwargs:
        return game.people[kwargs['player']].eat(kwargs['foodTable'])
    else:
        return _INVALID
    # return _TODO
actionDispatch['eatFood'] = _eatFood

## Attempts to make a player sleep
# @param args TODO - Explain valid args
# @param kwargs TODO - Explain valid KWArgs
def _sleep(game, *args, **kwargs):
    if 'player' in kwargs and 'hours' in kwargs:
        return game.people[kwargs['player']].sleep(kwargs['hours'])
    else:
        return _INVALID

    # return _TODO
actionDispatch['sleep'] = _sleep

## Attempts to make a player code
# @param args TODO - Explain valid args
# @param kwargs TODO - Explain valid KWArgs
def _code(game, *args, **kwargs):
    if 'player' in kwargs and 'team' in kwargs and 'attribute' in kwargs:
        return game.people[kwargs['player']].code(kwargs['team'], kwargs['attribute'])
    else:
        return _INVALID
    # return _TODO
actionDispatch['code'] = _code

## Returns a serialized-to-json version of the current game map(s?)
# @param args TODO - Explain valid args
# @param kwargs TODO - Explain valid KWArgs
def _getMap(game, *args, **kwargs):
    # This should be the same json interpretation that the logger uses.
    return _TODO
actionDispatch['getMap'] = _getMap

## Returns information about the server
# @param args Not used.
# @param kwargs Not used.
def _serverInfo(game, *args, **kwargs):
    """Returns information about the server
    """
    constants = retrieveConstants('generalInfo')
    return response(200, version=constants.VERSION, name=constants.NAME)
actionDispatch['serverInfo'] = _serverInfo


class TestaActionHandler(TestCase):
    # Test cases for Action Handler

    ## Set up the variables for each test case
    def setup(self):
        return

    ## Test that the response() function formats the response correctly.
    def testRespone(self):

        self.assertTrue(False)

    ## Test that the sortActions() function correctly sorts the actions.
    def testSortAction(self):
        pseudoBuffer = [
            {'priority': 0, 'name': 'last'},
            {'priority': 10, 'name': 'first'},
            {'priority': 5, 'name': 'middle'}
        ]
        sortActions(pseudoBuffer)
        self.assertEquals(pseudoBuffer[0]['name'], 'first')
        self.assertEquals(pseudoBuffer[1]['name'], 'middle')
        self.assertEquals(pseudoBuffer[2]['name'], 'last')

    ## Tests that the bufferAction function correctly adds an action to the buffer.
    def testBufferAction(self):
        validActions = retrieveConstants("actions")
        pseudoBuffer = []
        pseudoAction = validActions[0]
        bufferAction(pseudoBuffer, pseudoAction, target='pseudoTarget')
        self.assertFalse(not pseudoBuffer)
        self.assertEquals(pseudoBuffer[0], validActions[0])

    ## Tests that the executeAction() function correctly executes the action given a valid action.
    def testExecuteActionExists(self):
        self.assertTrue(False)

    ## Tests that the executeAction() function correctly responds given an invalid action.
    def testExecuteActionNotExists(self):
        self.assertTrue(False)

    ## Tests that the _movePlayer function returns the same thing as the player.move function given valid parameters.
    def test_movePlayerValid(self):
        self.assertTrue(False)

    ## Tests that the _movePlayer function returns _INVALID given invalid parameters.
    def test_movePlayerInvalid(self):
        self.assertTrue(False)

    ## Tests that the _eatFood function returns the same thing as the player.eat function given valid parameters.
    def test_eatFoodValid(self):
        self.assertTrue(False)

    ## Tests that the _eatFood function returns _INVALID given invalid parameters.
    def test_eatFoodInvalid(self):
        self.assertTrue(False)

    ## Tests that the _sleep function returns the same thing as the player.sleep function given valid parameters.
    def test_sleepValid(self):
        self.assertTrue(False)

    ## Tests that the _sleep function returns _INVALID given invalid parameters
    def test_sleepInvalid(self):
        self.assertTrue(False)

    ## Tests that the _code function returns the same thing as the player.code function given valid parameters.
    def test_codeValid(self):
        self.assertTrue(False)

    ## Tests that the _code function returns _INVALID given invalid parameters
    def test_codeInvalid(self):
        self.assertTrue(False)

    ## Tests that the _getMap function returns the same thing as the loggers mapToJson function
    def test_getMap(self):
        self.assertTrue(False)

    ## Tests that the _serverInfo function returns correct information on the server from constants.json
    def test_serverInfo(self):
        self.assertTrue(False)

    ## Test that handleTurn returns the correct list of responses.
    def testHandleTurn(self):
        self.assertTrue(True)

if __name__ == "__main__":
    # Run all of the test cases
    main()
