import symbol_table

SEMANTIC_STACK = []
PROGRAM_BLOCK = []
SEMANTIC_ERROR = []
RETURN_LIST = []
BREAK_LIST = []
PROGRAM_BLOCK_INDEX = 0
TEMPORARY = 500

NUM_OF_ARGS = 0

operations_dict = {"+": "ADD", "-": "SUB", "*": "MULT", "<": "LT", "==": "EQ"}


def add_type(type):
    SEMANTIC_STACK.append(type.value)


def pnum(num):
    SEMANTIC_STACK.append(f"#{num.value}")


def declare_int(param=None):
    id = SEMANTIC_STACK.pop()
    type = SEMANTIC_STACK.pop()
    addr = get_temp()
    symbol_table.SYMBOL_TABLE.append(symbol_table.Symbol(id, 'int', addr))


def declare_arr_arg(param=None):
    id = SEMANTIC_STACK.pop()
    type = SEMANTIC_STACK.pop()
    addr = get_temp()
    symbol_table.SYMBOL_TABLE.append(symbol_table.Symbol(id, 'array', addr))


def declare_arr(param=0):
    global PROGRAM_BLOCK_INDEX

    size = SEMANTIC_STACK.pop()[1:]
    id = SEMANTIC_STACK.pop()
    type = SEMANTIC_STACK.pop()

    temp = get_temp()
    arr = get_temp(int(size))
    add_to_pb(PROGRAM_BLOCK_INDEX, "ASSIGN", f"#{arr}", temp)
    PROGRAM_BLOCK_INDEX += 1
    symbol_table.SYMBOL_TABLE.append(symbol_table.Symbol(id, type, temp))


def func_id(param=None):
    global PROGRAM_BLOCK_INDEX
    global symbol_table

    id = SEMANTIC_STACK.pop()
    SEMANTIC_STACK.append(PROGRAM_BLOCK_INDEX)
    SEMANTIC_STACK.append(id)
    if id != 'main':
        PROGRAM_BLOCK_INDEX += 1
    symbol_table.SYMBOL_TABLE.append("func_start")


def params_declared(param=None):
    symbol_table.SYMBOL_TABLE.append("param_declare")


def label(param=None):
    SEMANTIC_STACK.append(PROGRAM_BLOCK_INDEX)


def set_func_temps(param=None):
    for i in range(2):
        SEMANTIC_STACK.append(get_temp())


def start_func(param=None):
    RETURN_LIST.append(('begin_func', '#0'))


def end_func(param=None):
    index = RETURN_LIST.pop()
    while index[0] != 'begin_func':
        add_to_pb(index[0], 'ASSIGN', index[1], SEMANTIC_STACK[-1])
        add_to_pb(index[0]+1, 'JP', PROGRAM_BLOCK_INDEX)
        index = RETURN_LIST.pop()


def return_address(param=None):
    global PROGRAM_BLOCK_INDEX

    name = SEMANTIC_STACK[-4]
    if name == 'main':
        return
    addr = SEMANTIC_STACK[-2]
    add_to_pb(PROGRAM_BLOCK_INDEX, 'JP', f"@{addr}")
    PROGRAM_BLOCK_INDEX += 1


def declare_func(param=None):
    global symbol_table

    attr = []
    attr_type = []
    symbol = symbol_table.SYMBOL_TABLE.pop()

    while symbol != 'param_declare':
        symbol = symbol_table.SYMBOL_TABLE.pop()

    symbol = symbol_table.SYMBOL_TABLE.pop()

    while symbol != 'func_start':
        attr.append(symbol.address)
        attr_type.append(symbol.type)
        symbol = symbol_table.SYMBOL_TABLE.pop()
    attr.append(SEMANTIC_STACK[-3])
    attr.reverse()
    attr.append(SEMANTIC_STACK[-2])
    attr.append(SEMANTIC_STACK[-1])
    symbol_table.SYMBOL_TABLE.append(symbol_table.Symbol(
        SEMANTIC_STACK[-4], 'func', attr, attr=attr_type))
    for i in range(4):
        SEMANTIC_STACK.pop()

    if symbol_table.SYMBOL_TABLE[-1].id != 'main':
        add_to_pb(SEMANTIC_STACK.pop(), 'JP', PROGRAM_BLOCK_INDEX)
    SEMANTIC_STACK.pop()


def add_id(id):
    SEMANTIC_STACK.append(id.value)


def pid(id):
    symbol = 'print' if id.value == 'output' else symbol_table.find_addr(
        id.value)
    if symbol:
        SEMANTIC_STACK.append(symbol)
    else:
        SEMANTIC_ERROR.append(
            f"#{id.line}: Semantic Error! '{id.value}' is not defined")


def save(param=None):
    global PROGRAM_BLOCK_INDEX

    SEMANTIC_STACK.append(PROGRAM_BLOCK_INDEX)
    PROGRAM_BLOCK_INDEX += 1


