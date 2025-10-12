import sys
from sly import Lexer

class Scanner(Lexer):

    tokens = {ID, FLOATNUM, INTNUM, DOTADD, DOTSUB, DOTMUL, DOTDIV, ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN,
              IF, ELSE, FOR, WHILE, PRINT, BREAK, CONTINUE, RETURN, EYE, ZEROS, ONES, 
              EQ, LT, LE, GT, GE, NE}
    literals = {'+', '-', '*', '/', '=', ';', ':', '.', ',', '\"', '(', ')', '[', ']', '{', '}', '\''}

    ignore = ' \t'

    FLOATNUM = r'[+-]?(\d+(\.\d*)([eE][+-]?\d+)?|\.\d+([eE][+-]?\d+)?)'
    INTNUM = r'[+-]?[0-9]+'
    DOTADD = r'\.\+'
    DOTSUB = r'\.-'
    DOTMUL = r'\.\*'
    DOTDIV = r'\./'
    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'/='
    EQ = r'=='
    LE      = r'<='
    LT      = r'<'
    GE      = r'>='
    GT      = r'>'
    NE      = r'!='

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['for'] = FOR
    ID['while'] = WHILE
    ID['print'] = PRINT
    ID['break'] = BREAK
    ID['continue'] = CONTINUE
    ID['return'] = RETURN
    ID['eye'] = EYE
    ID['zeros'] = ZEROS
    ID['ones'] = ONES

    ignore_comment = r'\#.*'
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

if __name__ == '__main__':

    lexer = Scanner()

    filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
    with open(filename, "r") as file:
        text = file.read()

    for tok in lexer.tokenize(text):
        print(f"{tok.lineno}: {tok.type}({tok.value})")