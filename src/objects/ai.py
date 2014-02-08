class ai:
	# optimization = 0
	# stability = 0
	# complexity = 0
	# strategy = 0
	# theory = 0
	# implementation = 0

	def __init__(self, opt, stab, comp, strat, theo, impl):
		self.optimization = opt
		self.stability = stab
		self.complexity = comp
		self.strategy = strat
		self.theory = theo
		self.implementation = impl

	def upOpt(self, opt):
		self.optimization += opt
	def upStab(self, stab):
		self.stability += stab
	def upComp(self, comp):
		self.complexity += comp
	def upStrat(self, strat):
		self.strategy += strat
	def upTheo(self, theo):
		self.theory += theo
	def upImpl(self, impl):
		self.implementation += impl

	def downOpt(self, opt):
		self.optimization -= opt
	def downStab(self, stab):
		self.stability -= stab
	def downComp(self, comp):
		self.complexity -= comp
	def downStrat(self, strat):
		self.strategy -= strat
	def downTheo(self, theo):
		self.theory -= theo
	def downImpl(self, impl):
		self.implementation -= impl

	def setOpt(self, opt):
		self.optimization = opt
	def setStab(self, stab):
		self.stability = stab
	def setComp(self, comp):
		self.complexity = comp
	def setStrat(self, strat):
		self.strategy = strat
	def setTheo(self, theo):
		self.theory = theo
	def setImpl(self, impl):
		self.implementation = impl

if __name__ == '__main__':
	test = ai(10,20,30,40,50,60)
	# test.upOpt(1)
	# test.upStab(1)
	# test.upComp(1)
	# test.upStrat(1)
	# test.upTheo(1)
	# test.upImpl(1)
	# print test.optimization
	# print test.stability
	# print test.complexity
	# print test.strategy
	# print test.theory
	# print test.implementation

	# test.downOpt(1)
	# test.downStab(1)
	# test.downComp(1)
	# test.downStrat(1)
	# test.downTheo(1)
	# test.downImpl(1)
	# print test.optimization
	# print test.stability
	# print test.complexity
	# print test.strategy
	# print test.theory
	# print test.implementation

	# test.setOpt(1)
	# test.setStab(1)
	# test.setComp(1)
	# test.setStrat(1)
	# test.setTheo(1)
	# test.setImpl(1)
	print test.optimization
	print test.stability
	print test.complexity
	print test.strategy
	print test.theory
	print test.implementation	