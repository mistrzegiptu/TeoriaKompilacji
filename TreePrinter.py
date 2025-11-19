import AST

def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print("|  " * indent + str(self.value))

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print("|  " * indent + str(self.value))

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print("|  " * indent + f'"{self.value}"')

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print("|  " * indent + self.name)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print("|  " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.RelExpr)
    def printTree(self, indent=0):
        print("|  " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Assign)
    def printTree(self, indent=0):
        print("|  " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        print("|  " * indent + "IF")
        self.condition.printTree(indent + 1)
        self.true_body.printTree(indent + 1)
        if self.false_body:
            print("|  " * indent + "ELSE")
            self.false_body.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        print("|  " * indent + "WHILE")
        self.condition.printTree(indent + 1)
        self.body.printTree(indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        print("|  " * indent + "FOR")
        self.var.printTree(indent + 1)
        self.range_expr.printTree(indent + 1)
        self.body.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print("|  " * indent + "RANGE")
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        print("|  " * indent + "BREAK")

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        print("|  " * indent + "CONTINUE")

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print("|  " * indent + "RETURN")
        self.expression.printTree(indent + 1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        print("|  " * indent + "PRINT")
        for expr in self.print_vals:
            expr.printTree(indent + 1)

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        print("|  " * indent + "MATRIX")
        for row in self.rows:
            if isinstance(row, list):
                for elem in row:
                    elem.printTree(indent + 1)
            else:
                row.printTree(indent + 1)

    @addToClass(AST.MatrixFunction)
    def printTree(self, indent=0):
        print("|  " * indent + self.func_name)
        self.expression.printTree(indent + 1)

    @addToClass(AST.Transposition)
    def printTree(self, indent=0):
        print("|  " * indent + "TRANSPOSE")
        self.expression.printTree(indent + 1)

    @addToClass(AST.VectorElement)
    def printTree(self, indent=0):
        print("|  " * indent + "VECTOR_ELEMENT")
        print("|  " * (indent + 1) + self.name)
        self.index.printTree(indent + 1)

    @addToClass(AST.MatrixElement)
    def printTree(self, indent=0):
        print("|  " * indent + "MATRIX_ELEMENT")
        print("|  " * (indent + 1) + self.name)
        self.row_index.printTree(indent + 1)
        self.col_index.printTree(indent + 1)

    @addToClass(AST.Uminus)
    def printTree(self, indent=0):
        print("|  " * indent + "UMINUS")
        self.expression.printTree(indent + 1)

    @addToClass(AST.Symbol)
    def printTree(self, indent=0):
        print("|  " * indent + self.name)

    @addToClass(AST.Apply)
    def printTree(self, indent=0):
        print("|  " * indent + "APPLY")
        self.function.printTree(indent + 1)
        for arg in self.args:
            arg.printTree(indent + 1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        print("|  " * indent + "ERROR")

    # Handle list of instructions
    @staticmethod
    def print_list(nodes, indent=0):
        for node in nodes:
            if isinstance(node, list):
                TreePrinter.print_list(node, indent)
            else:
                node.printTree(indent)