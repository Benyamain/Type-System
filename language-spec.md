### Language Definition (in extended Backus–Naur form [EBNF]-like notation)
"""
program ::= statement*
statement ::= expression | declaration
declaration ::= 'let' IDENTIFIER ':' type '=' expression
expression ::= INTEGER | BOOLEAN | IDENTIFIER | binary_op | function_call
binary_op ::= expression OPERATOR expression
function_call ::= IDENTIFIER '(' expression (',' expression)* ')'
type ::= 'Int' | 'Bool' | function_type
function_type ::= '(' type (',' type)* ')' '->' type
OPERATOR ::= '+' | '-' | '*' | '/' | '==' | '<' | '>'
BOOLEAN ::= 'True' | 'False'
"""

### Examples:
"""
let x: Int = 5
let y: Bool = True
let add: (Int, Int) -> Int = (a, b) -> a + b
let result: Int = add(x, 3)
let is_positive: (Int) -> Bool = (n) -> n > 0
"""