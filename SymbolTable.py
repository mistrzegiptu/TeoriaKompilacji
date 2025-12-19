class Symbol:
    def __init__(self, name, type, size=None):
        self.name = name
        self.type = type  # 'int', 'float', 'string', 'matrix', 'vector'
        self.size = size  # krotka (rows, cols) lub (size,) dla wektorów

class SymbolTable(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.symbols = {}

    def put(self, name, symbol):
        self.symbols[name] = symbol

    def get(self, name):
        s = self.symbols.get(name)
        if s is not None:
            return s
        if self.parent:
            return self.parent.get(name)
        return None

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        return SymbolTable(self, name)

    def popScope(self):
        return self.parent