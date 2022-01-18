import symbol_table

SEMANTIC_STACK=[]
PROGRAM_BLOCK=[]
LIVE_TEMPORARIES=[]

SYMBOL_TABLE={"a": {
    "address":500,
    "size":1
    }
}

operations_dict={ "+":"ADD", "-":"SUB", "*":"MULT", "=":"ASSIGN", "<":"LT", "==":"EQ" }


def pid(id):
    SEMANTIC_STACK.append(SYMBOL_TABLE[id]["address"])

def pnum(num):
    SEMANTIC_STACK.append(f"#{num}")
    
def save():
    SEMANTIC_STACK.append(len(PROGRAM_BLOCK))
    PROGRAM_BLOCK.append('JPF')

def assign():
    A1 = SEMANTIC_STACK.pop()
    R = SEMANTIC_STACK.pop()
    PROGRAM_BLOCK.append(f"(ASSIGN, {A1}, {R})")
    update_temp([A1, R])

def jump(destination):
    PROGRAM_BLOCK.append(f"(JP, {destination}, , )")

def jump_false():
    value = SEMANTIC_STACK.pop()
    address = SEMANTIC_STACK.pop()
    PROGRAM_BLOCK[address] = f"(JPF, {value}, {len(PROGRAM_BLOCK)})"

def execute_operation():
    operand_2 = SEMANTIC_STACK.pop()
    operator = SEMANTIC_STACK.pop()
    operand_1 = SEMANTIC_STACK.pop()
    result = get_temp()
    PROGRAM_BLOCK.append(f"({operator}, {operand_1}, {operand_2}, {result})")
    SEMANTIC_STACK.append(result)

def addop(operator):
    SEMANTIC_STACK.append(operations_dict[operator])

def declare(id):
    SEMANTIC_STACK.append(id)

def declare_int():
    id = SEMANTIC_STACK.pop()
    symbol_table.SYMBOL_TABLE.append(symbol_table.Symbol(id, 'int'))

def declare_arr(num):
    id = SEMANTIC_STACK.pop()
    symbol_table.SYMBOL_TABLE.append(symbol_table.Symbol(id,'array', size= num))

def declare_func():
    id = SEMANTIC_STACK.pop()
    symbol_table.SYMBOL_TABLE.append(symbol_table.Symbol(id, 'func'))

ACTION_SIGN={
    "#declare": declare,
    '#declare_int':declare_int,
    '#declare_arr':declare_arr,
    '#declare_func':declare_func,
    "#pid": pid,
    "#pnum": pnum,
    "#save": save,
    "#assign": assign,
    "#op_exec": execute_operation,
    "#jp": jump,
    "#jpf_save": jump_false,
    "#addop": addop
}


def code_gen(action, token=None):
    if token:
        ACTION_SIGN[action](token)
    else:
        ACTION_SIGN[action]()


def get_temp():
    temp = 500
    while temp in LIVE_TEMPORARIES:
        temp +=4

    LIVE_TEMPORARIES.append(temp)
    return temp

def update_temp(addr):
    for i in addr:
        if i in LIVE_TEMPORARIES:
            LIVE_TEMPORARIES.remove(i)
