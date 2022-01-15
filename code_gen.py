SEMANTIC_STACK=[]
PROGRAM_BLOCK=[]

SYMBOL_TABLE={"a": {
    "address":500,
    "size":1
    }

}

operations_dict={ "+":"ADD", "-":"SUB", "*":"MULT", "=":"ASSIGN", "<":"LT", "==":"EQ" }


def add_id(id):
    SEMANTIC_STACK.append(SYMBOL_TABLE[id]["address"])
    
def save():
    pass


def assign():
    pass

def jump():
    pass

def jump_false(destination):
    operand = SEMANTIC_STACK.pop()
    PROGRAM_BLOCK.append(f"JPF, {operand}, {destination}")

def execute_operation():
    operand_2 = SEMANTIC_STACK.pop()
    operator = SEMANTIC_STACK.pop()
    operand_1 = SEMANTIC_STACK.pop()
    result = 0 #get_temporary_variable
    PROGRAM_BLOCK.append(f"({operator}, {operand_1}, {operand_2}, {result})")
    SEMANTIC_STACK.append(result)



ACTION_SIGN={
    "#pid": add_id,
    "#save": save,
    "#assign": assign,
    "#op_exec": execute_operation,
    "#jmp": jump,
    "#jmpf": jump_false,
    "#addop": ""
}


inputTXT=input()

if input.contain(operations_dict.keys()):
    pass

# while a*b/c-d+r 

def generate_code(action, token):
    ACTION_SIGN[action](token)



