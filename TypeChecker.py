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

    def visit_IntNum(self, node):
        return 'int'

    def visit_FloatNum(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Variable(self, node):
        symbol = self.symbol_table.get(node.name)
        if symbol:
            return symbol.type
        return None

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op

        if not type1 or not type2:
            return None

        dims1 = self.get_dims(node.left)
        dims2 = self.get_dims(node.right)

        if type1 == 'matrix' or type2 == 'matrix':
            if type1 != type2 and op not in ['.+', '.-', '.*', './']:
                 print(f"Error: Incompatible types for operation '{op}' at line {getattr(node, 'lineno', '?')}")
                 self.errors_found = True
                 return None
            
            if type1 == 'matrix' and type2 == 'matrix':
                if op in ['+', '-']:
                    if dims1 != dims2:
                        print(f"Error: Matrix dimensions mismatch {dims1} vs {dims2} for operation '{op}' at line {getattr(node, 'lineno', '?')}")
                        self.errors_found = True
                elif op in ['.+', '.-', '.*', './']:
                    if dims1 != dims2:
                        print(f"Error: Matrix dimensions mismatch {dims1} vs {dims2} for dot operation '{op}' at line {getattr(node, 'lineno', '?')}")
                        self.errors_found = True
                elif op == '*':
                    if dims1 and dims2 and dims1[1] != dims2[0]:
                        print(f"Error: Invalid matrix dimensions for multiplication {dims1} vs {dims2} at line {getattr(node, 'lineno', '?')}")
                        self.errors_found = True
            
            return 'matrix'

        if type1 == type2:
            return type1
        
        if (type1 == 'int' and type2 == 'float') or (type1 == 'float' and type2 == 'int'):
            return 'float'

        print(f"Error: Incompatible types {type1} and {type2} for '{op}' at line {getattr(node, 'lineno', '?')}")
        self.errors_found = True
        return None

    def visit_Assign(self, node):
        type_right = self.visit(node.right)
        
        if isinstance(node.left, AST.Variable):
            dims = self.get_dims(node.right)
            self.symbol_table.put(node.left.name, Symbol(node.left.name, type_right, dims))
        
        elif isinstance(node.left, (AST.VectorElement, AST.MatrixElement)):
             self.visit(node.left)
             if type_right not in ['int', 'float']:
                 print(f"Error: Cannot assign {type_right} to matrix element at line {getattr(node, 'lineno', '?')}")

    def visit_Matrix(self, node):
        rows_len = []
        for row in node.rows:
            if isinstance(row, list):
                rows_len.append(len(row))
                for elem in row:
                    self.visit(elem)
            else:
                 pass
        
        if len(set(rows_len)) > 1:
            print(f"Error: Matrix rows have different sizes at line {getattr(node, 'lineno', '?')}")
            self.errors_found = True
            return 'matrix'
        
        return 'matrix'

    def visit_MatrixFunction(self, node):
        arg_type = self.visit(node.expression)
        if arg_type != 'int':
            print(f"Error: Function '{node.func_name}' argument must be an integer at line {getattr(node, 'lineno', '?')}")
            self.errors_found = True
        
        return 'matrix'

    def visit_VectorElement(self, node):
        return self._check_ref_bounds(node, 1)

    def visit_MatrixElement(self, node):
        return self._check_ref_bounds(node, 2)

    def _check_ref_bounds(self, node, expected_dims):
        var_name = node.name
        symbol = self.symbol_table.get(var_name)
        
        if not symbol or symbol.type != 'matrix':
            print(f"Error: Variable '{var_name}' is not a matrix/vector at line {getattr(node, 'lineno', '?')}")
            self.errors_found = True
            return 'error'

        indices = []
        if expected_dims == 1:
            indices = [node.index]
        else:
            indices = [node.row_index, node.col_index]

        for i, idx_node in enumerate(indices):
            idx_type = self.visit(idx_node)
            if idx_type != 'int':
                print(f"Error: Index must be an integer at line {getattr(node, 'lineno', '?')}")
                self.errors_found = True

            if isinstance(idx_node, AST.IntNum) and symbol.size:
                limit = symbol.size[i] if i < len(symbol.size) else 0
                val = idx_node.value
                
                if val < 0 or val >= limit: 
                    print(f"Error: Index {val} out of matrix bounds (0..{limit-1}) at line {getattr(node, 'lineno', '?')}")
                    self.errors_found = True

        return 'float'

    def visit_If(self, node):
        self.visit(node.condition)
        self.visit(node.true_body)
        if node.false_body:
            self.visit(node.false_body)

    def visit_While(self, node):
        self.visit(node.condition)
        self.loop_nesting += 1
        self.visit(node.body)
        self.loop_nesting -= 1

    def visit_For(self, node):
        self.visit(node.range_expr)
        self.symbol_table.put(node.var.name, Symbol(node.var.name, 'int'))
        
        self.loop_nesting += 1
        self.visit(node.body)
        self.loop_nesting -= 1

    def visit_Break(self, node):
        if self.loop_nesting == 0:
            print(f"Error: 'break' outside of loop at line {getattr(node, 'lineno', '?')}")
            self.errors_found = True

    def visit_Continue(self, node):
        if self.loop_nesting == 0:
            print(f"Error: 'continue' outside of loop at line {getattr(node, 'lineno', '?')}")
            self.errors_found = True
    
    def visit_Return(self, node):
        self.visit(node.expression)
    
    def visit_Print(self, node):
        self.visit(node.print_vals)

    def get_dims(self, node):
        if isinstance(node, AST.Matrix):
            rows = len(node.rows)
            cols = len(node.rows[0]) if rows > 0 else 0
            return (rows, cols)
        if isinstance(node, AST.MatrixFunction):
            if isinstance(node.expression, AST.IntNum):
                val = node.expression.value
                return (val, val)
        if isinstance(node, AST.Variable):
            sym = self.symbol_table.get(node.name)
            if sym and sym.size:
                return sym.size
        return None