## Conditions

A formal definition about a 'Condition' and it's resulting 'Effects'.

The best way to understand them is through sets.

Going back to my Linguistics class on Semantics, let's first develop some terminology that overlaps with the behavior we want.

I'm going to separate our "Ontology" by saying that the Ontology is the classification of things in the world. Technically, "Conditions" are one such classification, but each Condition we can use in our language is part of our "Lexicon". This is purely for semantic purposes.

So, we will define our Lexicon of Conditions as the set of words with specific meaning. We will call this set C. 

In general, the formal use of semantics is to allow operations on our lexicon for interpreting words. Namely, if our lexicon contains "Collision" as one of its words.

Then, there are the things that are variable in our lexicon represented in our ontology as Classes. For instance, if we have defined a game with the classes

```
Bird {
	Duck
	Chicken
}
```

Then we have introduced these words into our Lexicon, and they simply produce the following meanings with respect to our Lexicon:

* Bird := {the set of things that are a Bird}
* Duck := {the set of things that are a Duck}
* Chicken := {x : such that x is a Chicken}

The last example is just me introducing some new but hopefully familiar notation as it is what I will start having to use for the more complex definitions.

By defining these thing as Sets, it may become clearer what the interpretation of 

Collision(Bird, Duck) 

Essentially, it is taking two Sets as arguments, and finding the intersection of things in those sets that are colliding as two new sets. Here is where I'm going to have to divert quite a lot from the regular formal definition of Semantics, but that should be fine since that really isn't the point of this.

So, in either case, what I'm going to do is work backwards from what we want as a result of an expression to figure out how to go through the process of transform the expression to the result. So, for instance:

Collision(X, Y) > Kill(X)

can be written as

Kill x in X. x is colliding with y in Y.

But this doesn't generalize the functionality well. The way we're going to have to think of it is this:

Left Hand Side   >   Right Hand Side

The meaning of the Sets (X and Y) have different meanings entirely on Left Hand Side and the Right Hand Side.

Basically, what can make this clearer is that our syntax is implicitly doing this:

Collision(X, Y) > Kill(X')

Where X' is now whatever transformation resulted from the Condition.

In general, if your language had the classes A, B, C, and D, and there was this statement:

Collision(A, B) > Kill(C)

This would be the same as

Collision(A, B) > Kill(C')

where the lexicon on the left hand side is just the Sets: A, B, C, D, but the lexicon on the right hand side transforms to SetsPrime: A', B', C', D'. Now, how does it actually go through this transformation?

For starters, when we have a rule, we start with both Sets and SetsPrime as being equivalent in pretty much every way except by name. From there, each Condition reduces the SetsPrime in some way.

Collision(A, B) results in:

A' := A' intersect {a : a in A and a is colliding with b in B}
B' := B' intersect {b : b in B and b is colliding with a in A}

This format generalizes the behavior in a way that is nice. I'm going to introduce one more bit of notation to make this nicer (note, I wonder if we could use this instead? Nah, it's fine)

A' := A' intersect Collision(A)(B)
B' := B' intersect Collision(B)(A)

where Collision(A)(B) and Collision(B)(A) have respectively the same meanings as the previous definitions, but using a different notation.

Regardless, what I'm trying to get at is this:

C_i' := C_i' intersect Condition(C_i)(...)(...) 

for all C_1 to C_N class arguments in the condition and for all permutations of the arguments. This kind of reduction and symmetry will allow producing the necessary SetsPrime for applying effects. Because ultimately, the effects will take the SetsPrime and just do this:

Effect(C_i') := for all x in C_i', apply effect to x.

So, for the example:

Collision(Duck, Chicken) & ~Collision(Duck, Goose) > Kill(Duck)

This should effectively only kill the Duck that is both colliding with the Chicken and not colliding with the Goose. We start with:

Duck = Duck'
Goose = Goose'
Chicken = Chicken'

Apply first condition:

Duck' := Duck' intersect Collision(Duck)(Chicken)
Chicken' := Chicken' intersect Collision(Chicken)(Duck)

Apply second condition:

Duck' := Duck' intersect ~Collision(Duck)(Goose)
Goose' := Goose' intersect ~Collision(Goose)(Duck)

This chain of Conditions results in exactly what we want, so when Kill(Duck) is applied, it is applied to Duck', which is now

Duck' := Duck intersect Collision(Duck)(Chicken) intersect ~Collision(Duck)(Goose)


I see no reason this shouldn't work perfectly.