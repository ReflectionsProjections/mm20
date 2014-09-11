# Contains common vector methods used in both the visualizer and map parser
from math import atan2

# Get the distance between 2-tuples
# @param a The first tuple
# @param b The second tuple
# @returns Distance between a and b, as an int
def vecLen(a, b):
    return int(pow(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2), 0.5))

def angleBetween(a, b):
	return atan2(b[1] - a[1], a[0] - b[0])

# http://www.pygame.org/wiki/RotateCenter?parent=CookBook
