from abstract_syntax_tree import *
from typing import Dict

class TypeVariable:
    def __init__(self):
        self.instance = None

class TypeInferencer:
    def __init__(self):
        self.type_env: Dict[str, Type] = {}
        self.constraints = []

    def infer_program(self, program: Program):
        for statement in program.statements:
            if isinstance(statement, Declaration):
                self.infer_declaration(statement)
            elif isinstance(statement, Expression):
                self.infer_expression(statement)
        self.unify()

    def infer_declaration(self, declaration: Declaration):
        inferred_type = self.infer_expression(declaration.value)
        if declaration.type_annotation:
            self.unify_types(inferred_type, declaration.type_annotation)
        self.type_env[declaration.name] = inferred_type

    def infer_expression(self, expr: Expression) -> Type:
        if isinstance(expr, IntLiteral):
            return IntType()
        elif isinstance(expr, BoolLiteral):
            return BoolType()
        elif isinstance(expr, Variable):
            if expr.name in self.type_env:
                return self.type_env[expr.name]
            else:
                new_type = TypeVariable()
                self.type_env[expr.name] = new_type
                return new_type
        elif isinstance(expr, BinaryOperation):
            left_type = self.infer_expression(expr.left)
            right_type = self.infer_expression(expr.right)
            if expr.operator in ['+', '-', '*', '/']:
                self.unify_types(left_type, IntType())
                self.unify_types(right_type, IntType())
                return IntType()
            elif expr.operator in ['==', '<', '>']:
                self.unify_types(left_type, right_type)
                return BoolType()
        elif isinstance(expr, FunctionCall):
            func_type = self.infer_expression(expr.function)
            arg_types = [self.infer_expression(arg) for arg in expr.arguments]
            return_type = TypeVariable()
            self.unify_types(func_type, FunctionType(arg_types, return_type))
            return return_type
        raise TypeError(f"Cannot infer type for expression: {expr}")
    
    def unify_types(self, type1: Type, type2: Type):
        if isinstance(type1, TypeVariable):
            if type1.instance is None:
                type1.instance = type2
            else:
                self.unify_types(type1.instance, type2)
        elif isinstance(type2, TypeVariable):
            self.unify_types(type2, type1)
        elif isinstance(type1, FunctionType) and isinstance(type2, FunctionType):
            if len(type1.param_types) != len(type2.param_types):
                raise TypeError("Function types have different numbers of parameters")
            for param1, param2 in zip(type1.param_types, type2.param_types):
                self.unify_types(param1, param2)
            self.unify_types(type1.return_type, type2.return_type)
        elif type(type1) != type(type2):
            raise TypeError(f"Type mismatch: {type1} and {type2}")
        
    def unify(self):
        for name, type_var in self.type_env.items():
            self.type_env[name] = self.resolve_type(type_var)
            
    def resolve_type(self, type_: Type) -> Type:
        if isinstance(type_, TypeVariable):
            if type_.instance is None:
                return type_
            return self.resolve_type(type_.instance)
        elif isinstance(type_, FunctionType):
            return FunctionType(
                [self.resolve_type(param_type) for param_type in type_.param_types],
                self.resolve_type(type_.return_type)
            )
        return type_