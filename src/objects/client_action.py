#from config.handle_constants import retrieveConstants
from unittest import TestCase, main


class Action:
    actions = None # TODO This should be initialzed to actionDispatch

    def __init__(self, action, parameters, playerID):
        if not action in Action.actions:
            raise KeyError("Action not defined")
        self.action = action
        self.parameters = parameters
        self.key = self.parameters['target']
        #what is key used for?
        self.owner = playerID
        self.priority = 30
        #TODO find a good way to set the priority

#Action.actions = retrieveConstants("actions")


class TestaClientActions(TestCase):
    def testUnavailableAction(self):
        Action.actions = {}
        self.assertRaises(KeyError, Action,'move', {'team_member': 'banjos'}, 0)

if __name__ == "__main__":
    main()
