# Rules

## Motivation

Standardizing this is difficult because we have to deal with two things:

* Conditions are ultimately things that return True and False
* But, effects apply to instances
* So, we need som way to refer to the instances some how defined by the conditions
* Ambiguity insues.

So we need to come up with a strict way of turning chained Conditions into a set of instances that an Effect acts upon.

## Preface (More thoroughly described in Classes.md once I write that.)

Given a set of Classes: {X, Y, Z} where

`
X {
	Y
	Z
}
`

Just defines a bunch of sets, Y and Z are disjoint subsets of X. Assuming that all instances of a class must be defined as a "leaf" class's subsets, the Z and Y are also complete subsets. In other words, Z union Y exactly equals X. However, this doesn't have to be the case, but is an assumption based on how instances are defined in the original version of VGDL. The new version wouldn't necessarily have to work this way. But in general, defining instances is equivalent to saying that that instance belongs to a specific set.

Side note and visualizations:

disjoint, complet subsets

	  X
 _____________
|  Y   |  Z   |
|      |      |
|      |      |
|      |      |
|______|______|

Condinued: 

In the version where you can define an instance in terms of any class, I've already created a 'root' class that every class subclasses from, and it would have the basic/default features for everysprite. So, essentially, every heirarchy tree looks like whatever you define, plus:

`
root {
	user_defined_heirarchy
}
`

This is used mostly for theoretical purposes, but in terms of creating instances, I could create an instance of X that is neither Y nor Z.

Disjoint, and incomplete subsets.
 _______________
|     root      |
|               |
|  ___________  |
| |     X     | |
| |           | |
| |___________| |
| |  Y  |  Z  | |
| |_____|_____| |
|_______________|

## Conditions


### Idea 1, and why it won't work 

This first way is more or less the way I had decided to implement it to begin with. It is currently one of the easier to write and understand, but not as expressible in terms of capturing all logical formulas.

`Conditions modify their global sets to pass on to conditions`

The first impression of a condition is that it simply returns True or False, but it also needs to keep track of the instances involved. So, the second impression might just be that conditions simply return the set of things for which the condition is true:

`Condition(Class) := {x : x in Class such that Condition(x)}`

But this isn't enough. Because any number of conditions can be applied to any number of classes, there needs to be a more robust way of keeping track. So here is what I ultimately came up with after some trial and error.

A rule is initialized with and modifies it's own set of classes containing all sets and instances. More precisely, given the example above with X, Y, Z, a rule will initialize with X', Y', and Z' where the sets of sets are respectively equal to each other. Rules then reduce each of its sets down to the intersections between its conditions. So now, what a condition actually does is 

`Condition(X) ==> X' := X' intersect {x : x in X such that Condition(x)}`

and a condition that modifies multiple sets looks like this

`Condition(X, Y) ==> X' := X' intersect {x : x in X such that Condition(y)} and Y' = Y'= intersect {y : y in Y such that Condition(y)}

So instead of returning a new class, it modifies it's copies of the respective class. It does this for two reasons: to keep track of instances involved in all conditions, and then to have a final set of things left by the time we get to the effects that apply to them.

What this means is that rules have the following effect:

`
Condition1(X) & Condition(X) ==>
X' := X' intersect {x : x in X such that Condition1(x)} ==>
X' := X' intersect {x : x in X such that Condition2(x)}
`

Which is equivalent to 

`
X' := {x : x in X such that Condition1(x)} intersect {x : x in X such that Condition2(x)}
X' := {x : x in X such that Condition1(x) and Condition2(x)}
`

While collisions modify two sets at once, it's essentially the same idea.

What this means is that effects will end up with a concrete set of instances to act upon. But now Conditions aren't really conditions anymore, they're just things that return sets. By extension, logical formulisms don't strictly apply, so we can't do something like this:
X {
	Y
	Z
	A {
		B
		C
	}
}

And we would want to apply an effect to these instances conditioned upon something:

`
instances :=  { 
	{x : x in X and EXISTS y in Y where x collides with y} IF {x : x in X and EXISTS a in A where x collides with A} is EMPTY,
	{} ELSE
}
`

Or by your example:

Collision(X, Y) and ~Collision(X, A, any=True)

Or at least that's how I interpretated this statement. Like I said, this is doable, and requires some kind of modifier like 'any' or other extension to the language to be used to transform the Condition into an actual Condition that just returns True, or in the case of set modification in general:

`
Condition(X, any=True) ==> X' := X' intersect {X} IF Condition(x) for ALL x in X
							  := X' intersect {}  ELSE
`

Side note: I've introduced the * argument as a wildcard, so Condition(*) and Effect(*) apply to everything, or, in the case of complete heirarchy, the 'root' set. Another notation we could use is Condition(X)*, which would mean return all or nothing.

## Idea 2, Semantics and Formal Logic

The point of Formal Logic is to have a grammar that generates unambiguous representations of the world, and by extension, language. The linguistic study of Semantics took a lot of the ideas developed in Set theory and made it their own. Maybe it was the other way around. Who knows. The point of bringing up Semantics, though, is the fact that it develops a way to generate unambiguous translations by assigning more abstract meaning to words of a Lexicon. We're developing a language in the strictest of senses, so I feel like there is a lot to take from this formalism.

Semantics captures grammars through Lexicons, Variable, Identifiers, Predicates, and Special Symbols. This is pretty much exactly what we want. There is enough generality in this method to come up with simple structers of things. I'll start by introducing some possibilities for new syntax.

A Predicate, like a Condition, looks like a Function, so let's say we have the predicates

`
Dead := {x : x is dead}
`

and 

`
Dead(X)
`

simply means 

`
X is Dead
`

This isn't exactly what we want.

I think simply, we are looking for a way to capture things like

Collision(X)(Z) & Collision(Y)(Z)

(Collision(X) & Collision(Y))(Z)

The 'any' keyword is looking relatively useful now...