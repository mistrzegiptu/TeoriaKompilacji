from sly import Parser
from scanner import Scanner
from AST import *

class Mparser(Parser):

    tokens = Scanner.tokens
    debugfile = 'parser.out'

    precedence = (
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE'),
        ('nonassoc', '<', '>', 'EQ', 'NE', 'GE', 'LE'),
        ('left', '+', '-', 'DOTADD', 'DOTSUB'),
        ('left', '*', '/', 'DOTMUL', 'DOTDIV'),
        ('right', 'UMINUS'),
        ('left', "'"),
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
        node = If(p.condition, p.instruction)
        node.lineno = p.lineno
        return node

    @_('IF "(" condition ")" instruction ELSE instruction')
    def instruction(self, p):
        node = If(p.condition, p.instruction0, p.instruction1)
        node.lineno = p.lineno
        return node

    @_('WHILE "(" condition ")" instruction')
    def instruction(self, p):
        node = While(p.condition, p.instruction)
        node.lineno = p.lineno
        return node

    @_('FOR var "=" range instruction')
    def instruction(self, p):
        node = For(p.var, p.range, p.instruction)
        node.lineno = p.lineno
        return node

    @_('expression ":" expression')
    def range(self, p):
        return Range(p.expression0, p.expression1)
    
    @_('expression EQ expression', 
       'expression NE expression', 
       'expression LE expression', 
       'expression GE expression', 
       'expression ">" expression', 
       'expression "<" expression')
    def condition(self, p):
        node = RelExpr(p[1], p.expression0, p.expression1)
        node.lineno = p.expression0.lineno
        return node

    @_('MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN', '"="')
    def assignment_op(self, p):
        return p[0]

    @_('var assignment_op expression')
    def assignment(self, p):
        node = Assign(p.var, p.assignment_op, p.expression)
        node.lineno = p.lineno
        return node

    @_('matrix_element assignment_op expression')
    def assignment(self, p):
        node = Assign(p.matrix_element, p.assignment_op, p.expression)
        node.lineno = p.lineno
        return node

    @_('vector_element assignment_op expression')
    def assignment(self, p):
        node = Assign(p.vector_element, p.assignment_op, p.expression)
        node.lineno = p.lineno
        return node

    @_('matrix_function_name "(" expression ")"')
    def matrix_function(self, p):
        node = MatrixFunction(p.matrix_function_name, p.expression)
        node.lineno = p.lineno
        return node

    @_('matrix_function_name "(" expression "," expression ")"')
    def matrix_function(self, p):
        node = MatrixFunction(p.matrix_function_name, p.expression0, p.expression1)
        node.lineno = p.lineno
        return node

    @_('EYE', 'ONES', 'ZEROS')
    def matrix_function_name(self, p):
        return p[0]

    @_('"[" rows "]"')
    def matrix(self, p):
        node = Matrix(p.rows)
        node.lineno = p.lineno
        return node

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

    @_('number', 'var', 'element')
    def variable(self, p):
        return p[0]

    @_('"-" expression %prec UMINUS')
    def uminus(self, p):
        node = Uminus(p.expression)
        node.lineno = p.lineno
        return node

    @_('matrix_element')
    def element(self, p):
        return p.matrix_element

    @_('vector_element')
    def element(self, p):
        return p.vector_element

    @_('ID "[" expression "]"')
    def vector_element(self, p):
        node = VectorElement(p.ID, p.expression)
        node.lineno = p.lineno
        return node

    @_('ID "[" expression "," expression "]"')
    def matrix_element(self, p):
        node = MatrixElement(p.ID, p.expression0, p.expression1)
        node.lineno = p.lineno
        return node

    @_('ID')
    def var(self, p):
        node = Variable(p.ID)
        node.lineno = p.lineno
        return node

    @_('FLOATNUM')
    def number(self, p):
        node = FloatNum(p.FLOATNUM)
        node.lineno = p.lineno
        return node

    @_('INTNUM')
    def number(self, p):
        node = IntNum(p.INTNUM)
        node.lineno = p.lineno
        return node

    @_('STRING')
    def string(self, p):
        node = String(p.STRING)
        node.lineno = p.lineno
        return node

    @_('CONTINUE')
    def statement(self, p):
        node = Continue()
        node.lineno = p.lineno
        return node

    @_('BREAK')
    def statement(self, p):
        node = Break()
        node.lineno = p.lineno
        return node

    @_('RETURN expression')
    def statement(self, p):
        node = Return(p.expression)
        node.lineno = p.lineno
        return node

    @_('PRINT print_vals')
    def statement(self, p):
        node = Print(p.print_vals)
        node.lineno = p.lineno
        return node

    @_('print_vals "," print_val')
    def print_vals(self, p):
        return p.print_vals + [p.print_val]

    @_('print_val')
    def print_vals(self, p):
        return [p.print_val]

    @_('string', 'expression')
    def print_val(self, p):
        return p[0]

    @_('expression "+" expression', 
       'expression "-" expression', 
       'expression "*" expression', 
       'expression "/" expression', 
       'expression DOTADD expression', 
       'expression DOTSUB expression', 
       'expression DOTMUL expression', 
       'expression DOTDIV expression')
    def expression(self, p):
        node = BinExpr(p[1], p.expression0, p.expression1)
        node.lineno = p.lineno
        return node

    # --- ADDED: Rule for parentheses ---
    @_('"(" expression ")"')
    def expression(self, p):
        return p.expression

    @_('num_expression', 'matrix', 'matrix_function', 'transposition', 'matrix_element', 'vector_element', 'uminus')
    def expression(self, p):
        return p[0]

    @_('number', 'var')
    def num_expression(self, p):
        return p[0]

    @_('expression "\'"')
    def transposition(self, p):
        node = Transposition(p.expression)
        node.lineno = p.lineno
        return node

    def error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}, token={p.type}, value='{p.value}'")
        else:
            print("Unexpected end of input")