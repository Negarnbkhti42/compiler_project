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
            if True:
                return i

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
current_state = 'Program'

if token.value in Tables.FIRST[current_state] or 'EPSILON' in Tables.FIRST[current_state]:
    root = Node(current_state)
    state = Diagram(current_state)


while True:
    current_state = state.get_value()

    if token.value =='$' and current_state != '$':
        # unexpected eof error
        break

    if is_terminal(current_state):

        if token.value == current_state or token.type == current_state:
            # matches. move both state and token
            child = Node(f"({token.type}, {token.value})", parent= root)
            token = scanner.get_next_token()
            if not state.move_forward():
                state = STATE_STACK.pop()
                root = root.parent
        else:
            # missing token. change token without moving state
            token = scanner.get_next_token()

    else:

        if token in Tables.FIRST[current_state] or 'EPSILON' in Tables.FIRST[current_state]:
            state = Diagram(current_state)
            child = Node(current_state, parent= root)
            root = child

        else:

            if token in Tables.FOLLOW[current_state]:
                # missing procedure error. move state without changing the token
                if not state.move_forward():
                    state = STATE_STACK.pop()
                    root = root.parent

            else:
                # illegal procedure error. don't move state and change token
                token = scanner.get_next_token()

scanner.close_file()


