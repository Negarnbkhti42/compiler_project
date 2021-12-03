'''
compiler design project

group members:
    Negar Nobakhti 98171201
    Neda Taghizadeh Serajeh 98170743
'''
import scanner
import Tables
from anytree import Node, RenderTree


scanner.openFile('input.txt')
syntax_errors = []

STATE_STACK = [] 
token = ''
state = None

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

        return len(Tables.PRODUCTION[self.procedure]) - 1


    def get_value(self):
        return Tables.PRODUCTION[self.procedure][self.branch][self.state]

    def move_forward(self):
        if self.state < len(Tables.PRODUCTION[self.procedure][self.branch]) - 1:
            self.state += 1
            return True
        return False


def is_terminal(phrase):
    return phrase not in Tables.PRODUCTION


token = scanner.get_next_token()
state = Diagram('Program')
root = None

while token.value != '$':
    current_state = state.get_value()

    if is_terminal(current_state):
        if token.value == current_state or token.type == current_state:
            # matches. move both state and token
            child = Node(f"({token.type}, {token.value})", parent= root)
            token = scanner.get_next_token()
            while not state.move_forward():
                state = STATE_STACK.pop()
                root = root.parent
        else:
            # missing token. don't change token and move state
            syntax_errors.append(f"#{scanner.line_num} : syntax error, missing {current_state}")
            while not state.move_forward():
                state = STATE_STACK.pop()
                root = root.parent

    else: # non-terminal state
        if token.value in Tables.FIRST[current_state] or token.type in Tables.FIRST[current_state] or 'EPSILON' in Tables.FIRST[current_state]:
            STATE_STACK.append(state)
            state = Diagram(current_state)
            child = Node(current_state, parent= root)
            root = child

        else:
            if token in Tables.FOLLOW[current_state]:
                # missing procedure error. move state without changing the token
                syntax_errors.append(f"#{scanner.line_num} : syntax error, missing {current_state}")
                while not state.move_forward():
                    state = STATE_STACK.pop()
                    root = root.parent

            else:
                # illegal procedure error. don't move state and change token
                syntax_errors.append(f"#{scanner.line_num} : syntax error, illegal {token.type if token.type == 'ID' or token.type == 'NUM' else token.value}")
                token = scanner.get_next_token()
            
            
if current_state !="$":
    syntax_errors.append(f"#{scanner.line_num} : syntax error, Unexpected EOF")
else:
    lastNode=Node("$", parent=root)


with open('syntax_errors.txt', 'w') as errors:
    for error in syntax_errors:
        errors.write(error + "\n")

for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))

# with open('parse_tree.txt', 'w') as tree:
#     for pre, fill, node in RenderTree(root):
#         tree.write("%s%s" % (pre, node.name))

scanner.close_file()
