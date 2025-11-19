import sys
from TreePrinter import *
from scanner import Scanner
from parser import Mparser
from AST import *


if __name__ == '__main__':

    filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
    with open(filename, "r") as file:
        text = file.read()


    lexer = Scanner()
    parser = Mparser()

    ast = parser.parse(lexer.tokenize(text))
    #ast.printTree()
    #treePrinter = TreePrinter()
    TreePrinter.print_list(ast)