from abstract_syntax_tree import *
from type_inferencer import TypeVariable
from contextlib import contextmanager

class TypeError(Exception):
    pass

class TypeChecker:
    def __init__(self):
        self.environment = {}

    def check_program(self, program: Program):
        for statement in program.statements:
            if isinstance(statement, Declaration):
                self.check_declaration(statement)
            elif isinstance(statement, Expression):
                self.check_expression(statement)

    def check_declaration(self, declaration: Declaration):
        actual_type = self.check_expression(declaration.value)
        if declaration.type_annotation is None:
            # If there's no type annotation, infer the type from the value.
            declaration.type_annotation = actual_type
        elif not self.types_equal(actual_type, declaration.type_annotation):
            raise TypeError(f"Type mismatch in declaration of {declaration.name}: "
                            f"expected {declaration.type_annotation}, got {actual_type}")
        self.environment[declaration.name] = declaration.type_annotation

    def check_expression(self, expr: Expression) -> Type:
        if isinstance(expr, IntLiteral):
            return IntType()
        elif isinstance(expr, BoolLiteral):
            return BoolType()
        elif isinstance(expr, Variable):
            if expr.name not in self.environment:
                raise TypeError(f"Undefined variable: {expr.name}")
            return self.environment[expr.name]
        elif isinstance(expr, BinaryOp):
            left_type = self.check_expression(expr.left)
            right_type = self.check_expression(expr.right)
            if expr.operator in ['+', '-', '*', '/']:
                if not self.is_int_type(left_type) or not self.is_int_type(right_type):
                    raise TypeError(f"Arithmetic operation requires Int types, got {left_type} and {right_type}")
                return IntType()
            elif expr.operator in ['==', '<', '>']:
                if not self.types_equal(left_type, right_type):
                    raise TypeError(f"Comparison requires matching types, got {left_type} and {right_type}")
                return BoolType()
        elif isinstance(expr, FunctionCall):
            func_type = self.check_expression(expr.function)
            if not isinstance(func_type, FunctionType):
                raise TypeError(f"Calling non-function type: {func_type}")
            if len(expr.arguments) != len(func_type.param_types):
                raise TypeError(f"Function call with wrong number of arguments: "
                                f"expected {len(func_type.param_types)}, got {len(expr.arguments)}")
            for arg, param_type in zip(expr.arguments, func_type.param_types):
                arg_type = self.check_expression(arg)
                if not self.types_equal(arg_type, param_type):
                    raise TypeError(f"Function argument type mismatch: expected {param_type}, got {arg_type}")
            return func_type.return_type
        elif isinstance(expr, LambdaFunction):
            lambda_env = self.environment.copy()
            param_types = [TypeVariable() for _ in expr.parameters]
            for param, param_type in zip(expr.parameters, param_types):
                lambda_env[param] = param_type
            
            with self.scoped_environment(lambda_env):
                body_type = self.check_expression(expr.body)
            
            return FunctionType(param_types, body_type)
        else:
            raise TypeError(f"Unknown expression type: {type(expr)}")

    def types_equal(self, type1: Type, type2: Type) -> bool:
        if isinstance(type1, TypeVariable) or isinstance(type2, TypeVariable):
            return True  # Assume type variables can be equal to any type.
        if type(type1) != type(type2):
            return False
        if isinstance(type1, FunctionType):
            return (len(type1.param_types) == len(type2.param_types) and
                    all(self.types_equal(t1, t2) for t1, t2 in zip(type1.param_types, type2.param_types)) and
                    self.types_equal(type1.return_type, type2.return_type))
        return True

    def is_int_type(self, type_: Type) -> bool:
        return isinstance(type_, IntType) or isinstance(type_, TypeVariable)

    @contextmanager
    def scoped_environment(self, new_env):
        old_env = self.environment
        self.environment = new_env
        try:
            yield
        finally:
            self.environment = old_env