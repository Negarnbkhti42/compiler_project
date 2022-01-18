SYMBOL_TABLE=[]


class Symbol:
    def __init__(self, id, type, size=0):
        self.id = id
        self.address = 0 #get adress from table
        self.type=type
        self.array_size=size

symbol_1 = Symbol('a', 'int')
SYMBOL_TABLE.append(symbol_1)

symbol_2 = Symbol('arr', 'array', 4)
SYMBOL_TABLE.append(symbol_2)

def find_addr(id):
    for symbol in SYMBOL_TABLE:
        if symbol.id == id:
            return symbol.address