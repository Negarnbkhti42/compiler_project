import symbol_table

SEMANTIC_STACK = []
PROGRAM_BLOCK = []
RETURN_LIST = []
PROGRAM_BLOCK_INDEX = 0
TEMPORARY = 2000

operations_dict = {"+": "ADD", "-": "SUB", "*": "MULT", "<": "LT", "==": "EQ"}



def add_type(type):
    SEMANTIC_STACK.append(type)


def pnum(num):
    SEMANTIC_STACK.append(f"#{num}")


def declare_int(param=None):
    id = SEMANTIC_STACK.pop()
    type = SEMANTIC_STACK.pop()
    addr = get_temp()
    symbol_table.SYMBOL_TABLE.append(symbol_table.Symbol(id, 'int', addr))


def declare_arr(param=0):
    size = SEMANTIC_STACK.pop()[1:]
    id = SEMANTIC_STACK.pop()
    type = SEMANTIC_STACK.pop()
    addr = get_temp()
    symbol_table.SYMBOL_TABLE.append(symbol_table.Symbol(id, 'array', size))


def func_id(param=None):
    global PROGRAM_BLOCK_INDEX
    global symbol_table

    id = SEMANTIC_STACK.pop()
    SEMANTIC_STACK.append(PROGRAM_BLOCK_INDEX)
    SEMANTIC_STACK.append(id)
    PROGRAM_BLOCK_INDEX += 1
    symbol_table.SYMBOL_TABLE.append("func_start")


def label(param= None):
    SEMANTIC_STACK.append(PROGRAM_BLOCK_INDEX)


def set_func_temps(param= None):
    for i in range(2):
        SEMANTIC_STACK.append(get_temp())

def start_func(param= None):
    RETURN_LIST.append(('begin_func', '#0'))


def end_func(param= None):
    index = RETURN_LIST.pop()
    while index[0] != 'begin_func':
        add_to_pb(index[0], 'ASSIGN', index[1], SEMANTIC_STACK[-1])
        add_to_pb(index[0]+1, 'JP', PROGRAM_BLOCK_INDEX)
        index = RETURN_LIST.pop()

def return_address(param= None):
    global PROGRAM_BLOCK_INDEX

    name = SEMANTIC_STACK[-4]
    if name == 'main':
        return
    addr= SEMANTIC_STACK[-2]
    add_to_pb(PROGRAM_BLOCK_INDEX, 'JP', f"@{addr}")
    PROGRAM_BLOCK_INDEX += 1


def declare_func(param=None):
    global symbol_table

    attr = []
    symbol = symbol_table.SYMBOL_TABLE.pop()
    while symbol != 'func_start':
        attr.append(symbol)
        symbol = symbol_table.SYMBOL_TABLE.pop()
    attr.append(SEMANTIC_STACK[-3])
    attr.reverse()
    attr.append(SEMANTIC_STACK[-2])
    attr.append(SEMANTIC_STACK[-1])
    symbol_table.SYMBOL_TABLE.append(symbol_table.Symbol(SEMANTIC_STACK[-4], 'func', SEMANTIC_STACK[-3], attr= attr))


def add_id(id):
    SEMANTIC_STACK.append(id)


def pid(id):
    SEMANTIC_STACK.append(symbol_table.find_addr(id))


def save(param=None):
    global PROGRAM_BLOCK_INDEX

    SEMANTIC_STACK.append(PROGRAM_BLOCK_INDEX)
    add_to_pb(PROGRAM_BLOCK_INDEX, 'JPF', '')
    PROGRAM_BLOCK_INDEX += 1


def assign(param=None):
    global PROGRAM_BLOCK_INDEX

    A1 = SEMANTIC_STACK.pop()
    R = SEMANTIC_STACK.pop()
    add_to_pb(PROGRAM_BLOCK_INDEX, 'ASSIGN', A1, r= R)
    PROGRAM_BLOCK_INDEX += 1

def jump(param=None):
    address = SEMANTIC_STACK.pop()
    add_to_pb(address, 'JP', len(PROGRAM_BLOCK))


def jump_false(param=None):
    value = SEMANTIC_STACK.pop()
    address = SEMANTIC_STACK.pop()
    add_to_pb(address, 'JPF', value, op2= len(PROGRAM_BLOCK))


def jump_false_save(param=None):
    value = SEMANTIC_STACK.pop()
    address = SEMANTIC_STACK.pop()
    add_to_pb(address, 'JPF', value, op2= len(PROGRAM_BLOCK) + 1)
    save()


def execute_operation(param=None):
    global PROGRAM_BLOCK_INDEX

    operand_2 = SEMANTIC_STACK.pop()
    operator = SEMANTIC_STACK.pop()
    operand_1 = SEMANTIC_STACK.pop()
    result = get_temp()
    add_to_pb(PROGRAM_BLOCK_INDEX, operator, operand_1, op2= operand_2, r= result)
    PROGRAM_BLOCK_INDEX += 1
    SEMANTIC_STACK.append(result)


def addop(operator):
    SEMANTIC_STACK.append(operations_dict[operator])



def main_jump(param=None):
    PROGRAM_BLOCK[0] = f"(JP, {len(PROGRAM_BLOCK)}, , )"


def set_index(param=None):
    global PROGRAM_BLOCK_INDEX
    
    index = SEMANTIC_STACK.pop()
    id = SEMANTIC_STACK.pop()
    temp = get_temp()

    add_to_pb(PROGRAM_BLOCK_INDEX, 'MULT', f"#{index}", "#4", f"{temp}")
    PROGRAM_BLOCK_INDEX += 1
    add_to_pb(PROGRAM_BLOCK_INDEX, 'ADD', temp, id, temp)
    PROGRAM_BLOCK_INDEX += 1
    SEMANTIC_STACK.append(f"@{temp}")


def set_arg_pointer(param=None):
    SEMANTIC_STACK.append('_arg_pointer')


ACTION_SIGN = {
    "#add_type": add_type,
    "#add_id": add_id,
    '#declare_int': declare_int,
    '#declare_arr': declare_arr,
    '#func_id': func_id,
    "#label": label,
    "#set_func_temps": set_func_temps,
    "#start_func": start_func,
    "#end_func": end_func,
    "#return_address": return_address,
    '#declare_func': declare_func,
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


def get_temp(size=1):
    global TEMPORARY
    addr = TEMPORARY
    TEMPORARY += 4*size
    return addr

def add_to_pb(index, action, op1, op2='', r=''):
    global PROGRAM_BLOCK
    while len(PROGRAM_BLOCK) <= index:
        PROGRAM_BLOCK.append('')
    PROGRAM_BLOCK[index] = f"{action}, {op1}, {op2}, {r}"


def write_output():
    with open('output.txt', 'w', encoding='utf-8') as output:
        for idx, line in enumerate(PROGRAM_BLOCK):
            output.write(f"{idx}\t{line}")
