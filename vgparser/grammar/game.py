class Game(object):
	def __init__(self, props, description):
		pass

# Group and VGDLClass
class Group(object):
	def __init__(self, name, props={}):
		self.name = name
		self.props = {}
		self.props.update(props)

	def toJSON(self):
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

	def toJSON(self):
		return {'name': self.name,
				'props': self.props,
				'children': [child.toJSON() 
				for child in self.children]}

	def __str__(self):
		return 'VGDLClass: %s%r' % (self.name, self.props)

	def __repr__(self):
		return self.__str__()

#Action Sets
class ActionSet(object):
	def __init__(self, name, mappings):
		self.name = name
		self.mappings = mappings[:]

	def toJSON(self):
		return {'name': self.name,
				'mappings': [mapping.toJSON() 
				for mapping in self.mappings]}

class Mapping(object):
	def __init__(self, key_input, action, active = True):
		self.active = active
		self.key_input = key_input
		self.action = actions

	def toJSON(self):
		return {
				'inputs' : [ki.toJSON() for ki in self.key_input],
				'active' : self.active,
				'actions': [act.toJSON() for act in self.actions] 
			   }

class FuncObj(object):
	def __init__(self, function):
		self.function = function

	def toJSON(self):
		return self.function.toJSON()	

class Function(object):
	def __init__(self, name, params=[]):
		self.name = name
		self.params = params[:]

	def toJSON(self):
		return {'name': self.name, 
			    'params': self.params}

class Action(FuncObj):
	pass



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

class Condition(FuncObj):
	pass

class Effect(FuncObj):
	pass
