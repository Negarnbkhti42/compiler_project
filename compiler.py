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

def is_terminal(phrase):
    return phrase not in Tables.PRODUCTION

STATE_STACK = []
token = None

class Diagram:

    def __init__(self, procedure):
        self.procedure = procedure
        self.branch = self.get_branch()
        self.level = 0

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
        return Tables.PRODUCTION[self.procedure][self.branch][self.level]

    def move_forward(self):
        if self.level < len(Tables.PRODUCTION[self.procedure][self.branch]) - 1:
            self.level += 1
            return True
        return False


token = scanner.get_next_token()
level = Diagram('Program')
root = Node('Program')


def move_to_next_state():
    global level
    global root

    while not level.move_forward():
        level = STATE_STACK.pop()
        root = root.parent

while True:
    current_state = level.get_value()

    if current_state == 'EPSILON':
        Child = Node('epsilon', parent= root)
        move_to_next_state()
        

    elif is_terminal(current_state):
        if token.value == current_state or token.type == current_state:
            # matches. move both level and token
            if token.value == '$':
                child = Node('$', parent= root)
                break
            child = Node(f"({token.type}, {token.value})", parent= root)
            token = scanner.get_next_token()
            move_to_next_state()
        else:
            # missing token. don't change token and move level
            syntax_errors.append(f"#{scanner.line_num} : syntax error, missing {current_state}")
            move_to_next_state()

    else: # non-terminal level
        if token.value in Tables.FIRST[current_state] or token.type in Tables.FIRST[current_state] or 'EPSILON' in Tables.FIRST[current_state]:
            STATE_STACK.append(level)
            level = Diagram(current_state)
            child = Node(current_state, parent= root)
            root = child

        else:
            if token in Tables.FOLLOW[current_state]:
                # missing procedure error. move level without changing the token
                syntax_errors.append(f"#{scanner.line_num} : syntax error, missing {current_state}")
                move_to_next_state()

            else:
                # illegal procedure error. don't move level and change token
                if token.value == '$':
                    syntax_errors.append(f"#{scanner.line_num} : syntax error, Unexpected EOF")
                    break
                else:
                    syntax_errors.append(f"#{scanner.line_num} : syntax error, illegal {token.type if token.type == 'ID' or token.type == 'NUM' else token.value}")
                    token = scanner.get_next_token()
 

with open('syntax_errors.txt', 'w', encoding= "utf-8") as errors:
    if len(syntax_errors)==0:
        errors.write("There is no syntax error.")
    else:
        for error in syntax_errors:
            errors.write(error + "\n")

with open('parse_tree.txt', 'w', encoding= "utf-8") as tree:
    for pre, fill, node in RenderTree(root):
        tree.write("%s%s" % (pre, node.name) + "\n")

scanner.close_file()
