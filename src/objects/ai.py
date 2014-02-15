class ai:
	# optimization = 0
	# stability = 0
	# complexity = 0
	# strategy = 0
	# theory = 0
	# implementation = 0

	def __init__(self, opt, stab, comp, theo, impl, offen, defen):
		self.optimization = opt
		self.stability = stab
		self.complexity = comp
		self.theory = theo
		self.implementation = impl
		self.offensiveness = offen
		self.defensiveness = defen
		self.strategy = self.offensiveness + self.defensiveness


	def setOpt(self, opt):
		self.optimization = opt
	def setStab(self, stab):
		self.stability = stab
	def setComp(self, comp):
		self.complexity = comp
	def setTheo(self, theo):
		self.theory = theo
	def setImpl(self, impl):
		self.implementation = impl
	def setOffen(self, offen):
		self.offensiveness = offen
	def setDefen(self, defen):
		self.defensiveness = defen
	def setStrat(self):
		self.strategy = self.offensiveness + self.defensiveness

	def upOpt(self, opt):
		self.optimization += opt
	def upStab(self, stab):
		self.stability += stab
	def upComp(self, comp):
		self.complexity += comp
	def upTheo(self, theo):
		self.theory += theo
	def upImpl(self, impl):
		self.implementation += impl
	def upOffen(self, offen):
		self.offensiveness += offen
		self.setStrat()
	def upDefen(self, defen):
		self.defensiveness += defen
		self.setStrat()

	def downOpt(self, opt):
		self.optimization -= opt
	def downStab(self, stab):
		self.stability -= stab
	def downComp(self, comp):
		self.complexity -= comp
	def downTheo(self, theo):
		self.theory -= theo
	def downImpl(self, impl):
		self.implementation -= impl
	def downOffen(self, offen):
		self.offensiveness -= offen
		self.setStrat()
	def downDefen(self, defen):
		self.defensiveness -= defen
		self.setStrat()


if __name__ == '__main__':
	test = ai(10,20,30,40,50,60,70)

	test.upDefen(10)
	test.downOffen(10)

	print test.optimization
	print test.stability
	print test.complexity
	print test.theory
	print test.implementation	
	print test.offensiveness
	print test.defensiveness
	print test.strategy