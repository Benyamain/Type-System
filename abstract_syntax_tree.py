from dataclasses import dataclass
from typing import List, Union, Optional

@dataclass
class Type:
    pass

@dataclass
class IntType(Type):
    pass

@dataclass
class BoolType(Type):
    pass

@dataclass
class FunctionType(Type):
    param_types: List[Type]
    return_type: Type

@dataclass
class Expression:
    pass

@dataclass
class IntLiteral(Expression):
    value: int

@dataclass
class BoolLiteral(Expression):
    value: bool

@dataclass
class Variable(Expression):
    name: str

@dataclass
class BinaryOp(Expression):
    left: Expression
    operator: str
    right: Expression

@dataclass
class FunctionCall(Expression):
    function: Expression
    arguments: List[Expression]

@dataclass
class Declaration:
    name: str
    type_annotation: Optional[Type]
    value: Expression

@dataclass
class Program:
    statements: List[Union[Expression, Declaration]]

@dataclass
class LambdaFunction(Expression):
    parameters: List[str]
    body: Expression