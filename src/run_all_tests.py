#!/usr/bin/env python2
import unittest

if __name__ == "__main__":
    suit = unittest.TestLoader().discover('.', '*.py')
    unittest.TextTestRunner(verbosity=2).run(suit)
