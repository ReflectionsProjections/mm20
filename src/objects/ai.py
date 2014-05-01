import config.handle_constants
import unittest


## Holds all of the attributes for a team's Artificial Intelligence
class AI(object):
    ## Constructs the AI from the defaults found in constants.json
    def __init__(self):
        defaults = config.handle_constants.retrieveConstants('aiDefaults')
        self.optimization = defaults['optimization']
        self.stability = defaults['stability']
        self.complexity = defaults['complexity']
        self.theory = defaults['theory']
        self.implementation = defaults['implementation']

    ## Returns a seralible repesentaion of the AI
    # @return
    #    A dict that reprents the AI's stats
    def output_dict(self):
        return self.__dict__

    ## Sets an attribute to a given amount
    # @param attribute
    #   The attribute to set
    # @param amount
    #   The value to set it to
    def setAttribute(self, attribute, amount):
        if amount < 0:
            amount = 0
        self.__dict__[attribute] = amount


class TestAI(unittest.TestCase):
    def setUp(self):
        self.ai = AI()

    ## Test value initialization + constant retrieval
    def test_init(self):
        defaults = config.handle_constants.retrieveConstants('aiDefaults')
        self.assertIsNotNone(defaults)
        self.assertEqual(self.ai.optimization, defaults['optimization'])
        self.assertEqual(self.ai.stability, defaults['stability'])
        self.assertEqual(self.ai.complexity, defaults['complexity'])
        self.assertEqual(self.ai.theory, defaults['theory'])
        self.assertEqual(self.ai.implementation, defaults['implementation'])

    ## Test setAttribute
    def test_setAttribute(self):
        self.ai.setAttribute('complexity', 300)
        self.assertEqual(self.ai.complexity, 300)
        self.ai.setAttribute('implementation', -500)
        self.assertEqual(self.ai.implementation, 0)

if __name__ == '__main__':
    unittest.main()
