SYMBOL_TABLE = []


class Symbol:
    def __init__(self, id, type, address, attr=0):

        self.id = id
        self.address = address
        self.type = type
        self.attr = attr


def find_addr(id):
    for symbol in SYMBOL_TABLE[::-1]:
        if type(symbol) == str:
            continue
        if symbol.id == id:
            return symbol.address


def getSymbol(addr):
    for symbol in SYMBOL_TABLE[::-1]:
        if type(symbol) == str:
            continue
        if symbol.address == addr:
            return symbol
