'''
compiler design project

group members:
    Negar Nobakhti 98171201
    Neda Taghizadeh Serajeh 98170743
'''
import scanner
import Tables
from anytree import Node, RenderTree
import code_gen


scanner.openFile('input.txt')
syntax_errors = []

def is_terminal(phrase):
    return phrase not in Tables.PRODUCTION

STATE_STACK = []
token = None

class Diagram:

    def __init__(self, procedure):
        self.procedure = procedure
        self.branch = self.get_branch()
        self.state = 0

    def get_branch(self):
        for i in range(len(Tables.PRODUCTION[self.procedure])):
            for j in range(len(Tables.PRODUCTION[self.procedure][i])):
                komaki = Tables.PRODUCTION[self.procedure][i][j]
                if komaki == 'EPSILON':
                    return i
                if is_terminal(komaki):
                    if token.value == komaki or token.type == komaki:
                        return i
                    else:
                        break
                else:
                    if token.value in Tables.FIRST[komaki] or token.type in Tables.FIRST[komaki]:
                        return i
                    elif 'EPSILON' not in Tables.FIRST[komaki]:
                        break
                    elif j == len(Tables.PRODUCTION[self.procedure][i]) - 1:
                        return i

    def get_value(self):
        return Tables.PRODUCTION[self.procedure][self.branch][self.state]

    def move_forward(self):
        if self.state < len(Tables.PRODUCTION[self.procedure][self.branch]) - 1:
            self.state += 1
            return True
        return False


token = scanner.get_next_token()
state = Diagram('Program')
root = Node('Program')


def move_to_next_state():
    global state
    global root

    while not state.move_forward():
        state = STATE_STACK.pop()
        root = root.parent

while True:
    current_state = state.get_value()

    if current_state[0]=="#":
        code_gen.code_gen(current_state, token)
        
    elif current_state == 'EPSILON':
        Child = Node('epsilon', parent= root)
        move_to_next_state()
        

    elif is_terminal(current_state):
        if token.value == current_state or token.type == current_state:
            # matches. move both state and token
            if token.value == '$':
                child = Node('$', parent= root)
                break
            child = Node(f"({token.type}, {token.value})", parent= root)
            token = scanner.get_next_token()
            move_to_next_state()
        else:
            # missing token. don't change token and move state
            syntax_errors.append(f"#{token.line} : syntax error, missing {current_state}")
            move_to_next_state()

    else: # non-terminal state
        if token.value in Tables.FIRST[current_state] or token.type in Tables.FIRST[current_state]:
            STATE_STACK.append(state)
            state = Diagram(current_state)
            child = Node(current_state, parent= root)
            root = child

        else:
            if token.value in Tables.FOLLOW[current_state] or token.type in Tables.FOLLOW[current_state]:
                # missing procedure error. move state without changing the token
                if 'EPSILON' in Tables.FIRST[current_state]:
                    STATE_STACK.append(state)
                    state = Diagram(current_state)
                    child = Node(current_state, parent= root)
                    root = child
                else:    
                    syntax_errors.append(f"#{token.line} : syntax error, missing {current_state}")
                    move_to_next_state()

            else:
                # illegal procedure error. don't move state and change token
                if token.value == '$':
                    syntax_errors.append(f"#{token.line} : syntax error, Unexpected EOF")
                    break
                else:
                    syntax_errors.append(f"#{token.line} : syntax error, illegal {token.type if token.type == 'ID' or token.type == 'NUM' else token.value}")
                    token = scanner.get_next_token()
 

with open('syntax_errors.txt', 'w', encoding= "utf-8") as errors:
    if len(syntax_errors)==0:
        errors.write("There is no syntax error.")
    else:
        for error in syntax_errors:
            errors.write(error + "\n")

with open('parse_tree.txt', 'w', encoding= "utf-8") as tree:
    while root.parent:
        root = root.parent

    for pre, fill, node in RenderTree(root):
        tree.write("%s%s" % (pre, node.name) + "\n")

scanner.close_file()
