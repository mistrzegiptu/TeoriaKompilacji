import AST
from SymbolTable import SymbolTable, Symbol

class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            pass

class TypeChecker(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable(None, "Global")
        self.loop_nesting = 0
        self.errors_found = False

    def print_error(self, node, msg):
        self.errors_found = True
        print(f"Error: {msg} at line {getattr(node, 'lineno', '?')}")

    def visit_IntNum(self, node):
        return 'int'

    def visit_FloatNum(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Variable(self, node):
        symbol = self.symbol_table.get(node.name)
        if symbol is None:
            self.print_error(node, f"Variable '{node.name}' not defined")
            return None
        return symbol.type

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op

        if type1 is None or type2 is None:
            return None

        dims1 = self.get_dims(node.left)
        dims2 = self.get_dims(node.right)

        if type1 == 'matrix' or type2 == 'matrix':
            if type1 != type2:
                self.print_error(node, f"Incompatible operands for '{op}': {type1} and {type2}")
                return None
            
            if op in ['+', '-']:
                if dims1 and dims2 and dims1 != dims2:
                    self.print_error(node, f"Matrix dimension mismatch {dims1} vs {dims2} for operation '{op}'")
                return 'matrix'
            
            elif op in ['.+', '.-', '.*', './']:
                 if dims1 and dims2 and dims1 != dims2:
                    self.print_error(node, f"Matrix dimension mismatch {dims1} vs {dims2} for dot operation '{op}'")
                 return 'matrix'
            
            elif op == '*':
                if dims1 and dims2 and dims1[1] != dims2[0]:
                    self.print_error(node, f"Invalid matrix dimensions for multiplication {dims1} vs {dims2}")
                return 'matrix'
            
            elif op == '/':
                 self.print_error(node, "Matrix division not supported")
                 return None

        if type1 == type2:
            return type1
        
        if (type1 == 'int' and type2 == 'float') or (type1 == 'float' and type2 == 'int'):
            return 'float'
        
        if type1 == 'string' and type2 == 'string' and op == '+':
            return 'string'

        self.print_error(node, f"Incompatible types {type1} and {type2} for '{op}'")
        return None
    
    def visit_RelExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        if not type1 or not type2:
            return None
        if type1 != type2:
            self.print_error(node, f"Comparison types mismatch {type1} vs {type2}")
        return 'boolean'

    def visit_Assign(self, node):
        type_right = self.visit(node.right)
        
        if isinstance(node.left, AST.Variable):
            dims = self.get_dims(node.right)
            self.symbol_table.put(node.left.name, Symbol(node.left.name, type_right, dims))
        
        elif isinstance(node.left, (AST.VectorElement, AST.MatrixElement)):
             self.visit(node.left)
             if type_right and type_right not in ['int', 'float']:
                 self.print_error(node, f"Cannot assign {type_right} to matrix element")

    def visit_Matrix(self, node):
        if not node.rows:
            return 'matrix'
        
        ref_len = len(node.rows[0])
        
        for i, row in enumerate(node.rows):
            if len(row) != ref_len:
                line = node.lineno
                if row and hasattr(row[0], 'lineno'):
                    line = row[0].lineno
                print(f"Error: Matrix initialization error: Row {i} has length {len(row)}, expected {ref_len} at line {line}")
                self.errors_found = True
            
            for elem in row:
                t = self.visit(elem)
                if t and t not in ['int', 'float']:
                    self.print_error(node, f"Matrix element must be int or float, found {t}")

        return 'matrix'

    def visit_MatrixFunction(self, node):
        t1 = self.visit(node.dim1)
        if t1 != 'int':
            self.print_error(node, f"First argument of '{node.func_name}' must be an integer")
        
        if node.dim2:
            t2 = self.visit(node.dim2)
            if t2 != 'int':
                self.print_error(node, f"Second argument of '{node.func_name}' must be an integer")
        
        return 'matrix'

    def visit_VectorElement(self, node):
        return self._check_bounds(node, 1)

    def visit_MatrixElement(self, node):
        return self._check_bounds(node, 2)

    def _check_bounds(self, node, expected_dims):
        var_name = node.name
        symbol = self.symbol_table.get(var_name)
        
        if not symbol:
            self.print_error(node, f"Variable '{var_name}' not defined")
            return None
        
        if symbol.type != 'matrix':
            self.print_error(node, f"Variable '{var_name}' is not a matrix")
            return None

        indices = []
        if expected_dims == 1:
            indices = [node.index]
        else:
            indices = [node.row_index, node.col_index]

        for i, idx in enumerate(indices):
            idx_type = self.visit(idx)
            if idx_type != 'int':
                self.print_error(node, "Index must be an integer")
            
            if symbol.size and isinstance(idx, AST.IntNum):
                val = int(idx.value)
                
                if i < len(symbol.size):
                    limit = symbol.size[i]
                    if val < 0 or val >= limit:
                        self.print_error(node, f"Index {val} out of matrix bounds (0..{limit-1})")

        return 'float'

    def visit_If(self, node):
        self.visit(node.condition)
        self.symbol_table = self.symbol_table.pushScope('if')
        self.visit(node.true_body)
        self.symbol_table = self.symbol_table.popScope()
        if node.false_body:
            self.symbol_table = self.symbol_table.pushScope('else')
            self.visit(node.false_body)
            self.symbol_table = self.symbol_table.popScope()

    def visit_While(self, node):
        self.visit(node.condition)
        self.loop_nesting += 1
        self.symbol_table = self.symbol_table.pushScope('while')
        self.visit(node.body)
        self.symbol_table = self.symbol_table.popScope()
        self.loop_nesting -= 1

    def visit_For(self, node):
        self.visit(node.range_expr)
        self.loop_nesting += 1
        self.symbol_table = self.symbol_table.pushScope('for')
        self.symbol_table.put(node.var.name, Symbol(node.var.name, 'int'))
        self.visit(node.body)
        self.symbol_table = self.symbol_table.popScope()
        self.loop_nesting -= 1
        
    def visit_Range(self, node):
        t1 = self.visit(node.start)
        t2 = self.visit(node.end)
        if t1 != 'int' or t2 != 'int':
             self.print_error(node, "Range bounds must be integers")

    def visit_Break(self, node):
        if self.loop_nesting == 0:
            self.print_error(node, "'break' outside of loop")

    def visit_Continue(self, node):
        if self.loop_nesting == 0:
            self.print_error(node, "'continue' outside of loop")
    
    def visit_Return(self, node):
        self.visit(node.expression)
    
    def visit_Print(self, node):
        self.visit(node.print_vals)

    def visit_Transposition(self, node):
        t = self.visit(node.expression)
        if t != 'matrix':
            self.print_error(node, "Transposition only for matrices")
        return 'matrix'
        
    def visit_Uminus(self, node):
         t = self.visit(node.expression)
         return t

    def get_dims(self, node):
        if isinstance(node, AST.Matrix):
            rows = len(node.rows)
            cols = len(node.rows[0]) if rows > 0 else 0
            return (rows, cols)
        if isinstance(node, AST.MatrixFunction):
            if isinstance(node.dim1, AST.IntNum):
                rows = int(node.dim1.value)
                cols = rows
                if node.dim2 and isinstance(node.dim2, AST.IntNum):
                    cols = int(node.dim2.value)
                return (rows, cols)
        if isinstance(node, AST.Variable):
            sym = self.symbol_table.get(node.name)
            if sym and sym.size:
                return sym.size
        if isinstance(node, AST.BinExpr):
            d1 = self.get_dims(node.left)
            d2 = self.get_dims(node.right)
            if node.op in ['+', '-', '.+', '.-', '.*', './']:
                return d1 if d1 else d2
            if node.op == '*':
                if d1 and d2:
                    return (d1[0], d2[1])
        if isinstance(node, AST.Transposition):
             d = self.get_dims(node.expression)
             if d:
                 return (d[1], d[0])
        return None