import symbol_table

SEMANTIC_STACK=[]
PROGRAM_BLOCK=['main_jump']
LIVE_TEMPORARIES=[]

operations_dict={ "+":"ADD", "-":"SUB", "*":"MULT", "<":"LT", "==":"EQ"  }


def pid(id):
    SEMANTIC_STACK.append(symbol_table.find_addr(id))

def pnum(num):
    SEMANTIC_STACK.append(f"#{num}")

def save(param=None):
    SEMANTIC_STACK.append(len(PROGRAM_BLOCK))
    PROGRAM_BLOCK.append('JPF')

def assign(param=None):
    A1 = SEMANTIC_STACK.pop()
    R = SEMANTIC_STACK.pop()
    PROGRAM_BLOCK.append(f"(ASSIGN, {A1}, {R})")
    update_temp([A1, R])

def jump(param=None):
    address = SEMANTIC_STACK.pop()
    PROGRAM_BLOCK[address] = (f"(JP, {len(PROGRAM_BLOCK)}, , )")

def jump_false(param=None):
    value = SEMANTIC_STACK.pop()
    address = SEMANTIC_STACK.pop()
    PROGRAM_BLOCK[address] = f"(JPF, {value}, {len(PROGRAM_BLOCK)})"

def jump_false_save(param=None):
    value = SEMANTIC_STACK.pop()
    address = SEMANTIC_STACK.pop()
    PROGRAM_BLOCK[address] = f"(JPF, {value}, {len(PROGRAM_BLOCK) + 1})"
    save()

def execute_operation(param=None):
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

def declare_int(param=None):
    id = SEMANTIC_STACK.pop()
    symbol_table.SYMBOL_TABLE.append(symbol_table.Symbol(id, 'int'))

def declare_arr(num=0):
    id = SEMANTIC_STACK.pop()
    symbol_table.SYMBOL_TABLE.append(symbol_table.Symbol(id,'array', size= num))

def declare_func(param=None):
    id = SEMANTIC_STACK.pop()
    symbol_table.SYMBOL_TABLE.append(symbol_table.Symbol(id, 'func'))
    if id == 'main':
        main_jump()

def main_jump(param=None):
    PROGRAM_BLOCK[0] = f"(JP, {len(PROGRAM_BLOCK)}, , )"


def set_index(param=None):
    index = SEMANTIC_STACK.pop()
    id = SEMANTIC_STACK.pop()
    temp = get_temp()
    PROGRAM_BLOCK.append(f"(MULT, #{index}, #4, {temp})")
    PROGRAM_BLOCK.append(f"(ADD, {temp}, {id}, {temp})")
    SEMANTIC_STACK.append(f"@{temp}")


def set_arg_pointer(param=None):
    SEMANTIC_STACK.append('_arg_pointer')

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
    "#jpf": jump_false,
    "#jpf_save": jump_false_save,
    "#addop": addop,
    "#set_index": set_index,
    "#set_arg_pointer": set_arg_pointer,
    "#func_call": ''
}


def code_gen(action, token=None):
    ACTION_SIGN[action](token)


def get_temp():
    temp = 2000
    while temp in LIVE_TEMPORARIES:
        temp +=4

    LIVE_TEMPORARIES.append(temp)
    return temp

def update_temp(addr):
    for i in addr:
        if i in LIVE_TEMPORARIES:
            LIVE_TEMPORARIES.remove(i)


def write_output():
    with open('output.txt', 'w', encoding='utf-8') as output:
        for idx, line in enumerate(PROGRAM_BLOCK):
            output.write(f"{idx}\t{line}")