def save_iter(param=None):
    SEMANTIC_STACK.append(PROGRAM_BLOCK_INDEX)


def assign(param=None):
    global PROGRAM_BLOCK_INDEX
    global SEMANTIC_STACK

    A1 = SEMANTIC_STACK.pop()
    R = SEMANTIC_STACK.pop()
    SEMANTIC_STACK.append(R)
    add_to_pb(PROGRAM_BLOCK_INDEX, 'ASSIGN', A1, r=R)
    PROGRAM_BLOCK_INDEX += 1


def pop(param=None):
    SEMANTIC_STACK.pop()


def jump(param=None):
    address = SEMANTIC_STACK.pop()
    add_to_pb(address, 'JP', PROGRAM_BLOCK_INDEX)


def jump_false(param=None):
    global PROGRAM_BLOCK_INDEX

    address = SEMANTIC_STACK.pop()
    value = SEMANTIC_STACK.pop()
    add_to_pb(address, 'JPF', value, op2=PROGRAM_BLOCK_INDEX)


def jump_false_iter(param=None):
    global PROGRAM_BLOCK_INDEX

    value = SEMANTIC_STACK.pop()
    address = SEMANTIC_STACK.pop()
    add_to_pb(PROGRAM_BLOCK_INDEX, 'JPF', value, op2=address)
    PROGRAM_BLOCK_INDEX += 1


def jump_false_save(param=None):
    global PROGRAM_BLOCK_INDEX
    address = SEMANTIC_STACK.pop()
    value = SEMANTIC_STACK.pop()
    add_to_pb(address, 'JPF', value, op2=PROGRAM_BLOCK_INDEX + 1)
    save()


def execute_operation(param=None):
    global PROGRAM_BLOCK_INDEX

    operand_2 = SEMANTIC_STACK.pop()
    operator = SEMANTIC_STACK.pop()
    operand_1 = SEMANTIC_STACK.pop()
    result = get_temp()
    add_to_pb(PROGRAM_BLOCK_INDEX, operator,
              operand_1, op2=operand_2, r=result)
    PROGRAM_BLOCK_INDEX += 1
    SEMANTIC_STACK.append(result)


def addop(operator):
    SEMANTIC_STACK.append(operations_dict[operator.value])


def set_index(param=None):
    global PROGRAM_BLOCK_INDEX

    index = SEMANTIC_STACK.pop()
    id = SEMANTIC_STACK.pop()
    temp = get_temp()
    temp2 = get_temp()

    add_to_pb(PROGRAM_BLOCK_INDEX, 'MULT', f"{index}", "#4", f"{temp}")
    PROGRAM_BLOCK_INDEX += 1
    add_to_pb(PROGRAM_BLOCK_INDEX, 'ASSIGN', f"@{id}", temp2)
    PROGRAM_BLOCK_INDEX += 1
    add_to_pb(PROGRAM_BLOCK_INDEX, 'ADD', temp, temp2, temp)
    PROGRAM_BLOCK_INDEX += 1
    SEMANTIC_STACK.append(f"@{temp}")


def break_start(param=None):
    BREAK_LIST.append('loop_begin')


def break_op(param=None):
    global PROGRAM_BLOCK_INDEX

    if len(BREAK_LIST) == 0:
        SEMANTIC_ERROR.append(
            f"#{param.line}: Semantic Error! No 'repeat ... until' found for 'break'")
        return

    BREAK_LIST.append(PROGRAM_BLOCK_INDEX)
    PROGRAM_BLOCK_INDEX += 1


def break_end(param=None):
    index = BREAK_LIST.pop()

    while index != 'loop_begin':
        add_to_pb(index, 'JP', PROGRAM_BLOCK_INDEX)
        index = BREAK_LIST.pop()


def return_op(param=None):
    global PROGRAM_BLOCK_INDEX

    RETURN_LIST.append((PROGRAM_BLOCK_INDEX, '#0'))
    PROGRAM_BLOCK_INDEX += 2


def return_value_op(param=None):
    global PROGRAM_BLOCK_INDEX

    value = SEMANTIC_STACK.pop()
    RETURN_LIST.append((PROGRAM_BLOCK_INDEX, value))
    PROGRAM_BLOCK_INDEX += 2


def increase_arg_given(param=None):
    global NUM_OF_ARGS
    NUM_OF_ARGS += 1


