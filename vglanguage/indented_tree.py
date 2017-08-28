#
# This example demonstrates usage of the Indenter class.
#
# Since indentation is context-sensitive, a postlex stage is introduced to
# manufacture INDENT/DEDENT tokens.
#
# It is crucial for the indenter that the NL_type matches
# the spaces (and tabs) after the newline.
#

from lark.lark import Lark
from lark.indenter import Indenter

tree_grammar = r"""
    ?start: _NL* tree
    tree: name [":" props] _NL [_INDENT tree+ _DEDENT]
    name: NAME
    props: prop+
    prop: attr "=" value
    attr: NAME
    value: NAME
         | NUM 
         | bool

    bool: "True" | "False"
    %import common.SIGNED_NUMBER -> NUM
    %import common.CNAME -> NAME
    %import common.WS_INLINE
    %ignore WS_INLINE
    _NL: /(\r?\n[\t ]*)+/
    _INDENT: "<INDENT>"
    _DEDENT: "<DEDENT>"
"""

class TreeIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8

parser = Lark(tree_grammar, parser='lalr', postlex=TreeIndenter())

test_tree = """
Bird
    Chicken : one=1 two=2
    Duck
        Mallard : color=GREEN
        Whitetail
    Fish
        Trout
        Tuna
"""

def test():
    print(parser.parse(test_tree).pretty())

if __name__ == '__main__':
    test()