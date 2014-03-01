from config.handle_constants import retrieveConstants
from unittest import TestCase, main


class AI:

    def __init__(self):
        defaults = retrieveConstants('aiDefaults')
        self.optimization = defaults['optimization']
        self.stability = defaults['stability']
        self.complexity = defaults['complexity']
        self.theory = defaults['theory']
        self.implementation = defaults['implementation']

    """Changes an attribute given the amount
        positive number passed to increment
        negative number passed to decrement"""
    def changeAttribute(self, attribute, amount):
        if attribute not in self.__dict__:
            return "invalid attribute"
        self.__dict__[attribute] += amount

        if self.__dict__[attribute] < 0:
            setAttribute(attribute, 0)

    def setAttribute(self, attribute, amount):
        self.__dict__[attribute] = amount


class TestAI(TestCase):
    def setUp(self):
        self.ai = AI()

    def test_init(self):
        defaults = retrieveConstants('aiDefaults')
        self.assertIsNotNone(defaults)
        self.assertEqual(self.ai.optimization, defaults['optimization'])
        self.assertEqual(self.ai.stability, defaults['stability'])
        self.assertEqual(self.ai.complexity, defaults['complexity'])
        self.assertEqual(self.ai.theory, defaults['theory'])
        self.assertEqual(self.ai.implementation, defaults['implementation'])
        pass

    def test_2(self):
        defaults = retrieveConstants('aiDefaults')
        self.assertIsNotNone(defaults)
        self.ai.changeAttribute('optimization', 5)
        self.assertEqual(self.ai.optimization, defaults['optimization'] + 5)
        self.ai.changeAttribute('stability', -9000)
        self.assertEqual(self.ai.stability, 0)
        self.assertEqual(
            self.ai.setAttribute('bunnies', 500),
            "invalid attribute")
        pass

    # def test_3(self):
    #     self.ai.setAttribute('complexity', 300)
    #     self.assertEqual(self.ai.complexity, 300)
    #     pass

if __name__ == '__main__':
    main()
