import config.handle_constants
import unittest


## Raised when an error occurs due to something the client did
class ActionError(Exception):
    def __init__(self, reason, message):
        self.reason = reason
        self.message = message

    def __str__(self):
        return "{0} ({1})".format(self.reason, self.message)


## This class holds a client's action and all of the functionality
#  necessary to execute it.
class Action:
    ## Initializes an action.
    # @parameter action
    #   A string with the action the client wishes to perform
    # @parameter parameters
    #   All of the parameters needed by that action (see confluence or below
    #   for formats)
    # @parameter client_id
    #   The id of the client which sent this action to the server
    def __init__(self, action, parameters, client_id):
        actions_data = config.handle_constants.retrieveConstants('actions')
        self.action = action
        if not action in actions_data['validActions']:
            self.action = "INVALID"
        self.priority = actions_data['priorities'][action]
        self.parameters = parameters
        self.owner = client_id

    ## Executes this action
    # @parameter game
    #   The game state
    def execute(self, game):
        invalid = {'success': False, 'message': 'Invalid action',
                   'reason': 'INVALID'}
        if self.action == 'INVALID':
            return invalid
        func = getattr(self, self.action)
        return func(game, self.parameters)

    # --- Actions available to clients ---

    ## Move a team member from the room they are currently in
    #  to another.
    # @param game
    #   The game state
    # @param parameters
    #   The parameters needed to move a member
    #   (See the next two parameters)
    # @param member
    #   The team member to move
    # @param room
    #   The room to move the team member to
    # @return
    #   A response dictionary
    def move(self, game, parameters):
        response = self._build_response(game, parameters, ['member', 'room'],
                                        "moving")
        if response['success'] is True:
            try:
                game.people[parameters['member']].move(game.rooms[
                    parameters['room']])
            except ActionError as e:
                response['success'] = False
                response['reason'] = e[0]
                response['message'] = e[1]
            except KeyError as e:
                response['success'] = False
                response['reason'] = 'KEYERROR'
                response['message'] = 'Room does not exist'
        return response

    ## Have the team member eat food
    # @param game
    #   The game state
    # @param parameters
    #   The parameters necessary to tell a team member to eat food
    #   (See the next parameter)
    # @param member
    #   The team member that will eat food
    def eat(self, game, parameters):
        response = self._build_response(game, parameters, ['member'], "eating")
        if response['success'] is True:
            try:
                game.people[parameters['member']].eat()
            except ActionError as e:
                response['success'] = False
                response['reason'] = e.reason
                response['message'] = e.message
        return response

    ## Have a team member fall asleep
    # @param game
    #   The game state
    # @param parameters
    #   The parameters necessary to tell a team member to fall asleep
    #   (See the next parameter)
    # @param member
    #   The team member which should fall asleep
    def sleep(self, game, parameters):
        response = self._build_response(game, parameters, ['member'],
                                        "sleeping")
        if response['success'] is True:
            try:
                game.people[parameters['member']].sleep()
            except ActionError as e:
                response['success'] = False
                response['reason'] = e[0]
                response['message'] = e[1]
        return response

    ## Have a team member code
    # @param game
    #   The game state
    # @param parameters
    #   The parameters necessary to tell a team member to code
    #   (See the next two parameters)
    # @param member
    #   The team member which should code
    # @param type
    #   The type of coding the team member should perform
    #   (refactor, test, implement, or optimize)
    def code(self, game, parameters):
        response = self._build_response(game, parameters, ['member', 'type'],
                                        "coding")
        if response['success'] is True:
            try:
                game.people[parameters['member']].code(parameters['type'],
                                                       game.turn)
            except ActionError as e:
                response['success'] = False
                response['reason'] = e[0]
                response['message'] = e[1]
        return response

    ## Have a member develop theory for that teams AI
    # @param game
    #   The game state
    # @param parameters
    #   The parameters necessary to have a team member theorize
    #   (See the next parameter)
    # @param member
    #   The member to tell to theorize
    def theorize(self, game, parameters):
        response = self._build_response(game, parameters, ['member'],
                                        "theorizing")
        if response['success'] is True:
            try:
                game.people[parameters['member']].theorize(game.turn)
            except ActionError as e:
                response['success'] = False
                response['reason'] = e.reason
                response['message'] = e.message
        return response

    ## Get one of your team members to distract any other person
    #  (including your own team members, albeit this is not
    #   a recommended strategy)
    # @param game
    #   The game state
    # @param parameters
    #   The parameters necessary to have your team member distract
    #   another person
    #   (See the next two parameters)
    # @param member
    #   Your team member distracting another person
    # @param victim
    #   The person your team member is distracting
    def distract(self, game, parameters):
        response = self._build_response(game, parameters, ['member', 'victim'],
                                        "distracting")
        if response['success'] is True:
            try:
                game.people[parameters['member']].theorize(game.people[
                    parameters['victim']])
            except ActionError as e:
                response['success'] = False
                response['reason'] = e.reason
                response['message'] = e.message
        return response

    ## Have a team member wake up any other person
    # @param game
    #   The game state
    # @param parameters
    #   The parameters necessary to have a team member to wake up a person
    #   (See the next two parameters)
    # @param member
    #   Your team member waking up another person
    # @param victim
    #   The person being awoken
    def wake(self, game, parameters):
        response = self._build_response(game, parameters, ['member', 'victim'],
                                        "waking")
        if response['success'] is True:
            try:
                game.people[parameters['member']].wake(game.people[
                    parameters['victim']])
            except ActionError as e:
                response['success'] = False
                response['reason'] = e.reason
                response['message'] = e.message
        return response

    ## Have a team member spy on people from other teams (in the same room)
    # @param game
    #   The game state
    # @param parameters
    #   The parameters necessary to have your team member spy on others
    #   (See the next parameter)
    # @param member
    #   The team member which will be doing the spying
    def spy(self, game, parameters):
        response = self._build_response(game, parameters, ['member'], "spying")
        if response['success'] is True:
            try:
                game.people[parameters['member']].theorize()
            except ActionError as e:
                response['success'] = False
                response['reason'] = e.reason
                response['message'] = e.message
        return response

    ## Returns information about the server
    # @param game
    #   The game state
    # @param parameters
    #   This parameter is ignored
    # @param return
    #   Information on the server
    def serverInfo(self, game, parameters=None):
        constants = config.handle_constants.retrieveConstants('generalInfo')
        response = {'action': 'getInfo', 'success': True,
                    'message': 'Information Retrieved',
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
            response['message'] = "KeyError: {0} not found in parameters"\
                .format(e)
            response['reason'] = 'KEYERROR'
            return response
        else:
            response['reason'] = 'SUCCESS'
            if 'member' in parameters:
                response['message'] = "Member {0} is "\
                    .format(parameters['member']) + message
            else:
                response['message'] = message
        if 'member' in parameters:
            if not isinstance(parameters['member'], int)\
                    or parameters['member'] > len(game.people):
                response['success'] = False
                response['message'] = "KeyError: {0} not a valid member"\
                    .format(parameters['member'])
                response['reason'] = 'KEYERROR'
            elif game.people[parameters['member']].team.my_id != self.owner:
                response['success'] = False
                response['message'] = "{0} is not a member of your team"\
                    .format(parameters['member'])
                response['reason'] = 'NOTTEAMMEMBER'

        return response


class TestaClientActions(unittest.TestCase):
    def testUnavailableAction(self):
        Action.actions = {}
        with self.assertRaises(KeyError):
            Action('move', {'team_member': 'banjos'}, 0)

    ## Tests that the _movePlayer function returns the same thing as
    #  the player.move function given valid parameters.
    def test_movePlayerValid(self):
        self.assertTrue(False)

    ## Tests that the _movePlayer function returns _INVALID
    #  given invalid parameters.
    def test_movePlayerInvalid(self):
        self.assertTrue(False)

    ## Tests that the _eatFood function returns the same thing as
    #  the player.eat function given valid parameters.
    def test_eatFoodValid(self):
        self.assertTrue(False)

    ## Tests that the _eatFood function returns _INVALID
    #  given invalid parameters.
    def test_eatFoodInvalid(self):
        self.assertTrue(False)

    ## Tests that the _sleep function returns the same thing as
    #  the player.sleep function given valid parameters.
    def test_sleepValid(self):
        self.assertTrue(False)

    ## Tests that the _sleep function returns _INVALID given invalid parameters
    def test_sleepInvalid(self):
        self.assertTrue(False)

    ## Tests that the _code function returns the same thing as
    #  the player.code function given valid parameters.
    def test_codeValid(self):
        self.assertTrue(False)

    ## Tests that the _code function returns _INVALID given invalid parameters
    def test_codeInvalid(self):
        self.assertTrue(False)

    ## Tests that the _getMap function returns the same thing as
    #  the loggers mapToJson function
    def test_getMap(self):
        self.assertTrue(False)

    ## Tests that the _serverInfo function returns correct
    #  information on the server from constants.json
    def test_serverInfo(self):
        self.assertTrue(False)

if __name__ == "__main__":
    unittest.main()
