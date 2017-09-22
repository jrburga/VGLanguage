from ontology import *
import gparser
import pprint


def CreateGame(game_string, level_string):
	pp = pprint.PrettyPrinter(indent=4)
	game = gparser.game_parser.parse(game_string)
	level = gparser.level_parser.parse(level_string)

	basic_scene = BasicScene((300, 300), 60)
	basic_scene.physics.space.gravity = game[0][1]['gravity']

	# for leaf in game[1]['classes'].leaves:
	# 	print leaf.name
	actionsets = game[1]['action_set']
	# print actionsets
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
			new_instance.orientation = instance['transform'][-1]
			basic_scene.add_instance(new_instance)
	# print 'human', list(game[1]['classes'].find('Human').instances)[0].resources
	basic_game = BasicGame(basic_scene)
	return basic_game 

if __name__ == '__main__':
	game_string = '''
Game < SideView : gravity = (0, 0) :

Classes 
	Bouncy : elasticity = 1.0 friction = 0.0 : {
		Brick : bodytype = STATIC 
				shape = RECT(20, 5) 
				color = RED :
		Paddle : controller=Horizontal
				 actionset=LeftRight
				 shape = RECT(30, 5) 
				 mass=inf :
		Wall : bodytype = STATIC 
			   shape = RECT(300, 2) :
		Ball : shape = RECT(3, 3) 
			   velocity = (1000, 750)
			   controller=SpeedLimiter :
	}
Rules 
	Collision(Brick, Ball) > Kill(Brick)
	InstanceCount(all, 0, =) > Kill(Ball)
	# Killed(Ball)

ActionSets 
	LeftRight {
		LEFT  > Move((-1, 0), 300)
		RIGHT > Move((1 , 0), 300)
		NONE  > Move((0, 0), 0)
	}
'''
	level_string = '''
Level
Paddle {
	(0, -100, 0)
}
Wall {
	(0, 100, 0)
	(-148, 0, 1.5708)
	(148, 0, 1.5708)
	(0, -149, 0)
}
Ball {
	(0, -50, 0)
}
Brick {
	(-130, 0, 0)
	(-110, 0, 0)
	(-90, 0, 0)
	(-70, 0, 0)
	(-50, 0, 0)
	(-30, 0, 0)
	(-10, 0, 0)
	(10, 0, 0)
	(30, 0, 0)
	(50, 0, 0)
	(70, 0, 0)
	(90, 0, 0)
	(110, 0, 0)
	(130, 0, 0)

	(-130, 5, 0)
	(-110, 5, 0)
	(-90, 5, 0)
	(-70, 5, 0)
	(-50, 5, 0)
	(-30, 5, 0)
	(-10, 5, 0)
	(10, 5, 0)
	(30, 5, 0)
	(50, 5, 0)
	(70, 5, 0)
	(90, 5, 0)
	(110, 5, 0)
	(130, 5, 0)

	(-130, 10, 0)
	(-110, 10, 0)
	(-90, 10, 0)
	(-70, 10, 0)
	(-50, 10, 0)
	(-30, 10, 0)
	(-10, 10, 0)
	(10, 10, 0)
	(30, 10, 0)
	(50, 10, 0)
	(70, 10, 0)
	(90, 10, 0)
	(110, 10, 0)
	(130, 10, 0)
}
'''
	basic_game = CreateGame(game_string, level_string)
	basic_game.run()