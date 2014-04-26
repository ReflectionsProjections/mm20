import config.handle_constants
import unittest


## The type of error occuring due to any client initiated action
class ActionError(Exception):
    def __init__(self, reason, message):
        self.reason = reason
        self.message = message

    def __str__(self):
        return "{0} ({1})".format(self.reason, self.message)


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

    ## Attempts to move a member. If the move is invalid, a 404 "Invalid Call" response is returned.
    # @param action
    #   The action to execute
    def _move(self, game, parameters):
        response = self._build_response(game, parameters, ['member', 'room'], "moving")
        if response['success'] is True:
            try:
                game.people[parameters['member']].move(game.rooms[parameters['room']])
            except ActionError as e:
                response['success'] = False
                response['reason'] = e[0]
                response['message'] = e[1]
            except KeyError as e:
                response['success'] = False
                response['reason'] = 'KEYERROR'
                response['message'] = 'Room does not exist'
        return response

    ## Attempts to eat food from FoodTable
    # @param parameters
    #   TODO - Explain valid parameters
    def _eat(self, game, parameters):
        response = self._build_response(game, parameters, ['member', 'foodTable'], "eating")
        if response['success'] is True:
            try:
                game.people[parameters['member']].eat(parameters['foodTable'])
            except ActionError as e:
                response['success'] = False
                response['reason'] = e.reason
                response['message'] = e.message
        return response

    ## Attempts to make a member sleep
    # @param parameters
    #   TODO - Explain valid parameters
    def _sleep(self, game, parameters):
        response = self._build_response(game, parameters, ['member'], "sleeping")
        if response['success'] is True:
            try:
                game.people[parameters['member']].sleep()
            except ActionError as e:
                response['success'] = False
                response['reason'] = e[0]
                response['message'] = e[1]
        return response

    ## Attempts to make a member code
    # @param parameters
    #   TODO - Explain valid parameters
    def _code(self, game, parameters):
        response = self._build_response(game, parameters, ['member', 'type'], "coding")
        if response['success'] is True:
            try:
                game.people[parameters['member']].code(parameters['type'], game.turn)
            except ActionError as e:
                response['success'] = False
                response['reason'] = e[0]
                response['message'] = e[1]
        return response

    ## Attempts to make a member theorize
    # @param parameters
    #   TODO - Explain valid parameters
    def _theorize(self, game, parameters):
        response = self._build_response(game, parameters, ['member'], "theorizing")
        if response['success'] is True:
            try:
                game.people[parameters['member']].theorize(game.turn)
            except ActionError as e:
                response['success'] = False
                response['reason'] = e.reason
                response['message'] = e.message
        return response

    ## Attempts to make a member theorize
    # @param parameters
    #   TODO - Explain valid parameters
    def _distract(self, game, parameters):
        response = self._build_response(game, parameters, ['member', 'victim'], "distracting")
        if response['success'] is True:
            try:
                game.people[parameters['member']].theorize(game.people[parameters['victim']])
            except ActionError as e:
                response['success'] = False
                response['reason'] = e.reason
                response['message'] = e.message
        return response

    ## Attempts to make a member theorize
    # @param parameters
    #   TODO - Explain valid parameters
    def _wake(self, game, parameters):
        response = self._build_response(game, parameters, ['member', 'victim'], "distracting")
        if response['success'] is True:
            try:
                game.people[parameters['member']].wake(game.people[parameters['victim']])
            except ActionError as e:
                response['success'] = False
                response['reason'] = e.reason
                response['message'] = e.message
        return response

    ## Attempts to make a member theorize
    # @param parameters
    #   TODO - Explain valid parameters
    def _spy(self, game, parameters):
        response = self._build_response(game, parameters, ['member'], "distracting")
        if response['success'] is True:
            try:
                game.people[parameters['member']].theorize()
            except ActionError as e:
                response['success'] = False
                response['reason'] = e.reason
                response['message'] = e.message
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
        if 'member' in parameters:
            if not isinstance(parameters['member'], int) or parameters['member'] > len(game.people):
                response['success'] = False
                response['message'] = "KeyError: {0} not a valid member".format(parameters['member'])
                response['reason'] = 'KEYERROR'
            elif game.people[parameters['member']].team.my_id != self.owner:
                response['success'] = False
                response['message'] = "{0} is not a member of your team".format(parameters['member'])
                response['reason'] = 'NOTTEAMMEMBER'

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
