Rules
=====


	    Rule
	     |
	    / \
       /   \
      /     \
Condition  Effect 


Rule := Condition > Effect

Effect(Condition.instances)

Effects are applied to the instances of the class specified by the condition and the effect.

Otherwise, they are applied to all instances of a specified class.

Condition(Classes, args) > Effect(Classes', args)

Maybe more explicitly:

for all instances of Classes', apply Effect(instances, args) 
	iff there exists an instance of the instances of Classes 
		such that Condition(instances, args) is True


Example:
Classes 
	Bird {
		Duck
		Goose
	}
Level 
	Duck {(0, 0, 0)}
	Goose {(0, 0, 0)}


<Duck> <-Collision-> <Goose>

Rule: Collision(Bird, Bird) -> Kill(Bird)

		Collision(<Duck>, <Goose>) -> Kill(<Goose>)
		Collision(<Goose>, <Duck>) -> Kill(<Duck>)

Is all that really needs to happen.

So, I guess this will kill both birds. I suppose that's fine. 

Rule: should basically just hold on to the instances it cares about, and nothing else.

Conditions and effects should just be functions, shouldn't they?

A rule can use the condition and effect functions to determine the instances.


Condition

Condition & Condition => Condition

~Condition => Condition

Effect

Effect, Effect => Effect 

Condition Classes             Effect Classes
Class1, Class2, ... ClassN => Class1', Class2', ... ClassM'

Conditions can refer to classes (or not) and so can Effects

So they should mostly just be handling the instances themselves?




