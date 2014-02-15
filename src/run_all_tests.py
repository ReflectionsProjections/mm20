#!/usr/bin/env python2

from unittest import TestLoader, TextTestRunner

if __name__ == "__main__":
    suit = TestLoader().discover('.', '*.py')
    TextTestRunner(verbosity=2).run(suit)
