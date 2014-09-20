# Contains common vector methods used in both the visualizer and map parser
from math import atan2, pi

# Get the distance between 2-tuples
# @param a The first tuple
# @param b The second tuple
# @returns Distance between a and b, as a float
def vecLen(a, b):
    return pow(float(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2)), 0.5)
    #return abs(a[0] - b[0]) + abs(a[1] - b[1])

def angleBetween(a, b):
	return float(180/pi) * atan2(b[1] - a[1], a[0] - b[0])

# http://www.pygame.org/wiki/RotateCenter?parent=CookBook
