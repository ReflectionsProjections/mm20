## actionHandler Handles the client's actions sent to the engine from the server.

import config.handle_constants
import objects.client_action
import unittest

actionDispatch = {}
actionPriorities = {}


## Create a response (on the client) to be sent to the server.
# @param status_code TODO
def response(status_code, **kwargs):
    kwargs["status"] = status_code
    return kwargs

_TODO = response(500, message="not yet implemented")
_INVALID = response(404, message="invalid call")


## Takes in a list of json actions taken by all of the clients and executes them.
def handleTurn(game, action_buffer):
    action_buffer.sort(lambda a, b: a.priority - b.priority, reverse=True)  # TODO: test this function
    for action in action_buffer:
        game.msg_buffer[action.owner].append(executeAction(game, action))
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
# @param parameters TODO
# @param client_id TODO
def bufferAction(actionBuffer, action, parameters, client_id):
    action = objects.client_action.Action(action, parameters, client_id)
    actionBuffer.append(action)


## Attempts to execute the given action. If it is invalid, a 404 response is returned.
# @param game TODO The current game state?
# @param action The action to execute
# @returns An actionDispatch object indicating (TODO - indicating what?) if the action is successful, a 404 "Invalid Call" response otherwise
def executeAction(game, action):
    if action.action in actionDispatch:
        return actionDispatch[action.action](game, action.parameters)
    else:
        return response(404, message="invalid call")


## Attempts to move a player. If the move is invalid, a 404 "Invalid Call" response is returned.
# @param action The action to execute
def _movePlayer(game, parameters):
    if 'room' in parameters and 'player' in parameters:
        return game.people[parameters['player']].move(parameters['room'])
    else:
        return _INVALID
    # return _TODO
actionDispatch['movePlayer'] = _movePlayer
actionPriorities['movePlayer'] = 80


## Attempts to eat food from FoodTable
# @param parameters TODO - Explain valid parameters
def _eatFood(game, parameters):
    if 'foodTable' in parameters and 'player' in parameters:
        return game.people[parameters['player']].eat(parameters['foodTable'])
    else:
        return _INVALID
    # return _TODO
actionDispatch['eatFood'] = _eatFood
actionPriorities['eatFood'] = 80


## Attempts to make a player sleep
# @param parameters TODO - Explain valid parameters
def _sleep(game, parameters):
    if 'player' in parameters and 'hours' in parameters:
        return game.people[parameters['player']].sleep(parameters['hours'])
    else:
        return _INVALID

    # return _TODO
actionDispatch['sleep'] = _sleep
actionPriorities['sleep'] = 60


## Attempts to make a player code
# @param parameters Should include the player to code and the type of coding to do
def _code(game, parameters):
    if 'player' in parameters and 'type' in parameters and
        'duration' in parameters:
        return game.people[parameters['player']].code(parameters['type'], game.turn)
    else:
        return _INVALID
actionDispatch['code'] = _code
actionPriorities['code'] = 60


## Returns information about the server
# @param parameters TODO - Explain valid parameters.
def _serverInfo(game, parameters):
    """Returns information about the server
    """
    constants = config.handle_constants.retrieveConstants('generalInfo')
    return response(200, version=constants["VERSION"], name=constants["NAME"])
actionDispatch['serverInfo'] = _serverInfo
actionPriorities['serverInfo'] = 100

objects.client_action.Action.actions = actionDispatch
objects.client_action.Action.priorities = actionPriorities


class TestaActionHandler(unittest.TestCase):
    # Test cases for Action Handler

    ## Sets up variables required by each test case
    def setUp(self):
        pass

    ## Test that the response() function formats the response correctly.
    def testResponse(self):
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
        validActions = config.handle_constants.retrieveConstants("actions")
        pseudoBuffer = []
        pseudoAction = validActions[0]
        bufferAction(pseudoBuffer, pseudoAction, {"target": 'pseudoTarget'}, 0)
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
    # Run all of the test cases in this file
    unittest.main()
