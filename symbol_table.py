SYMBOL_TABLE=[]

ADDRESS = 100

class Symbol:
    def __init__(self, id, type, size=0):
        global ADDRESS
        
        self.id = id
        self.address = ADDRESS
        self.type=type
        self.array_size=size

        if(type == 'array'):
            ADDRESS += size * 4
        else:
            ADDRESS += 4


def find_addr(id):
    for symbol in SYMBOL_TABLE[::-1]:
        if symbol.id == id:
            return symbol.address