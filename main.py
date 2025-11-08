import sys
from scanner import Scanner
from parser import Mparser


if __name__ == '__main__':

    lexer = Scanner()
    parser = Mparser()

    filename = sys.argv[1] if len(sys.argv) > 1 else "examples/example.txt"
    with open(filename, "r") as file:
        text = file.read()

    parser.parse(lexer.tokenize(text))
