SEMANTIC_STACK=[]
PROGRAM_BLOCK=[]

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
    pass


def assign():
    A1 = SEMANTIC_STACK.pop()
    R = SEMANTIC_STACK.pop()
    PROGRAM_BLOCK.append(f"(ASSIGN, {A1}, {R})")

def jump(destination):
    PROGRAM_BLOCK.append(f"(JP, {destination}, , )")

def jump_false(destination):
    operand = SEMANTIC_STACK.pop()
    PROGRAM_BLOCK.append(f"(JPF, {operand}, {destination})")

def execute_operation():
    operand_2 = SEMANTIC_STACK.pop()
    operator = SEMANTIC_STACK.pop()
    operand_1 = SEMANTIC_STACK.pop()
    result = 0 #get_temporary_variable
    PROGRAM_BLOCK.append(f"({operator}, {operand_1}, {operand_2}, {result})")
    SEMANTIC_STACK.append(result)



ACTION_SIGN={
    "#pid": pid,
    "#pnum": pnum,
    "#save": save,
    "#assign": assign,
    "#op_exec": execute_operation,
    "#jp": jump,
    "#jpf": jump_false,
    "#addop": ""
}


def generate_code(action, token):
    if token:
        ACTION_SIGN[action](token)
    else:
        ACTION_SIGN[action]()
