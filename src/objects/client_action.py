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
        self.reason = ""
        if not action in actions_data['validActions']:
            self.action = "INVALID"
            self.priority = 0
            self.reason = "Invalid action"
        else:
            self.priority = actions_data['priorities'][action]
        self.parameters = parameters
        self.owner = client_id
        if not "person_id" in parameters:
            self.action = "INVALID"
            self.priority = 0
            self.reason = "Did not specify who is performing this action"
            self.person_id = -1
        else:
            self.person_id = parameters["person_id"]

    ## Executes this action
    # @parameter game
    #   The game state
    def execute(self, game):
        if self.person_id != -1 and game != None:
            person = game.people[self.person_id]
            try:
                person.location.sitDown(person)
            except client_action.ActionError:
                pass # Should never happen
        invalid = {'success': False, 'message': self.reason,
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
    # @param person_id
    #   The team member to move
    # @param room
    #   The room to move the team member to
    # @return
    #   A response dictionary
    def move(self, game, parameters):
        response = self._build_response(game, parameters, ['person_id', 'room'],
                                        "moving")
        if response['success'] is True:
            try:
                game.people[parameters['person_id']].move(game.rooms[
                    parameters['room']])
            except ActionError as e:
                response['success'] = False
                response['reason'] = e.reason
                response['message'] = e.message
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
    # @param person_id
    #   The team member that will eat food
    def eat(self, game, parameters):
        response = self._build_response(game, parameters, ['person_id'], "eating")
        if response['success'] is True:
            try:
                game.people[parameters['person_id']].eat()
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
    # @param person_id
    #   The team member which should fall asleep
    def sleep(self, game, parameters):
        response = self._build_response(game, parameters, ['person_id'],
                                        "sleeping")
        if response['success'] is True:
            try:
                game.people[parameters['person_id']].sleep()
            except ActionError as e:
                response['success'] = False
                response['reason'] = e.reason
                response['message'] = e.message
        return response

    ## Have a team member code
    # @param game
    #   The game state
    # @param parameters
    #   The parameters necessary to tell a team member to code
    #   (See the next two parameters)
    # @param person_id
    #   The team member which should code
    # @param type
    #   The type of coding the team member should perform
    #   (refactor, test, implement, or optimize)
    def code(self, game, parameters):
        response = self._build_response(game, parameters, ['person_id', 'type'],
                                        "coding")
        if response['success'] is True:
            try:
                game.people[parameters['person_id']].code(parameters['type'],
                                                       game.turn)
            except ActionError as e:
                response['success'] = False
                response['reason'] = e.reason
                response['message'] = e.message
        return response

    ## Have a member develop theory for that teams AI
    # @param game
    #   The game state
    # @param parameters
    #   The parameters necessary to have a team member theorize
    #   (See the next parameter)
    # @param person_id
    #   The member to tell to theorize
    def theorize(self, game, parameters):
        response = self._build_response(game, parameters, ['person_id'],
                                        "theorizing")
        if response['success'] is True:
            try:
                game.people[parameters['person_id']].theorize(game.turn)
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
    # @param person_id
    #   Your team member distracting another person
    # @param victim
    #   The person your team member is distracting
    def distract(self, game, parameters):
        response = self._build_response(game, parameters, ['person_id', 'victim'],
                                        "distracting")
        if response['success'] is True:
            try:
                game.people[parameters['person_id']].distract(game.people[
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
    # @param person_id
    #   Your team member waking up another person
    # @param victim
    #   The person being awoken
    def wake(self, game, parameters):
        response = self._build_response(game, parameters, ['person_id', 'victim'],
                                        "waking")
        if response['success'] is True:
            try:
                game.people[parameters['person_id']].wake(game.people[
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
    # @param person_id
    #   The team member which will be doing the spying
    def spy(self, game, parameters):
        response = self._build_response(game, parameters, ['person_id'],
                                        "spying")
        if response['success'] is True:
            try:
                game.people[parameters['person_id']].spy()
            except ActionError as e:
                response['success'] = False
                response['reason'] = e.reason
                response['message'] = e.message
        return response

    ## View the practice games to gain info on other teams
    # @param game
    #   The game state
    # @param parameters
    #   The parameters necessary to have your team member view the practice games
    #   (See the next parameter)
    # @param person_id
    #   The team member which will be doing the watching
    def view(self, game, parameters):
        response = self._build_response(game, parameters, ['person_id'],
                                        "viewing")
        if response['success'] is True:
            try:
                game.people[parameters['person_id']].view()
                message = {}
                for key, value in game.teams.iteritems():
                    message[key] = game.calc_score(key)
                response['message'] = message
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
            if 'person_id' in parameters:
                response['message'] = "{0} is "\
                    .format(
                        game.people[parameters['person_id']].name) + message
            else:
                response['message'] = message
        if 'person_id' in parameters:
            if not isinstance(parameters['person_id'], int)\
                    or parameters['person_id'] > len(game.people):
                response['success'] = False
                response['message'] =\
                    "KeyError: {0} not a valid team member id"\
                    .format(parameters['person_id'])
                response['reason'] = 'KEYERROR'
            elif game.people[parameters['person_id']].team.my_id != self.owner:
                response['success'] = False
                response['message'] = "{0} is not a member of your team"\
                    .format(game.people[parameters['person_id']].name)
                response['reason'] = 'NOTTEAMMEMBER'

        return response


class TestClientActions(unittest.TestCase):
    def testUnavailableAction(self):
        Action.actions = {}
        test = Action('Not-An-Action', {'team_member': 'banjos', 'person_id': 3}, 0)
        result = test.execute(None)
        self.assertFalse(result['success'])
        self.assertEqual(result['reason'], 'INVALID')

    ## Tests that the _movePlayer function returns the same thing as
    #  the player.move function given valid parameters.
    @unittest.skip("Not yet implemented")
    def test_movePlayerValid(self):
        self.assertTrue(False)

    ## Tests that the _movePlayer function returns _INVALID
    #  given invalid parameters.
    @unittest.skip("Not yet implemented")
    def test_movePlayerInvalid(self):
        self.assertTrue(False)

    ## Tests that the _eatFood function returns the same thing as
    #  the player.eat function given valid parameters.
    @unittest.skip("Not yet implemented")
    def test_eatFoodValid(self):
        self.assertTrue(False)

    ## Tests that the _eatFood function returns _INVALID
    #  given invalid parameters.
    @unittest.skip("Not yet implemented")
    def test_eatFoodInvalid(self):
        self.assertTrue(False)

    ## Tests that the _sleep function returns the same thing as
    #  the player.sleep function given valid parameters.
    @unittest.skip("Not yet implemented")
    def test_sleepValid(self):
        self.assertTrue(False)

    ## Tests that the _sleep function returns _INVALID given invalid parameters
    @unittest.skip("Not yet implemented")
    def test_sleepInvalid(self):
        self.assertTrue(False)

    ## Tests that the _code function returns the same thing as
    #  the player.code function given valid parameters.
    @unittest.skip("Not yet implemented")
    def test_codeValid(self):
        self.assertTrue(False)

    ## Tests that the _code function returns _INVALID given invalid parameters
    @unittest.skip("Not yet implemented")
    def test_codeInvalid(self):
        self.assertTrue(False)

    ## Tests that the _getMap function returns the same thing as
    #  the loggers mapToJson function
    @unittest.skip("Not yet implemented")
    def test_getMap(self):
        self.assertTrue(False)

    ## Tests that the _serverInfo function returns correct
    #  information on the server from constants.json
    @unittest.skip("Not yet implemented")
    def test_serverInfo(self):
        self.assertTrue(False)

if __name__ == "__main__":
    unittest.main()
