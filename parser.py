from sly import Parser
from scanner import Scanner

class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = 'parser.out'

    start = 'program'

    precedence = (
    # to fill ...
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE'),
        ('right', 'MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN'),
        ('nonassoc', 'EQ', 'NE', 'LE', 'GE', '>', '<'),
        ("left", '+', '-'),
        ("left", 'DOTADD', 'DOTSUB'),
        ("left", "*", "/"),
        ("left", 'DOTMUL', 'DOTDIV'),
        ("right", 'UMINUS'),
        ("left", "'")
    # to fill ...
    )


    @_('instructions_opt')
    def program(self, p):
        pass

    @_('instructions')
    def instructions_opt(self, p):
        pass

    @_('')
    def instructions_opt(self, p):
        pass

    @_('instructions instruction')
    def instructions(self, p):
        pass

    @_('instruction')
    def instructions(self, p):
        pass

    @_('assignment ";"', 'statement ";"', '"{" instructions "}"')
    def instruction(self, p):
        pass

    @_('IF "(" condition ")" instruction %prec IFX')
    def instruction(self, p):
        pass

    @_('IF "(" condition ")" instruction ELSE instruction')
    def instruction(self, p):
        pass

    @_('WHILE "(" condition ")" instruction')
    def instruction(self, p):
        pass

    @_('FOR var "=" range instruction')
    def instruction(self, p):
        pass

    @_('expression ":" expression')
    def range(self, p):
        pass
    
    @_('expression EQ expression', 'expression NE expression', 'expression LE expression', 'expression GE expression', 'expression ">" expression', 'expression "<" expression')
    def condition(self, p):
        pass

    @_('MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN', '"="')
    def assignment_op(self, p):
        pass

    @_('var assignment_op expression', 'matrix_element assignment_op expression', 'vector_element assignment_op expression')
    def assignment(self, p):
        pass

    @_('matrix_function_name "(" expression ")"')
    def matrix_function(self, p):
        pass

    @_('EYE', 'ONES', 'ZEROS')
    def matrix_function_name(self, p):
        pass

    @_('"[" rows "]"')
    def matrix(self, p):
        pass

    @_('rows ";" row', 'row')
    def rows(self, p):
        pass

    @_('variables')
    def row(self, p):
        pass

    @_('variables "," variable', 'variable')
    def variables(self, p):
        pass

    @_('number', 'var', 'element')
    def variable(self, p):
        pass

    @_('"-" expression %prec UMINUS')
    def uminus(self, p):
        pass

    @_('matrix_element', 'vector_element')
    def element(self, p):
        pass

    @_('ID "[" expression "]"')
    def vector_element(self, p):
        pass

    @_('ID "[" expression "," expression "]"')
    def matrix_element(self, p):
        pass

    @_('ID')
    def var(self, p):
        pass

    @_('FLOATNUM', 'INTNUM')
    def number(self, p):
        pass

    @_('STRING')
    def string(self, p):
        pass

    @_('CONTINUE')
    def statement(self, p):
        pass

    @_('BREAK')
    def statement(self, p):
        pass

    @_('RETURN expression')
    def statement(self, p):
        pass

    @_('expression "+" expression', 'expression "-" expression', 'expression "*" expression', 'expression "/" expression', 'expression DOTADD expression', 'expression DOTSUB expression', 'expression DOTMUL expression', 'expression DOTDIV expression')
    def expression(self, p):
        pass

    @_('num_expression', 'matrix', 'matrix_function', 'transposition', 'matrix_element', 'vector_element', 'uminus')
    def expression(self, p):
        pass

    @_('number', 'var')
    def num_expression(self, p):
        pass

    @_('expression "\'"')
    def transposition(self, p):
        pass

    @_('PRINT print_vals')
    def statement(self, p):
        pass

    @_('print_vals "," print_val',
       'print_val')
    def print_vals(self, p):
        pass

    @_('string', 'expression')
    def print_val(self, p):
        pass

    def error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}: {p.type}('{p.value}')")
        else:
            print("Unexpected end of input")
