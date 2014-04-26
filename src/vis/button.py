
class Button:
	def __init__(self, x, y, size, image_name):
		self.pos = x, y
		self.size = size
		self.image = pygame.image.load(image_name).convert()
		# self.image = pygame.transform.scale(self.image,(size, size))
	def draw(ScreenSurface):
		ScreenSurface.blit(self.image, self.pos)

	# When a mouse clicks, it will check to see if it's pressing this button
	def pushTest(mousePos):
		if( \
			mousePos[0] > this.pos[0] and mousePos[0] < this.pos[0] + this.size \
			mousePos[1] > this.pos[1] and mousePos[1] < this.pos[1] + this.size \
		):
			return True
		return False

