Problems with physics
* Change how motion is performed on dyn/kin bodies
** This will require applying velocities ONCE one keypress. Should this be part of the controller

In general, need to have more options for types of key presses:
* Press
* Hold
* Release
* Combos
* Multi-Key

This should solve the physics problems, I presume.

But then, the agent is going to have to infer the types of controls, but that seems like ~~exactly~~ what tutorials are for.	

Problems with properties
* I think I'm going to have to enumerate all the properties of an instance

Physical Properties
* mass
* moment
* density
* size 
** shape
** area
* friction
* elasticity
* position
* velocity
* gravity

Graphical Properties
* (Shared with physical)
** size
*** shape
*** area
* appearance
** color
** image

Control Properties
* controller
* action set

Misc
* timer
* resources
** extends attributes of the object

