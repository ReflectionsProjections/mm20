from config.handle_constants import retrieveConstants
from unittest import TestCase, main


class Action:
    actions = {}

    def __init__(self, action, *args, **kwargs):
        if not action in Action.actions:
            raise KeyError("Action not defined")
        self.action = action
        self.args = args
        self.kwargs = kwargs
        self.key = self.kwargs['target']

Action.actions = retrieveConstants("actions")


class TestaClientActions(TestCase):
    def testUnavailableAction(self):
        self.assertRaises(KeyError, Action, 'notDefined', {'move': 'banjos'})

if __name__ == "__main__":
    main()
