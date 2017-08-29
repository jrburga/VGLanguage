from ontology import *
import gparser
import pprint

if __name__ == '__main__':
	game_string = '''

Game < SideView : gravity=(0, 0) :
#################################
#   Comments are pretty cool    #
#################################  
Classes  # This is a Comment
	Bird : gravity=(0, -100) : {
		Chicken : color=RED :
		Duck {
			Mallard : color=GREEN :
			Whitetail : color=WHITE :
		}
	}
	Fish : gravity=(0, 100) : {
		Trout  : color=BLUE   :
		Tuna   : color=YELLOW :
		Salmon : color=SALMON   :
	}
	Human : actionset=BasicMotion  
			controller=Keyboard 
			health=RESOURCE(100)
			gravity=(0, 0)
			shape=CIRCLE(5)
			color=LIGHTBLUE :

	Platform : bodytype=STATIC 
			   shape=RECT(100, 10) :
Rules
	Collision(Bird, Human) > Kill(Fish), Kill(Human)
ActionSets
	BasicMotion {
		UP   > Move((0 , 1), 1)
		DOWN > Move((0 ,-1), 1)
		LEFT > Move((-1, 0), 1)
		RIHT > Move((1 , 0), 1)
	}
	'''

	level_string = '''
Level
Mallard {
	(0, 60, 0)
}
Trout {
	(0, -60, 0)
}
Chicken {
	(30, 60, 0)
}	
Tuna {
	(-30, -60, 0)
}
Whitetail {
	(-30, 60, 0)
}
Salmon {
	(30, -60, 0)
	(-60, -60, 0)
	(-60, -60, 0)
}
Human {
	(0, 0, 0)
}
Platform {
	(0, -100, 0)
}
'''
	pp = pprint.PrettyPrinter(indent=4)
	game = gparser.game_parser.parse(game_string)
	level = gparser.level_parser.parse(level_string)

	basic_scene = BasicScene((300, 300), 60)
	basic_scene.physics.space.gravity = game[0][1]['gravity']

	# for leaf in game[1]['classes'].leaves:
	# 	print leaf.name
	actionsets = game[1]['action_set']
	print actionsets
	classes = {}
	for subclass in game[1]['classes'].subclasses:
		# print subclass.name
		if 'actionset' in subclass._props:
			subclass._props['actionset'] = actionsets[subclass._props['actionset']]

		if 'controller' in subclass._props:
			subclass._props
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
	print 'human', list(game[1]['classes'].find('Human').instances)[0].resources
	basic_game = BasicGame(basic_scene)
	basic_game.run()