from unittest import TestCase, main


class Food(object):
    def __init__(self, name, container, amount):
        self.name = name
        self.container = container
        self.amount = amount

    def consume(self, person):
        amountConsumed = person.consumeFood(self)
        
        self.amount = self.amount - amountConsumed


class TestFood(TestCase):
    class MockPerson:
        def consumeFood(self, food):
            if food.name == 'Coke':
                return 5
            return 1

    def setUp(self):
        self.mockPerson = TestFood.MockPerson()
        self.coke = Food('Coke', 'Caffeine', 50)
        self.cake = Food('Cake', 'Table', 10)

    def test_consume_basic(self):
        self.cake.consume(self.mockPerson)
        self.assertEqual(self.cake.amount, 9)

        self.coke.consume(self.mockPerson)
        self.assertEqual(self.coke.amount, 45)

    def test_consume_all(self):
        for i in xrange(20):
            self.cake.consume(self.mockPerson)
        self.assertEqual(self.cake.amount, 0)

if __name__ == "__main__":
    main()
