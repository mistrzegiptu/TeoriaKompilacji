import sys
from scanner import Scanner
from parser import Mparser
from TypeChecker import TypeChecker
from Interpreter import Interpreter

if __name__ == '__main__':

    filename = sys.argv[1] if len(sys.argv) > 1 else "examples/opers.m"
    try:
        with open(filename, "r") as file:
            text = file.read()
    except IOError:
        print(f"Cannot open file: {filename}")
        sys.exit(0)

    lexer = Scanner()
    parser = Mparser()
    
    ast = parser.parse(lexer.tokenize(text))
    
    if ast:
        # 1. Semantic Analysis
        typeChecker = TypeChecker()
        typeChecker.visit(ast)
        
        # 2. Interpretation (only if no semantic errors)
        if not typeChecker.errors_found:
            interpreter = Interpreter()
            interpreter.visit(ast)
        else:
            print("Interpretation skipped due to semantic errors.")