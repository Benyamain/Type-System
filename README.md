# Type System

Type System is a simple implementation of a type system in Python, designed to help understand the basics of type theory and type systems in programming languages.

## Features

- Custom language with integer, boolean, and function types
- Parser to convert code into an Abstract Syntax Tree (AST)
- Type checker to ensure type consistency
- Type inference system
- Lambda functions support
- Simple example programs to demonstrate the type system in action

## Project Structure

```
Type-System/
│
│── README.md
|── language-spec.md
│── requirements.txt
|── environment.yml
│── abstract_syntax_tree.py
│── parse.py
│── type_checker.py
│── type_inferencer.py
│── main.py
```

## Setup

1. Ensure you have Python 3.7 or later installed on your system.
2. Clone this repository:
   ```
   git clone https://github.com/benyamain/Type-System.git
   cd Type-System
   ```

## Usage

To run the example program and see the type checker and inferencer in action, use the following command:

```
python -m main
```

This will run the example program, perform type checking, and show the inferred types.

## Components

### Abstract Syntax Tree (AST)

The AST is defined in `abstract_syntax_tree.py`. It includes classes for different types of expressions, declarations, and types.

### Parser

The parser in `parse.py` converts the input program text into an AST. It supports parsing of declarations, expressions, and types.

### Type Checker

The type checker in `type_checker.py` ensures type consistency in the program. It checks declarations and expressions, including lambda functions.

### Type Inferencer

The type inferencer in `type_inferencer.py` infers types for expressions and declarations when type annotations are not provided.

## Example Program

The example program in `main.py` demonstrates various features of the type system:

```python
let x: Int = 5
let y: Int = 10
let add: (Int, Int) -> Int = (a, b) -> a + b
let result = add(x, y)
let is_positive = (n) -> n > 0
let check = is_positive(result)
```

This program showcases integer literals, function declarations with type annotations, lambda functions, and type inference.

## Extending the Project

1. Add more complex types, such as lists or records
2. Implement more advanced type inference algorithms
3. Add support for polymorphic types
4. Implement a simple interpreter for the language
5. Add more example programs to demonstrate different aspects of the type system

## Acknowledgments

This project was created as a learning exercise in type theory and type systems. It was inspired by various resources on programming language theory and type systems.