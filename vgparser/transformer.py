from lark import Lark, Transformer
from collections import defaultdict

from grammar import *

grammar = open('vgdlgrammar.g').read()

class Tree2PyVGDL(Transformer):
	def game(self, (props, description)):
		return Game(props, description)

	


# with open('vgdlgrammar.g') as g:
# 	game_parser = Lark(g.read(), start='game', parser='lalr', transformer=Tree2PyVGDL())

# with open('vgdlgrammar.g') as g:
# 	level_parser = Lark(g.read(), start='level', parser='lalr', transformer=Tree2PyVGDL())