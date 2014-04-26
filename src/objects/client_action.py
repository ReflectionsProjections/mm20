import config.handle_constants
import unittest


## ??
class Action:
    ## ??
    # @parameter action
    #   ??
    # @parameter parameters
    #   ??
    # @parameter client_id
    #   ??
    def __init__(self, action, parameters, client_id):
        actions_data = config.handle_constants.retrieveConstants('actions')
        self.action = action
        if not action in actions_data['validActions']:
            self.action = "INVALID"
        self.priority = actions_data['priorities'][action]
        self.parameters = parameters
        self.owner = client_id

    ## Executes the action
    def execute(self, game):
        invalid = {'success': False, 'message': 'Invalid action',
                   'reason': 'INVALID'}
        if self.action == 'INVALID':
            return invalid
        try:
            func = getattr(Action, '_{0}'.format(self.action))
            return func(game, self.parameters)
        except AttributeError:
            return invalid

    # --- Actions available to clients ---

    ## Attempts to move a player. If the move is invalid, a 404 "Invalid Call" response is returned.
    # @param action
    #   The action to execute
    def _movePlayer(game, parameters):
        response = {'action': 'move'}
        try:
            response = {'success': True, 'message': '', 'reason': '',
                        'member': parameters['player'], 'room': parameters['room']}
        except KeyError as e:
            response.success = False
            response.message = "KeyError: {0} not found in parameters".format(e)
            response.reason = 'KEYERROR'
            return response
        try:
            game.people[parameters['player']].move(parameters['room'])
        except Exception as e:
            response.success = False
            response.message = "{0}".format(e.args[1])
            response.reason = e.args[0]
        else:
            response.success = True
            response.message = "Member {0} moved to {1}".format(parameters['player'], parameters['room'])
            response.reason = 'SUCCESS'
        return response

    ## Attempts to eat food from FoodTable
    # @param parameters
    #   TODO - Explain valid parameters
    def _eatFood(game, parameters):
        response = {'action': 'eatFood'}
        try:
            response = {'success': True, 'message': '', 'reason': '',
                        'member': parameters['player'], 'foodTable': parameters['foodTable']}
        except KeyError as e:
            response.success = False
            response.message = "KeyError: {0} not found in parameters".format(e)
            response.reason = 'KEYERROR'
            return response
        try:
            game.people[parameters['player']].eat(parameters['foodTable'])
        except Exception as e:
            response.success = False
            response.message = "{0}".format(e.args[1])
            response.reason = e.args[0]
        else:
            response.success = True
            response.message = "Member {0} ate food from {1}".format(parameters['player'], parameters['foodTable'])
            response.reason = 'SUCCESS'
        return response

    ## Attempts to make a player sleep
    # @param parameters
    #   TODO - Explain valid parameters
    def _sleep(game, parameters):
        response = {'action': 'sleep'}
        try:
            response = {'success': True, 'message': '', 'reason': '',
                        'member': parameters['player']}
        except KeyError as e:
            response.success = False
            response.message = "KeyError: {0} not found in parameters".format(e)
            response.reason = 'KEYERROR'
            return response
        try:
            game.people[parameters['player']].sleep()
        except Exception as e:
            response.success = False
            response.message = "{0}".format(e.args[1])
            response.reason = e.args[0]
        else:
            response.success = True
            response.message = "Member {0} went to sleep".format(parameters['player'])
            response.reason = 'SUCCESS'
        return response

    ## Attempts to make a player code
    # @param parameters
    #   TODO - Explain valid parameters
    def _code(game, parameters):
        response = {'action': 'code'}
        try:
            response = {'success': True, 'message': '', 'reason': '',
                        'member': parameters['player'], 'attribute': parameters['attribute']}
        except KeyError as e:
            response.success = False
            response.message = "KeyError: {0} not found in parameters".format(e)
            response.reason = 'KEYERROR'
            return response
        try:
            game.people[parameters['player']].code(parameters['attribute'])
        except Exception as e:
            response.success = False
            response.message = "{0}".format(e.args[1])
            response.reason = e.args[0]
        else:
            response.success = True
            response.message = "Member {0} is coding {1}".format(parameters['player'], parameters['attribute'])
            response.reason = 'SUCCESS'
        return response

    ## Returns information about the server
    # @param parameters
    #   TODO - Explain valid parameters.
    def _serverInfo(game, parameters):
        """Returns information about the server
        """
        constants = config.handle_constants.retrieveConstants('generalInfo')
        response = {'action': 'getInfo', 'success': True, 'message': 'Information Retrieved',
                    'reason': 'SUCCESS', 'version': constants["VERSION"],
                    'name': constants["NAME"]}
        return response


class TestaClientActions(unittest.TestCase):
    def testUnavailableAction(self):
        Action.actions = {}
        with self.assertRaises(KeyError):
            Action('move', {'team_member': 'banjos'}, 0)

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

if __name__ == "__main__":
    unittest.main()
