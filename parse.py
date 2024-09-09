import re
from typing import List, Union
from abstract_syntax_tree import *

class Parser:
    def __init__(self, text: str):
        self.tokens = self.tokenize(text)
        self.current = 0

    def tokenize(self, text: str) -> List[str]:
        token_specification = [
            ('NUMBER',   r'\d+'),
            ('BOOLEAN',  r'True|False'),
            ('TYPE',     r'Int|Bool'),
            ('LET',      r'let'),
            ('ARROW',    r'->'),
            ('OPERATOR', r'[+\-*/==<>]'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('LPAREN',   r'\('),
            ('RPAREN',   r'\)'),
            ('COLON',    r':'),
            ('COMMA',    r','),
            ('EQUALS',   r'='),
            ('WHITESPACE', r'\s+'),
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        return [m.group() for m in re.finditer(tok_regex, text) if m.lastgroup != 'WHITESPACE']

    def parse_program(self):
        statements = []
        while self.current < len(self.tokens):
            if self.match('LET'):
                statements.append(self.parse_declaration())
            else:
                statements.append(self.parse_expression())
        return Program(statements)
    
    def parse_declaration(self):
        self.consume('LET')
        name = self.consume('IDENTIFIER')
        
        if self.match('COLON'):
            self.consume('COLON')
            type_annotation = self.parse_type()
        else:
            type_annotation = None
        
        self.consume('EQUALS')
        value = self.parse_expression()
        return Declaration(name, type_annotation, value)

    def parse_type(self):
        if self.match('TYPE'):
            type_name = self.consume('TYPE')
            return IntType() if type_name == 'Int' else BoolType()
        elif self.match('LPAREN'):
            self.consume('LPAREN')
            param_types = []
            while not self.match('RPAREN'):
                param_types.append(self.parse_type())
                if not self.match('RPAREN'):
                    self.consume('COMMA')
            self.consume('RPAREN')
            self.consume('ARROW')
            return_type = self.parse_type()
            return FunctionType(param_types, return_type)
        else:
            raise SyntaxError(f"Unexpected token in type: {self.tokens[self.current]} at position {self.current}")

    def match(self, expected):
        if self.current < len(self.tokens):
            token_type = self.get_token_type(self.tokens[self.current])
            return token_type == expected
        return False

    def consume(self, expected):
        if self.match(expected):
            token = self.tokens[self.current]
            self.current += 1
            return token
        else:
            raise SyntaxError(f"Expected {expected}, got {self.tokens[self.current]} at position {self.current}")

    def get_token_type(self, token):
        if token == 'let':
            return 'LET'
        if token == '->':
            return 'ARROW'
        if token in ['+', '-', '*', '/', '==', '<', '>']:
            return 'OPERATOR'
        if token.isdigit():
            return 'NUMBER'
        if token in ['True', 'False']:
            return 'BOOLEAN'
        if token in ['Int', 'Bool']:
            return 'TYPE'
        if token == '(':
            return 'LPAREN'
        if token == ')':
            return 'RPAREN'
        if token == ':':
            return 'COLON'
        if token == '=':
            return 'EQUALS'
        if token == ',':
            return 'COMMA'
        if token == '->':
            return 'ARROW'
        if token.isidentifier():
            return 'IDENTIFIER'
        return 'UNKNOWN'

    def parse_expression(self) -> Expression:
        return self.parse_binary_op()

    def parse_binary_op(self) -> Expression:
        left = self.parse_primary()
        while self.match('OPERATOR'):
            operator = self.consume('OPERATOR')
            right = self.parse_primary()
            left = BinaryOp(left, operator, right)
        return left

    def parse_primary(self) -> Expression:
        print(f"parse_primary: Current token: {self.tokens[self.current]}")  # Debug print
        if self.match('NUMBER'):
            return IntLiteral(int(self.consume('NUMBER')))
        elif self.match('BOOLEAN'):
            return BoolLiteral(self.consume('BOOLEAN') == 'True')
        elif self.match('IDENTIFIER'):
            name = self.consume('IDENTIFIER')
            if self.match('LPAREN'):
                return self.parse_function_call(name)
            return Variable(name)
        elif self.match('LPAREN'):
            self.consume('LPAREN')
            if self.match('IDENTIFIER'):
                # This might be a lambda function.
                params = []
                while not self.match('RPAREN'):
                    params.append(self.consume('IDENTIFIER'))
                    if self.match('COMMA'):
                        self.consume('COMMA')
                self.consume('RPAREN')
                if self.match('ARROW'):
                    self.consume('ARROW')
                    body = self.parse_expression()
                    return LambdaFunction(params, body)
            # If it's not a lambda, it's a regular parenthesized expression.
            expr = self.parse_expression()
            self.consume('RPAREN')
            return expr
        else:
            raise SyntaxError(f"Unexpected token: {self.tokens[self.current]}")

    def parse_function_call(self, function_name: str) -> FunctionCall:
        print(f"parse_function_call: Current token: {self.tokens[self.current]}")  # Debug print
        self.consume('LPAREN')
        arguments = []
        if not self.match('RPAREN'):
            arguments.append(self.parse_expression())
            while self.match('COMMA'):
                self.consume('COMMA')
                arguments.append(self.parse_expression())
        self.consume('RPAREN')
        return FunctionCall(Variable(function_name), arguments)