// GameDescription
// ****************
game: header body
header: "Game"
body: (classes
	  | groups)

// Classes
// ****************
classes: "Classes" vgdlclasses
vgdlclasses: class_hierarchy+
class_hierarchy: vgdlclass ["{" vgdlclasses "}"]
vgdlclass: name [":" props]
// ****************

// Groups
// ****************
groups: "Groups" group+
group: name ":" props
// ****************

// ActionSets
// ****************
actionsets: "ActionSets" actionset+
actionset: name "{" mappings "}"
mappings: mapping+
mapping: key_inputs [":" active_flag] ">" actions
actions: action ("," action)
key_inputs: key_input ("&" key_input)
action: function

function: name "(" (param ["," param])? ")"
param: name | value

props: prop+
prop: key "=" value

key_input: UCASE -> string
active_flag: "active" | "inactive"
name: UCAMEL -> string
key: LCAMEL -> string

value: NUMBER  -> number
     | "True"  -> true
     | "False" -> false

UCAMEL: /([A-Z]([a-z]|[A-Z])*)/
LCAMEL: /([a-z]([a-z]|[A-Z])*)/
UCASE: /([A-Z])+/

COMMENT: "#"+ /./* NEWLINE

%import common.NUMBER
%import common.NEWLINE
%import common.WS

%ignore WS
%ignore COMMENT
%ignore NEWLINE