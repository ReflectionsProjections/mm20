import config.handle_constants
import unittest


class AI:
    def __init__(self):
        defaults = config.handle_constants.retrieveConstants('aiDefaults')
        self.optimization = defaults['optimization']
        self.stability = defaults['stability']
        self.complexity = defaults['complexity']
        self.theory = defaults['theory']
        self.implementation = defaults['implementation']

    # Changes an attribute given the amount
    # @param Attribute The attribute to (in-/de-)crement
    # @param amount The amount to (in-/de-)crement the attribute (positive = increment; negative = decrement)
    def changeAttribute(self, attribute, amount):
        if attribute not in self.__dict__:
            return "Invalid attribute"  # TODO - Should this be an exception instead?

        self.__dict__[attribute] += amount

        if self.__dict__[attribute] < 0:
            self.setAttribute(attribute, 0)

    ## Sets an attribute to a given amount
    # @param attribute The attribute to set
    # @param amount The value to set it to
    def setAttribute(self, attribute, amount):
        self.__dict__[attribute] = amount  # TODO Do we want to allow negative values here?


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
        pass

    ## Test changeAttribute
    def test_changeAttribute(self):
        defaults = config.handle_constants.retrieveConstants('aiDefaults')
        self.assertIsNotNone(defaults)

        # Test that changeAttribute actually sets values
        self.ai.changeAttribute('optimization', 5)
        self.assertEqual(self.ai.optimization, defaults['optimization'] + 5)

        # Test changeAttribute's zero-clamping (i.e. attributes should have a minimum value of 0)
        self.ai.changeAttribute('optimization', -90000)
        self.assertEqual(self.ai.optimization, 0)

        # Test changeAttribute's handling of nonexistent attributes
        self.assertEqual(
            self.ai.changeAttribute('THISattributeDOESnotEXIST', 500),
            "Invalid attribute")
        pass

    ## Test that AI's complexity can be set
    def test_complexity(self):
        self.ai.setAttribute('complexity', 300)
        self.assertEqual(self.ai.complexity, 300)
        pass

if __name__ == '__main__':
    unittest.main()
