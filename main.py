import sys
from TreePrinter import *
from scanner import Scanner
from parser import Mparser
from AST import *
from TypeChecker import *


if __name__ == '__main__':

    filename = sys.argv[1] if len(sys.argv) > 1 else "examples/init.m"
    with open(filename, "r") as file:
        text = file.read()


    lexer = Scanner()
    parser = Mparser()
    
    ast = parser.parse(lexer.tokenize(text))
    
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    #ast.printTree()
    #treePrinter = TreePrinter()
    
    # for tok in lexer.tokenize(text):
    #     print(f"{tok.lineno}: {tok.type}({tok.value})")

    TreePrinter.print_list(ast)