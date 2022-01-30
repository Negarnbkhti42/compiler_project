SYMBOL_TABLE=[]


class Symbol:
    def __init__(self, id, type, address, size=0):
        
        self.id = id
        self.address = address
        self.type=type
        self.array_size=size



def find_addr(id):
    for symbol in SYMBOL_TABLE[::-1]:
        if symbol.id == id:
            return symbol.address