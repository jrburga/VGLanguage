class Game(object):
	def __init__(self, props, description):
		pass

# Group and VGDLClass
class Group(object):
	def __init__(self, name, props={}):
		self.name = name
		self.props = {}
		self.props.update(props)

	def toDict(self):
		return_dict = {}
		return_dict['name'] = self.name
		return {'name'    : self.name, 
				'props'   : self.props}

class VGDLClass(Group):
	def __init__(self, name, props={}, children=[]):
		super(VGDLClass, self).__init__(name, props)
		self.children = []
		self.parent = None
		self.add_children(*children)
		
	def add_children(self, *children):
		for child in children:
			child.parent = self
			self.children.append(child)

	def remove_child(self, child):
		self.children.remove(child)
		child.parent = None


	def __str__(self):
		return 'VGDLClass: %s%r' % (self.name, self.props)

	def __repr__(self):
		return self.__str__()

#Action Sets
class ActionSet(object):
	def __init__(self, name, mappings):
		self.name = name
		self.mappings = mappings[:]

class Mapping(object):
	def __init__(self, key_input, action, active = True):
		self.active = active
		self.key_input = key_input
		self.action = action

class Action(object):
	def __init__(self, function):
		self.function = function

class KeyInput(object):
	def __init__(self, name):
		self.name = name

#Rules
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
	def __init__(self, sign, function):
		self.function = function

class Effect(object):
	def __init__(self, function):
		self.function = function

class Function(object):
	def __init__(self, name, params=[]):
		self.name = name
		self.params = params[:]
