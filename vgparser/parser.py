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

	# Classes Section
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

	# Groups Section
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

	props = lambda self, props: {k: v for d in props for k, v in d.items()}
	prop = lambda self, (key, value): {key: value}

	string = lambda self, (string, ): str(string)

	number = lambda self, (number, ): float(number)

	true = lambda self, : True
	false = lambda self, _: False


# with open('vgdlgrammar.g') as g:
# 	game_parser = Lark(g.read(), start='game', parser='lalr', transformer=Tree2PyVGDL())

# with open('vgdlgrammar.g') as g:
# 	level_parser = Lark(g.read(), start='level', parser='lalr', transformer=Tree2PyVGDL())