def func_call(param):
    global PROGRAM_BLOCK_INDEX
    global SEMANTIC_STACK
    global SEMANTIC_ERROR
    global NUM_OF_ARGS

    if len(SEMANTIC_STACK) > 1 and SEMANTIC_STACK[-2] == 'print':
        addr = SEMANTIC_STACK.pop()
        add_to_pb(PROGRAM_BLOCK_INDEX, 'PRINT', addr)

        PROGRAM_BLOCK_INDEX += 1
        NUM_OF_ARGS = 0
        return

    argLen = len(SEMANTIC_STACK)
    funcionArgs = []

    for symbol in SEMANTIC_STACK[::-1]:
        if isinstance(symbol, list):
            funcionArgs = symbol
            break
    else:
        return

    if funcionArgs == []:
        return

    originalArgLen = len(funcionArgs) - 3
    func = symbol_table.getSymbol(funcionArgs)

    if originalArgLen != NUM_OF_ARGS:
        SEMANTIC_ERROR.append(
            f"#{param.line}: semantic error! Mismatch in numbers of arguments of '{func.id}'")
        for i in range(NUM_OF_ARGS):
            SEMANTIC_STACK.pop()
        NUM_OF_ARGS = 0
        return

    for i in range(originalArgLen):
        formal_arg = SEMANTIC_STACK[argLen - NUM_OF_ARGS + i]
        original_arg = funcionArgs[i + 1]

        formal_arg_type = 'int' if isinstance(
            formal_arg, str) else symbol_table.getSymbol(formal_arg).type
        original_arg_type = func.attr[i]

        if formal_arg_type != original_arg_type:
            SEMANTIC_ERROR.append(
                f"#{param.line}: Semantic Error! Mismatch in type of argument {i+1} for '{func.id}'. Expected '{original_arg_type}' but got '{formal_arg_type}' instead")
        add_to_pb(PROGRAM_BLOCK_INDEX, 'ASSIGN', formal_arg, r=original_arg)
        PROGRAM_BLOCK_INDEX += 1

    add_to_pb(PROGRAM_BLOCK_INDEX, 'ASSIGN',
              f"#{PROGRAM_BLOCK_INDEX + 2}", funcionArgs[originalArgLen + 1])
    PROGRAM_BLOCK_INDEX += 1
    add_to_pb(PROGRAM_BLOCK_INDEX, 'JP', funcionArgs[0] + 1)
    PROGRAM_BLOCK_INDEX += 1

    for i in range(NUM_OF_ARGS + 1):
        SEMANTIC_STACK.pop()

    addr = get_temp()
    SEMANTIC_STACK.append(addr)
    add_to_pb(PROGRAM_BLOCK_INDEX, 'ASSIGN',
              funcionArgs[originalArgLen + 2], addr)
    PROGRAM_BLOCK_INDEX += 1

    NUM_OF_ARGS = 0


ACTION_SIGN = {
    "#add_type": add_type,
    "#add_id": add_id,
    '#declare_int': declare_int,
    "#declare_arr_arg": declare_arr_arg,
    '#declare_arr': declare_arr,
    '#func_id': func_id,
    "#params_declared": params_declared,
    "#label": label,
    "#set_func_temps": set_func_temps,
    "#start_func": start_func,
    "#end_func": end_func,
    "#return_address": return_address,
    '#declare_func': declare_func,
    "#pid": pid,
    "#pnum": pnum,
    "#save": save,
    "#save_iter": save_iter,
    "#assign": assign,
    "#pop": pop,
    "#op_exec": execute_operation,
    "#jp": jump,
    "#jpf": jump_false,
    "#jpf_iter": jump_false_iter,
    "#jpf_save": jump_false_save,
    "#addop": addop,
    "#set_index": set_index,
    "#break_start": break_start,
    "#break": break_op,
    "#break_end": break_end,
    "#return": return_op,
    "#return_value": return_value_op,
    "#increase_arg_given": increase_arg_given,
    "#func_call": func_call
}


def code_gen(action, token=None):
    ACTION_SIGN[action](token)


def get_temp(size=1):
    global TEMPORARY
    global PROGRAM_BLOCK_INDEX

    addr = TEMPORARY
    for i in range(size):
        add_to_pb(PROGRAM_BLOCK_INDEX, 'ASSIGN', '#0', TEMPORARY)
        TEMPORARY += 4
        PROGRAM_BLOCK_INDEX += 1
    # TEMPORARY += 4 * size
    return addr


def add_to_pb(index, action, op1, op2='', r=''):
    global PROGRAM_BLOCK
    while len(PROGRAM_BLOCK) <= index:
        PROGRAM_BLOCK.append('')
    PROGRAM_BLOCK[index] = f"({action}, {op1}, {op2}, {r})"


def write_output():
    with open('output.txt', 'w+', encoding='utf-8') as output:
        for idx, line in enumerate(PROGRAM_BLOCK):
            output.write(f"{idx}\t{line}\n")


def write_semantic_errors():
    with open('semantic_errors.txt', 'w', encoding='utf-8') as errors:
        if SEMANTIC_ERROR:
            for error in SEMANTIC_ERROR:
                errors.write(f"{error}\n")
        else:
            errors.write("The input program is semantically correct.")
