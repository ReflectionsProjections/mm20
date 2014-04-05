#from config.handle_constants import retrieveConstants
from unittest import TestCase, main


class Action:
    actions = None # This is initialzed to actionDispatch in action_handler
    priorities = None

    def __init__(self, action, parameters, client_id):
        if not action in Action.actions:
            raise KeyError("Action not defined")
        self.action = action
        self.parameters = parameters
        self.key = self.parameters['target']
        #what is key used for?
        self.owner = client_id
        self.priority = Action.priorities[action]

#Action.actions = retrieveConstants("actions")


class TestaClientActions(TestCase):
    def testUnavailableAction(self):
        Action.actions = {}
        self.assertRaises(KeyError, Action,'move', {'team_member': 'banjos'}, 0)

if __name__ == "__main__":
    main()
