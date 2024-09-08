import re
from typing import List, Union
from .abstract_syntax_tree import *

class Parser:
    def __init__(self, text: str):
        self.tokens = self.tokenize(text)
        self.current = 0

    def tokenize(self, text: str) -> List[str]:
        token_specification = [
            ('NUMBER', r'\d+'),
            ('BOOLEAN',  r'True|False'),
            ('TYPE',     r'Int|Bool'),
            ('LET',      r'let'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('OPERATOR', r'[+\-*/==<>]'),
            ('ARROW',    r'->'),
            ('LPAREN',   r'\('),
            ('RPAREN',   r'\)'),
            ('COLON',    r':'),
            ('COMMA',    r','),
            ('EQUALS',   r'='),
            ('WHITESPACE', r'\s+'),
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        return [m.group() for m in re.finditer(tok_regex, text) if m.lastgroup != 'WHITESPACE']
    
    def parse_program(self) -> Program:
        statements= []
        while self.current < len(self.tokens):
            if self.match('LET'):
                statements.append(self.parse_declaration())
            else:
                statements.append(self.parse_expression())
            return Program(statements)
        
    def parse_declaration(self) -> Declaration:
        self.consume('LET')
        name = self.consume('IDENTIFIER')
        self.consume('COLON')
        type_annotation = self.parse_type()
        self.consume('EQUALS')
        value = self.parse_expression()
        return Declaration(name, type_annotation, value)
    
    def parse_type(self) -> Type:
        if self.match('TYPE'):
            type_name = self.consume()
            return IntType() if type_name == 'Int' else BoolType()
        elif self.match('LPAREN'):
            self.consume('LPAREN')
            param_types = [self.parse_type()]
            while self.match('COMMA'):
                self.consume('COMMA')
                param_types.append(self.parse_type())
            self.consume('RPAREN')
            self.consume('ARROW')
            return_type = self.parse_type()
            return FunctionType(param_types, return_type)
        else:
            raise SyntaxError(f"Unexpected token: {self.tokens[self.current]}")
        
    def parse_expression(self) -> Expression:
        return self.parse_binary_operation()
    
    def parse_binary_operation(self) -> Expression:
        left = self.parse_primary()
        while self.match('OPERATOR'):
            operator = self.consume('OPERATOR')
            right = self.parse_primary()
            left = BinaryOperation(left, operator, right)
        return left
    
    def parse_primary(self) -> Expression:
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
            expr = self.parse_expression()
            self.consume('RPAREN')
            return expr
        else:
            raise SyntaxError(f"Unexpected token: {self.tokens[self.current]}")
        
    def parse_function_call(self, function_name: str) -> FunctionCall:
        self.consume('LPAREN')
        arguments = [self.parse_expression()]
        while self.match('COMMA'):
            self.consume('COMMA')
            arguments.append(self.parse_expression())
        self.consume('RPAREN')
        return FunctionCall(Variable(function_name), arguments)
    
    def match(self, expected: str) -> bool:
        return self.current < len(self.tokens) and re.match(expected, self.tokens[self.current])
    
    def consume(self, expected: str = None) -> str:
        if expected and not self.match(expected):
            raise SyntaxError(f"Expected {expected}, got {self.tokens[self.current]}")
        token = self.tokens[self.current]
        self.current += 1
        return token