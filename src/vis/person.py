
class Person:
	def __init__(self, room, size, image_name):
		self.size = size
		self.image = pygame.image.load(image_name).convert()
		self.state.room = room
	def update():
		this.state = dict()
	def draw(ScreenSurface):
		# ScreenSurface.blit(self.image, self.pos)
		pass
	def move(room):
		this.state['move'] = (this.room, room)
		this.room = room
	def eat():
		this.state['eat'] = True
	def distract(victim):
		this.state['distract'] = victim
	def sleep():
		this.state['sleep'] = True
	def

