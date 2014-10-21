import pygame

class StatsVisualizer(object):

	def __init__(self, visualizer):
		self.visualizer =visualizer

		self.setup()

	def setup():
		pygame.display.set_caption("")