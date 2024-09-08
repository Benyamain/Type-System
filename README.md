# Type System

Type System is a simple implementation of a type system in Python, designed to help understand the basics of type theory and type systems in programming languages.

## Features

- Custom language with integer, boolean, and function types
- Parser to convert code into an Abstract Syntax Tree (AST)
- Type checker to ensure type consistency
- Basic type inference system
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
│── type-checker.py
│── type-inferencer.py
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
python -m Type-System.main
```

This will run the example program, perform type checking, and show the inferred types.

## Extending the Project

1. Add more complex types, such as lists or records
2. Implement more advanced type inference algorithms
3. Add support for polymorphic types
4. Implement a simple interpreter for the language
5. Add more example programs to demonstrate different aspects of the type system

## Acknowledgments

This project was created as a learning exercise in type theory and type systems. It was inspired by various resources on programming language theory and type systems.