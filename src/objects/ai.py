from config.handle_constants import retrieveConstants
from unittest import TestCase, main


class ai:
    # optimization = 0
    # stability = 0
    # complexity = 0
    # strategy = 0
    # theory = 0
    # implementation = 0

    def __init__(self):
        defaults = retrieveConstants('aiDefaults')
        self.optimization = defaults['optimization']
        self.stability = defaults['stability']
        self.complexity = defaults['complexity']
        self.theory = defaults['theory']
        self.implementation = defaults['implementation']

    def incrementAttribute(self, attribute, ammount):
        self.__dict__[attribute] += ammount

    def decrementAttribute(self, attribute, ammount):
        self.__dict__[attribute] -= ammount

    def setAttribute(self, attribute, ammount):
        self.__dict__[attribute] = ammount


class TestAI(TestCase):
    def setUp(self):
        self.ai = ai()

    def test_init(self):
        defaults = retrieveConstants('aiDefaults')
        self.assertEqual(self.optimization, defaults['optimization'])
        self.assertEqual(self.stability, defaults['stability'])
        self.assertEqual(self.complexity, defaults['complexity'])
        self.assertEqual(self.theory, defaults['theory'])
        self.assertEqual(self.implementation, defaults['implementation'])
        pass

    def test_2(self):
        pass

if __name__ == '__main__':
    main()
