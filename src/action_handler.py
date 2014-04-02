"""@actionHandler Handles the client's actions sent to the engine from the server.
"""
from config.handle_constants import retrieveConstants
from objects.client_action import Action
from unittest import TestCase, main

actionDispatch = {}


def response(status_code, **kwargs):
    """Creates a response formatted to be understood by the server.
    """
    kwargs["status"] = status_code
    return kwargs

_TODO = response(500, message="not yet implemented")
_INVALID = response(404, message="invalid call")


def handleTurn(game, action_buffer):
    """Takes in the list of actions given from all of the clients.
    it sorts then and executes them by the given prioity.
    """
    
    action_buffer.sort(lambda a,b: a.priority - b.priority, reverse=True) #TODO: test this function
    for action in action_buffer:
        game.msg_buffer[action.playerID].append(executeAction(game, action))
    return



def bufferAction(actionBuffer, action, parameters, playerID):
    """Adds the action to a buffered list of actions so that it can be executed later.
    """
    action = Action(action, parameters, playerID)
    actionBuffer.append(action)


def executeAction(game, action):
    """Executes the given action.
    """
    if action.action in actionDispatch:
        return actionDispatch[action.key](game, action.parameters)
    else:
        return response(404, message="invalid call")


def _movePlayer(game, parameters):
    """Attempts to move a player from one room to another
    """
    if 'room' in parameters and 'player' in parameters:
        return game.people[parameters['player']].move(parameters['room'])
    else:
        return _INVALID
    # return _TODO
actionDispatch['movePlayer'] = _movePlayer


def _eatFood(game, parameters):
    """Attempts to have a player eat the food from FoodTable
    """
    if 'foodTable' in parameters and 'player' in parameters:
        return game.people[parameters['player']].eat(parameters['foodTable'])
    else:
        return _INVALID
    # return _TODO
actionDispatch['eatFood'] = _eatFood


def _sleep(game, parameters):
    """Attempts to tell a player to sleep
    """
    if 'player' in parameters and 'hours' in parameters:
        return game.people[parameters['player']].sleep(parameters['hours'])
    else:
        return _INVALID

    # return _TODO
actionDispatch['sleep'] = _sleep


def _code(game, parameters):
    """Attempts to tell a player to code
    """
    if 'player' in parameters and 'team' in parameters \
        and 'attribute' in parameters:
        return game.people[parameters['player']].code(
            parameters['team'], parameters['attribute'])
    else:
        return _INVALID
    # return _TODO
actionDispatch['code'] = _code


def _getMap(game, parameters):
    """Returns a json version of the current game maps
    """
    # This should be the same json interpretation that the logger uses.
    return _TODO
actionDispatch['getMap'] = _getMap


def _serverInfo(game, parameters):
    """Returns information about the server
    """
    constants = retrieveConstants('generalInfo')
    return response(200, version=constants.VERSION, name=constants.NAME)
actionDispatch['serverInfo'] = _serverInfo

Action.actions = actionDispatch


class TestaActionHandler(TestCase):
    """Holds the test cases to test the Action Handler
    """
    def setup(self):
        """Sets up the variables that will be needed by each test case
        """
        return

    def testRespone(self):
        """Test that the respone function formats the response correctly.
        """
        self.assertTrue(False)

    def testSortAction(self):
        """Test that the sortActions function correctly sorts the actions.
        """
        pseudoBuffer = [
            {'priority': 0, 'name': 'last'},
            {'priority': 10, 'name': 'first'},
            {'priority': 5, 'name': 'middle'}
        ]
        sortActions(pseudoBuffer)
        self.assertEquals(pseudoBuffer[0]['name'], 'first')
        self.assertEquals(pseudoBuffer[1]['name'], 'middle')
        self.assertEquals(pseudoBuffer[2]['name'], 'last')

    def testBufferAction(self):
        """Tests that the bufferAction function correctly adds an action to the buffer.
        """
        validActions = retrieveConstants("actions")
        pseudoBuffer = []
        pseudoAction = validActions[0]
        bufferAction(pseudoBuffer, pseudoAction, {"target":'pseudoTarget'}, 0)
        self.assertFalse(not pseudoBuffer)
        self.assertEquals(pseudoBuffer[0], validActions[0])

    def testExecuteActionExists(self):
        """Tests that the execeuteAction function correctly executes the function given a valid function
        """
        self.assertTrue(False)

    def testExecuteActionNotExists(self):
        """Tests that the executeAction function correctly respons given an invalid action
        """
        self.assertTrue(False)

    def test_movePlayerValid(self):
        """Tests that the _movePlayer function returns the same thing as the player.move function given valid parameters.
        """
        self.assertTrue(False)

    def test_movePlayerInvalid(self):
        """Tests that the _movePlayer function returns _INVALID given invalid parameters
        """
        self.assertTrue(False)

    def test_eatFoodValid(self):
        """Tests that the _eatFood function returns the same thing as the player.eat function given valid parameters.
        """
        self.assertTrue(False)

    def test_eatFoodInvalid(self):
        """Tests that the _eatFood function returns _INVALID given invalid parameters
        """
        self.assertTrue(False)

    def test_sleepValid(self):
        """Tests that the _sleep function returns the same thing as the player.sleep function given valid parameters.
        """
        self.assertTrue(False)

    def test_sleepInvalid(self):
        """Tests that the _sleep function returns _INVALID given invalid parameters
        """
        self.assertTrue(False)

    def test_codeValid(self):
        """Tests that the _code function returns the same thing as the player.code function given valid parameters.
        """
        self.assertTrue(False)

    def test_codeInvalid(self):
        """Tests that the _code function returns _INVALID given invalid parameters
        """
        self.assertTrue(False)

    def test_getMap(self):
        """Tests that the _getMap function returns the same thing as the loggers mapToJson function
        """
        self.assertTrue(False)

    def test_serverInfo(self):
        """Tests that the _serverInfo function returns correct information on the server from constants.json
        """
        self.assertTrue(False)

    def testHandleTurn(self):
        """Test that handleTurn returns the correct list of responses.
        """
        self.assertTrue(True)

if __name__ == "__main__":
    # Run all of the test cases
    main()
