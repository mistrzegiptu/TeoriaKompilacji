

class Node(object):
    def __init__(self):
        self.lineno = 0 

    def accept(self, visitor):
        return visitor.visit(self)

class IntNum(Node):
    def __init__(self, value):
        self.value = value

class FloatNum(Node):
    def __init__(self, value):
        self.value = value

class String(Node):
    def __init__(self, value):
        self.value = value

class Variable(Node):
    def __init__(self, name):
        self.name = name

class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class RelExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Assignment(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class If(Node):
    def __init__(self, condition, true_body, false_body=None):
        self.condition = condition
        self.true_body = true_body
        self.false_body = false_body

class While(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class For(Node):
    def __init__(self, var, range_expr, body):
        self.var = var
        self.range_expr = range_expr
        self.body = body

class Range(Node):
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Break(Node):
    pass

class Continue(Node):
    pass

class Return(Node):
    def __init__(self, expression):
        self.expression = expression

class Print(Node):
    def __init__(self, print_vals):
        self.print_vals = print_vals

class Matrix(Node):
    def __init__(self, rows):
        self.rows = rows

class MatrixFunction(Node):
    def __init__(self, func_name, expression):
        self.func_name = func_name
        self.expression = expression

class Transposition(Node):
    def __init__(self, expression):
        self.expression = expression

class VectorElement(Node):
    def __init__(self, name, index):
        self.name = name
        self.index = index

class MatrixElement(Node):
    def __init__(self, name, row_index, col_index):
        self.name = name
        self.row_index = row_index
        self.col_index = col_index

class Uminus(Node):
    def __init__(self, expression):
        self.expression = expression

class Symbol(Node):
    def __init__(self, name):
        self.name = name

class Apply(Node):
    def __init__(self, function, args):
        self.function = function
        self.args = args

class Assign(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Error(Node):
    def __init__(self):
        pass
      
