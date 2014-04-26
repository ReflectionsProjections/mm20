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
        func = getattr(self, '_{0}'.format(self.action))
        return func(game, self.parameters)

    # --- Actions available to clients ---

    ## Attempts to move a player. If the move is invalid, a 404 "Invalid Call" response is returned.
    # @param action
    #   The action to execute
    def _movePlayer(self, game, parameters):
        response = self._build_response(game, parameters, ['member', 'room'], "moving")
        if response['success'] == True:
            game.people[parameters['player']].move(parameters['room'])
        return response

    ## Attempts to eat food from FoodTable
    # @param parameters
    #   TODO - Explain valid parameters
    def _eatFood(self, game, parameters):
        response = self._build_response(game, parameters, ['member', 'foodTable'], "eating")
        if response['success'] == True:
            game.people[parameters['player']].eat(parameters['foodTable'])
        return response

    ## Attempts to make a player sleep
    # @param parameters
    #   TODO - Explain valid parameters
    def _sleep(self, game, parameters):
        response = self._build_response(game, parameters, ['member'], "sleeping")
        if response['success'] == True:
            game.people[parameters['member']].sleep()
        return response

    ## Attempts to make a player code
    # @param parameters
    #   TODO - Explain valid parameters
    def _code(self, game, parameters):
        response = self._build_response(game, parameters, ['member', 'type'], "coding")
        if response['success'] == True:
            game.people[parameters['member']].code(parameters['type'], game.turn)
        return response

    ## Attempts to make a player theorize
    # @param parameters
    #   TODO - Explain valid parameters
    def _theorize(self, game, parameters):
        response = self._build_response(game, parameters, ['member'], "theorizing")
        if response['success'] == True:
            game.people[parameters['member']].theorize(game.turn)
        return response

    ## Returns information about the server
    # @param parameters
    #   TODO - Explain valid parameters.
    def _serverInfo(self, game, parameters):
        """Returns information about the server
        """
        constants = config.handle_constants.retrieveConstants('generalInfo')
        response = {'action': 'getInfo', 'success': True, 'message': 'Information Retrieved',
                    'reason': 'SUCCESS', 'version': constants["VERSION"],
                    'name': constants["NAME"]}
        return response

    def _build_response(self, game, parameters, expected_params, message):
        response = {}
        response['action'] = parameters['action']
        try:
            response['success'] = True
            response['message'] = ''
            for par in expected_params:
                response[par] = parameters[par]
        except KeyError as e:
            response['success'] = False
            response['message'] = "KeyError: {0} not found in parameters".format(e)
            response['reason'] = 'KEYERROR'
            return response
        else:
            response['reason'] = 'SUCCESS'
            if 'member' in parameters:
                response['message'] = "Member {0} is ".format(parameters['member']) + message
            else:
                response['message'] = message
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
