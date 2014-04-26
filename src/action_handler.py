## actionHandler Handles the client's actions sent to the engine from the server.

import config.handle_constants
import objects.client_action
import unittest


## Takes in a list of json actions taken by all of the clients and executes them.
# @param game
#   ?
# @param action_buffer
#   ?
def handleTurn(game, action_buffer):

    sortActions(action_buffer)
    for action in action_buffer:
        game.result_buffer[action.owner].append(executeAction(game, action))
    return


## Sort the actions in the action buffer by their priority.
# @param actionBuffer
#   The buffered list of actions to sort.
def sortActions(actionBuffer):
    # TODO
    # sort the actions in actionBuffer by priority, see the python
    # built-in sort function
    actionBuffer.sort(lambda a, b: a.priority - b.priority, reverse=True)
    return


## Adds the action to a buffered list of actions so that it can be executed later.
# @param actionBuffer
#   The buffered list of actions to add the action to
# @param action
#   The action to add to the actionBuffer
# @param parameters
#   TODO
# @param client_id
#   TODO
def bufferAction(actionBuffer, action, parameters, client_id):
    action = objects.client_action.Action(action, parameters, client_id)
    actionBuffer.append(action)


## Attempts to execute the given action. If it is invalid, a 404 response is returned.
# @param game
#   TODO The current game state?
# @param action
#   The action to execute
# @returns
#   An actionDispatch object indicating (TODO - indicating what?) if the action is successful, a 404 "Invalid Call" response otherwise
def executeAction(game, action):
    return action.execute(game)


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
        validActions = config.handle_constants.retrieveConstants("actions")['validActions']
        pseudoBuffer = []
        pseudoAction = validActions[0]
        bufferAction(pseudoBuffer, pseudoAction, {"target": 'pseudoTarget'}, 0)
        self.assertFalse(not pseudoBuffer)
        self.assertEquals(pseudoBuffer[0].action, validActions[0])

    ## Tests that the executeAction() function correctly executes the action given a valid action.
    def testExecuteActionExists(self):
        self.assertTrue(False)

    ## Tests that the executeAction() function correctly responds given an invalid action.
    def testExecuteActionNotExists(self):
        self.assertTrue(False)

    ## Test that handleTurn returns the correct list of responses.
    def testHandleTurn(self):
        self.assertTrue(True)

if __name__ == "__main__":
    # Run all of the test cases in this file
    unittest.main()
