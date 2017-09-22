class Rule(object):
	'''A condition > effect container'''
	def __init__(self, conditions, effects):
		self.conditions = conditions[:]
		self.effects = effects[:]

class TerminationRule(Rule):
	'''A special kind of rule that ends the game'''
	def __init__(self, conditions, effects=[]):
		super(TerminationRule, self).__init__(conditions, effects)

class Condition(object):
	def __init__(self, name, params):
		self.name = name
		self.params = params[:]

class Effect(object):
	def __init__(self, name, params):
		self.name = name
		self.params = params[:]
