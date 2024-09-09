from parse import Parser
from abstract_syntax_tree import Program, Declaration, Expression
from type_checker import TypeChecker
from type_inferencer import TypeInferencer

def main():
    program = """
    let x: Int = 5
    let y: Int = 10
    let add: (Int, Int) -> Int = (a, b) -> a + b
    let result = add(x, y)
    let is_positive = (n) -> n > 0
    let check = is_positive(result)
    """

    parser = Parser(program)
    ast = parser.parse_program()

    type_checker = TypeChecker()
    try:
        type_checker.check_program(ast)
        print("Type checking passed!")
    except TypeError as e:
        print(f"Type checking failed: {e}")

    type_inferencer = TypeInferencer()
    try:
        type_inferencer.infer_program(ast)
        print("\nInferred types:")
        for name, type_ in type_inferencer.type_env.items():
            print(f"{name}: {type_}")
    except TypeError as e:
        print(f"Type inference failed: {e}")

if __name__ == "__main__":
    main()