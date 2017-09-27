from lark import Lark, Transformer
from collections import defaultdict

from grammar import *

# grammar = open('vgdlgrammar.g').read()

ALLCLASS = 'ALLCLASS'
ALLGROUP = 'ALLGROUP'

class Tree2PyVGDL(Transformer):
	def game(self, (props, description)):
		return Game(props, description)

	def hierarchy(self, hierarchy):
		root = hierarchy[0]
		children = hierarchy[1:]
		if children: children = children[0]
		root.add_children(*children)
		return root		

	# Classes 
	###################
	def classes(self, (classes, )):
		root_class = VGDLClass(ALLCLASS, children=classes)
		return root_class

	def vgdlclasses(self, vgdlclasses):
		return vgdlclasses

	def class_hierarchy(self, hierarchy):
		return self.hierarchy(hierarchy)

	def vgdlclass(self, vgdlclass):
		name = vgdlclass[0]
		props = vgdlclass[1:]
		if props: props = props[0]
		return VGDLClass(name, props)
	####################
	# 

	# Groups 
	####################
	def groups(self, groups):
		return groups
		
	def group(self, vgdlgroup):
		name = vgdlgroup[0]
		props = vgdlgroup[1:]
		if props: props = props[0]
		return Group(name, props)
	####################
	#

	# Rules 
	###################
	def rules(self, rules):
		return rules

	def rule(self, (conditions, effects)):
		return Rule(conditions, effects)

	def effects(self, (effects)):
		return effects

	def conditions(self, (conditions)):	
		# print conditions
		return conditions

	def condition(self, (condition)):
		
		sign = lambda func: func()
		if len(condition) > 1:
			sign, condition = condition
		else:
			condition = condition[0]
		return Condition(sign, condition)

	def effect(self, (effect)):
		return Effect(effect)
	###################
	#

	# Termination Rules 
	###################
	def terminationrules(self, terminationrules):
		return terminationrules

	def terminationrule(self, terminationrule):
		return TerminationRule(*terminationrule)
		
	###################
	#

	# Action Sets
	###################
	def actionsets(self, actionsets):
		return actionsets

	def actionset(self, actionset):
		name, mappings = actionset
		return ActionSet(name, mappings)

	def mappings(self, mappings):
		return mappings

	def mapping(self, mapping):
		active = True
		if len(mapping) > 2:
			key_inputs, active, actions = mapping
		else:
			key_inputs, actions = mapping
		return Mapping(key_inputs, actions, active)

	###################
	#

	def function(self, function):
		return Function(*function)

	def param(self, (param)):
		return param

	def props(self, props):
		return {k: v for d in props for k, v in d.items()}


	def prop(self, (key, value)):
		return {key: value}


	neg = lambda self, _: lambda func: not func()

	string = lambda self, (string, ): str(string)

	number = lambda self, (number, ): float(number)

	true = lambda self, : True
	false = lambda self, _: False


# with open('vgdlgrammar.g') as g:
# 	game_parser = Lark(g.read(), start='game', parser='lalr', transformer=Tree2PyVGDL())

# with open('vgdlgrammar.g') as g:
# 	level_parser = Lark(g.read(), start='level', parser='lalr', transformer=Tree2PyVGDL())

# def parse_game(game_string):
# 	return game_parser.parse(game_string)

# def parse_level(level_string):
# 	return level_parser.parse(level_string)