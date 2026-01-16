class Memory:
    def __init__(self, name): 
        self.name = name
        self.memory = {}

    def has_key(self, name): 
        return name in self.memory

    def get(self, name): 
        return self.memory.get(name)

    def put(self, name, value): 
        self.memory[name] = value

class MemoryStack:
    def __init__(self, memory=None): 
        self.stack = []
        if memory:
            self.stack.append(memory)
        else:
            self.stack.append(Memory("Global"))

    def get(self, name): 
        for mem in reversed(self.stack):
            if mem.has_key(name):
                return mem.get(name)
        return None

    def insert(self, name, value): 
        self.stack[-1].put(name, value)

    def set(self, name, value):
        for mem in reversed(self.stack):
            if mem.has_key(name):
                mem.put(name, value)
                return
        self.stack[-1].put(name, value)

    def push(self, memory): 
        self.stack.append(memory)

    def pop(self): 
        return self.stack.pop()