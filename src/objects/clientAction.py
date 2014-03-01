from config.handleConstants import retrieveConstants
from unittest import TestCase, main
#from exception import KeyError


class Action:
    actions = {}

    def __init__(self, action, *args, **kwargs):
        if not action in Action.actions:
            raise KeyError("Action not defined")
        self.action = action
        self.args = args
        self.kwargs = kwargs
        self.key = self.kwargs.target

Action.actions = retrieveConstants("actions")


class TestaActions(TestCase):
    def testReadFile(self):
        # Asserts that the retrieveConstants function does not fail via an error
        constants = retrieveConstants('aiDefaults')
        self.assertIsNotNone(constants)

    def testReturnNoneOnInvalidKey(self):
        constants = retrieveConstants('ThisIsNotAValidKey')
        self.assertIsNone(constants)

if __name__ == "__main__":
    main()
