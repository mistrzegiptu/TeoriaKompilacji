import AST
from Memory import *
from Exceptions import *
from visit import *
import sys

sys.setrecursionlimit(10000)

def mat_add(A, B):
    return [[a + b for a, b in zip(rowA, rowB)] for rowA, rowB in zip(A, B)]

def mat_sub(A, B):
    return [[a - b for a, b in zip(rowA, rowB)] for rowA, rowB in zip(A, B)]

def mat_mul(A, B):
    zip_b = list(zip(*B))
    return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b)) 
             for col_b in zip_b] for row_a in A]

def mat_dot_mul(A, B):
    return [[a * b for a, b in zip(rowA, rowB)] for rowA, rowB in zip(A, B)]

def mat_dot_div(A, B):
    return [[a / b for a, b in zip(rowA, rowB)] for rowA, rowB in zip(A, B)]

class Interpreter(object):

    def __init__(self):
        self.memoryStack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(list)
    def visit(self, node):
        r = None
        for elem in node:
            r = self.visit(elem)
        return r

    @when(AST.IntNum)
    def visit(self, node):
        return int(node.value)

    @when(AST.FloatNum)
    def visit(self, node):
        return float(node.value)

    @when(AST.String)
    def visit(self, node):
        return node.value[1:-1]

    @when(AST.Variable)
    def visit(self, node):
        return self.memoryStack.get(node.name)

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)
        
        if isinstance(r1, str) or isinstance(r2, str):
            if node.op == '*':
                return r1 * r2
            elif node.op == '+':
                return r1 + r2
            else:
                 raise Exception(f"Operation {node.op} not supported for strings in interpreter")
            
        is_matrix = isinstance(r1, list) and isinstance(r2, list)

        if node.op == '+':
            return mat_add(r1, r2) if is_matrix else r1 + r2
        elif node.op == '-':
            return mat_sub(r1, r2) if is_matrix else r1 - r2
        elif node.op == '*':
            return mat_mul(r1, r2) if is_matrix else r1 * r2
        elif node.op == '/':
            return r1 / r2
        elif node.op == '.+':
            return mat_add(r1, r2)
        elif node.op == '.-':
            return mat_sub(r1, r2)
        elif node.op == '.*':
            return mat_dot_mul(r1, r2)
        elif node.op == './':
            return mat_dot_div(r1, r2)
        
        return None

    @when(AST.RelExpr)
    def visit(self, node):
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)
        if node.op == '==': return r1 == r2
        if node.op == '!=': return r1 != r2
        if node.op == '<': return r1 < r2
        if node.op == '>': return r1 > r2
        if node.op == '<=': return r1 <= r2
        if node.op == '>=': return r1 >= r2
        return False

    @when(AST.Assign)
    def visit(self, node):
        val = self.visit(node.right)
        
        if isinstance(node.left, AST.Variable):
            if node.op == '=':
                self.memoryStack.set(node.left.name, val)
            else:
                current_val = self.memoryStack.get(node.left.name)
                if node.op == '+=': new_val = current_val + val
                elif node.op == '-=': new_val = current_val - val
                elif node.op == '*=': new_val = current_val * val
                elif node.op == '/=': new_val = current_val / val
                self.memoryStack.set(node.left.name, new_val)

        elif isinstance(node.left, (AST.VectorElement, AST.MatrixElement)):
            matrix_name = node.left.name
            matrix = self.memoryStack.get(matrix_name)
            
            if isinstance(node.left, AST.VectorElement):
                idx = self.visit(node.left.index)
                matrix[idx] = val
            elif isinstance(node.left, AST.MatrixElement):
                r = self.visit(node.left.row_index)
                c = self.visit(node.left.col_index)
                matrix[r][c] = val

    @when(AST.If)
    def visit(self, node):
        if self.visit(node.condition):
            self.memoryStack.push(Memory("if"))
            try:
                self.visit(node.true_body) 
            finally:
                self.memoryStack.pop()
        elif node.false_body:
            self.memoryStack.push(Memory("else"))
            try:
                self.visit(node.false_body)
            finally:
                self.memoryStack.pop()

    @when(AST.While)
    def visit(self, node):
        while self.visit(node.condition):
            self.memoryStack.push(Memory("while"))
            try:
                self.visit(node.body)
            except BreakException:
                self.memoryStack.pop()
                break
            except ContinueException:
                self.memoryStack.pop()
                continue
            self.memoryStack.pop()

    @when(AST.For)
    def visit(self, node):
        start, end = self.visit(node.range_expr)
        step = 1 if start <= end else -1
        rng = range(start, end + step, step)
        
        for i in rng:
            self.memoryStack.push(Memory("for"))
            self.memoryStack.insert(node.var.name, i)
            try:
                self.visit(node.body)
            except BreakException:
                self.memoryStack.pop()
                break
            except ContinueException:
                self.memoryStack.pop()
                continue
            self.memoryStack.pop()

    @when(AST.Range)
    def visit(self, node):
        return self.visit(node.start), self.visit(node.end)

    @when(AST.Print)
    def visit(self, node):
        vals = [self.visit(v) for v in node.print_vals]
        print(*vals)

    @when(AST.Matrix)
    def visit(self, node):
        return [[self.visit(e) for e in row] for row in node.rows]

    @when(AST.MatrixFunction)
    def visit(self, node):
        rows = self.visit(node.dim1)
        cols = self.visit(node.dim2) if node.dim2 else rows
        
        if node.func_name == 'zeros':
            return [[0]*cols for _ in range(rows)]
        
        if node.func_name == 'ones':
            return [[1]*cols for _ in range(rows)]
        
        if node.func_name == 'eye':
            return [[1 if i == j else 0 for j in range(cols)] for i in range(rows)]

    @when(AST.Transposition)
    def visit(self, node):
        mat = self.visit(node.expression)
        return [list(x) for x in zip(*mat)]

    @when(AST.Uminus)
    def visit(self, node):
        v = self.visit(node.expression)
        if isinstance(v, list):
            return [[-x for x in row] for row in v]
        return -v

    @when(AST.VectorElement)
    def visit(self, node):
        idx = self.visit(node.index)
        return self.memoryStack.get(node.name)[idx]

    @when(AST.MatrixElement)
    def visit(self, node):
        r = self.visit(node.row_index)
        c = self.visit(node.col_index)
        return self.memoryStack.get(node.name)[r][c]

    @when(AST.Break)
    def visit(self, node):
        raise BreakException()

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException()
        
    @when(AST.Return)
    def visit(self, node):
        val = self.visit(node.expression)
        print(f"RETURN: {val}")
        sys.exit(0)