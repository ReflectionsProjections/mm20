## Handles the client's actions sent to the engine from the server.

import config.handle_constants
import objects.client_action
import unittest


## Executes all of the actions queued up by the clients
# @param game
#   The gamestate
# @param action_buffer
#   A buffer (list) of all of the actions to be performed this turn
def handleTurn(game, action_buffer):
    sortActions(action_buffer)
    for action in action_buffer:
        game.result_buffer[action.owner].append(action.execute(game))
    return


## Sorts the actions in the action buffer by their priority.
# @param actionBuffer
#   A buffer (list) of actions
def sortActions(actionBuffer):
    # TODO
    # sort the actions in actionBuffer by priority, see the python
    # built-in sort function
    actionBuffer.sort(sortFunction, reverse=True)
    return

## Compare two actions and return >0 if a has higher priority,
#  return <0 if b has higher priority (higher means faster)
# @param a
#   The action to compare with b
# @param b
#   The action to compare with a
def sortFunction(a, b):
    return a.priority - b.priority


## Adds the action to a buffered list of actions that will be
#  executed this turn
# @param actionBuffer
#   The buffer (list) of actions the action will be added to
# @param action
#   The action (string) to buffer
# @param parameters
#   The parameters for said action
# @param client_id
#   The client which sent this action to the server
def bufferAction(actionBuffer, action, parameters, client_id):
    action = objects.client_action.Action(action, parameters, client_id)
    actionBuffer.append(action)


class TestaActionHandler(unittest.TestCase):
    ## Sets up variables required by each test case
    def setUp(self):
        pass

    ## Test that the response() function formats the response correctly.
    @unittest.skip("Not yet implemented")
    def testResponse(self):
        self.assertTrue(False)

    ## Test that the sortActions() function correctly sorts the actions.
    def testSortAction(self):
        act1 = objects.client_action.Action("spy", None, 0)
        act2 = objects.client_action.Action("wake", None, 0)
        act3 = objects.client_action.Action("eat", None, 0)
        act1.priority = 0
        act2.priority = 50
        act3.priority = 100
        pseudoBuffer = [act1, act2, act3]
        sortActions(pseudoBuffer)
        self.assertEquals(pseudoBuffer[0], act3)
        self.assertEquals(pseudoBuffer[1], act2)
        self.assertEquals(pseudoBuffer[2], act1)

    ## Tests that the bufferAction function correctly adds
    #  an action to the buffer.
    def testBufferAction(self):
        validActions = config.handle_constants.retrieveConstants("actions")[
            'validActions']
        pseudoBuffer = []
        pseudoAction = validActions[0]
        bufferAction(pseudoBuffer, pseudoAction, {"target": 'pseudoTarget'}, 0)
        self.assertFalse(not pseudoBuffer)
        self.assertEquals(pseudoBuffer[0].action, validActions[0])

    ## Tests that the executeAction() function correctly executes
    #  the action given a valid action.
    @unittest.skip("Not yet implemented")
    def testExecuteActionExists(self):
        self.assertTrue(False)

    ## Tests that the executeAction() function correctly
    #  responds given an invalid action.
    @unittest.skip("Not yet implemented")
    def testExecuteActionNotExists(self):
        self.assertTrue(False)

    ## Test that handleTurn returns the correct list of responses.
    @unittest.skip("Not yet implemented")
    def testHandleTurn(self):
        self.assertTrue(True)

if __name__ == "__main__":
    # Run all of the test cases in this file
    unittest.main()
