from sly import Parser
from scanner import Scanner
from AST import *

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
        return p.instructions_opt

    @_('instructions')
    def instructions_opt(self, p):
        return p.instructions

    @_('')
    def instructions_opt(self, p):
        return []

    @_('instructions instruction')
    def instructions(self, p):
        return p.instructions + [p.instruction]

    @_('instruction')
    def instructions(self, p):
        return [p.instruction]

    @_('assignment ";"')
    def instruction(self, p):
        return p.assignment
    
    @_('statement ";"')
    def instruction(self, p):
        return p.statement
    
    @_('"{" instructions "}"')
    def instruction(self, p):
        return p.instructions

    @_('IF "(" condition ")" instruction %prec IFX')
    def instruction(self, p):
        return If(p.condition, p.instruction)

    @_('IF "(" condition ")" instruction ELSE instruction')
    def instruction(self, p):
        return If(p.condition, p.instruction0, p.instruction1)

    @_('WHILE "(" condition ")" instruction')
    def instruction(self, p):
        return While(p.condition, p.instruction)

    @_('FOR var "=" range instruction')
    def instruction(self, p):
        return For(p.var, p.range, p.instruction)

    @_('expression ":" expression')
    def range(self, p):
        return Range(p.expression0, p.expression1)
    
    @_('expression EQ expression', 'expression NE expression', 'expression LE expression', 'expression GE expression', 'expression ">" expression', 'expression "<" expression')
    def condition(self, p):
        return RelExpr(p[1], p.expression0, p.expression1)

    @_('MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN', '"="')
    def assignment_op(self, p):
        return p[0]

    @_('var assignment_op expression')
    def assignment(self, p):
        return Assign(p.var, p.assignment_op, p.expression)

    @_('matrix_element assignment_op expression')
    def assignment(self, p):
        return Assign(p.matrix_element, p.assignment_op, p.expression)

    @_('vector_element assignment_op expression')
    def assignment(self, p):
        return Assign(p.vector_element, p.assignment_op, p.expression)

    @_('matrix_function_name "(" expression ")"')
    def matrix_function(self, p):
        return MatrixFunction(p.matrix_function_name, p.expression)

    @_('EYE', 'ONES', 'ZEROS')
    def matrix_function_name(self, p):
        return p[0]

    @_('"[" rows "]"')
    def matrix(self, p):
        return Matrix(p.rows)

    @_('rows ";" row')
    def rows(self, p):
        return p.rows + [p.row]

    @_('row')
    def rows(self, p):
        return [p.row]

    @_('variables')
    def row(self, p):
        return p.variables

    @_('variables "," variable')
    def variables(self, p):
        return p.variables + [p.variable]

    @_('variable')
    def variables(self, p):
        return [p.variable]

    @_('number')
    def variable(self, p):
        return p.number

    @_('var')
    def variable(self, p):
        return p.var

    @_('element')
    def variable(self, p):
        return p.element

    @_('"-" expression %prec UMINUS')
    def uminus(self, p):
        return Uminus(p.expression)

    @_('matrix_element')
    def element(self, p):
        return p.matrix_element

    @_('vector_element')
    def element(self, p):
        return p.vector_element

    @_('ID "[" expression "]"')
    def vector_element(self, p):
        return VectorElement(p.ID, p.expression)

    @_('ID "[" expression "," expression "]"')
    def matrix_element(self, p):
        return MatrixElement(p.ID, p.expression0, p.expression1)

    @_('ID')
    def var(self, p):
        return Variable(p.ID)

    @_('FLOATNUM')
    def number(self, p):
        return FloatNum(p.FLOATNUM)

    @_('INTNUM')
    def number(self, p):
        return IntNum(p.INTNUM)

    @_('STRING')
    def string(self, p):
        return String(p.STRING)

    @_('CONTINUE')
    def statement(self, p):
        return Continue()

    @_('BREAK')
    def statement(self, p):
        return Break()

    @_('RETURN expression')
    def statement(self, p):
        return Return(p.expression)

    @_('expression "+" expression', 'expression "-" expression', 'expression "*" expression', 'expression "/" expression', 'expression DOTADD expression', 'expression DOTSUB expression', 'expression DOTMUL expression', 'expression DOTDIV expression')
    def expression(self, p):
        return BinExpr(p[1], p.expression0, p.expression1)

    @_('num_expression')
    def expression(self, p):
        return p.num_expression

    @_('matrix')
    def expression(self, p):
        return p.matrix

    @_('matrix_function')
    def expression(self, p):
        return p.matrix_function

    @_('transposition')
    def expression(self, p):
        return p.transposition

    @_('matrix_element')
    def expression(self, p):
        return p.matrix_element

    @_('vector_element')
    def expression(self, p):
        return p.vector_element

    @_('uminus')
    def expression(self, p):
        return p.uminus

    @_('number')
    def num_expression(self, p):
        return p.number

    @_('var')
    def num_expression(self, p):
        return p.var

    @_('expression "\'"')
    def transposition(self, p):
        return Transposition(p.expression)

    @_('PRINT print_vals')
    def statement(self, p):
        return Print(p.print_vals)

    @_('print_vals "," print_val')
    def print_vals(self, p):
        return p.print_vals + [p.print_val]

    @_('print_val')
    def print_vals(self, p):
        return [p.print_val]

    @_('string')
    def print_val(self, p):
        return p.string

    @_('expression')
    def print_val(self, p):
        return p.expression

    def error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}: {p.type}('{p.value}')")
        else:
            print("Unexpected end of input")
