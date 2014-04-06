import unittest
import json
import os

constantsLoaded = False
constants = {}

directory = os.path.dirname(__file__)


def retrieveConstants(key):
    global constants
    if constantsLoaded:
        try:
            return constants[key]
        except KeyError:
            return None
    try:
        with open(directory + '/' + 'constants.json', 'r') as constantsFile:
            jsonConstantsString = constantsFile.read()
        constants = json.loads(jsonConstantsString)
    except IOError as e:
        print "IOError: " + str(e)
    try:
        return constants[key]
    except KeyError:
        return None


class TestHandleConstants(unittest.TestCase):
    def testReadFile(self):
        # Asserts that the retrieveConstants function does not fail via an error
        constants = retrieveConstants('aiDefaults')
        self.assertIsNotNone(constants)

    def testReturnNoneOnInvalidKey(self):
        constants = retrieveConstants('ThisIsNotAValidKey')
        self.assertIsNone(constants)


if __name__ == '__main__':
    unittest.main()
