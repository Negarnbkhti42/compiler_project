'''
compiler design project

group members:
    Negar Nobakhti 98171201
    Neda Taghizadeh Serajeh 98170743
'''
import scanner
import Tables
from anytree import Node, RenderTree

def token_matches_branch(token, branch):
    for value in branch:
        if token in Tables.FIRST[value]:
            return True
        if 'EPSILON' not in Tables.FIRST[value]:
            return False


def program_procedure(token):
    procedure = 'Program'
    root = Node(procedure)

    child = declaration_list_procedure(token)
    child.parent = root

    token = scanner.get_next_token()
    if token.value == '$':
        child = Node('$', parent=root)

    return root


def declaration_list_procedure(token):
    procedure = 'Declaration_list'
    root = Node(procedure)

    if token_matches_branch(token, Tables.PRODUCTION[procedure][0]):
        child = declaration_procedure(token)
        child.parent = root
        token = scanner.get_next_token()
        child = declaration_list_procedure(token)
        child.parent = root
    else:
        if token not in Tables.FOLLOW[procedure]:
            pass

    return root


def declaration_procedure(token):
    procedure = 'Declaration'
    root = Node(procedure)

    child = declaration_initial_procedure(token)
    child.parent = root

    token = scanner.get_next_token()
    child = declaration_prime_procedure(token)
    child.parent = root

    return root


def declaration_initial_procedure(token):
    procedure = 'Declaration-initial'
    root = Node(procedure)

    child = type_specifier_procedure(token)
    child.parent = root

    token = scanner.get_next_token()
    if token.type == 'ID':
        child = Node(f"(ID, {token.value})", parent= root)
    
    return root


def declaration_prime_procedure(token):
    procedure = 'Declaration-prime'
    root = Node(procedure)

    if token_matches_branch(token, Tables.PRODUCTION[procedure][0]):
        child = fun_declaration_prime_procedure(token)
        child.parent = root
        return root
    if token_matches_branch(token, Tables.PRODUCTION[1]):
        child = var_declaration_prime_procedure(token)
        child.parent = root
        return root

    # TODO: error handle




scanner.openFile('input.txt')


token = scanner.get_next_token()
tree = program_procedure(token)

scanner.close_file()
