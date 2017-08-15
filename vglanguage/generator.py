from ontology import *
import gparser
import pprint

if __name__ == '__main__':
	game_string = '''
Game < SideView : gravity=(0, -10)
#################################
#   Comments are pretty cool    #
#################################  
Classes  # This is a Comment
	Bird {
		Chicken 
		Duck {
			Mallard
		}
	}
	Fish {
		Trout
		Tuna
	}
Rules
	~Collision(Bird, Fish) > Kill(Bird), Kill(Fish)
	'''

	level_string = '''
Level
Mallard {
	(0, 0, 0)
	(20, 20, 0)
}
Trout {
	(-20, 20, 0)
}
'''
	pp = pprint.PrettyPrinter(indent=4)
	game = gparser.game_parser.parse(game_string)
	level = gparser.level_parser.parse(level_string)

	basic_scene = BasicScene((300, 300), 60)

	classes = {}
	for subclass in game[1]['classes'].subclasses:
		classes[subclass.name] = subclass

	for rule in game[1]['rules']:
		basic_scene.add_condition_handler(rule[0], rule[1])

	# pp.pprint(classes)
	# pp.pprint(game)
	# pp.pprint(level)
	for _class in level[1]:
		for instance in level[1][_class]:
			new_instance = Instance(classes[_class])
			new_instance.position = instance['transform'][:-1]
			new_instance.rotation = instance['transform'][-1]
			basic_scene.room.add(new_instance)

	basic_game = BasicGame(basic_scene)
	basic_game.run()