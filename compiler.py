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
token = scanner.get_next_token()

def procedure_is_terminal(procedure):
    return not (procedure in Tables.PRODUCTION.keys())

def token_matches_branch(branch):
    for value in branch:
        is_terminal = procedure_is_terminal(value)
        if is_terminal:
            if token.value == value or token.type == value:
                return True
            return False
        else:
            if token in Tables.FIRST[value]:
                return True
            if 'EPSILON' not in Tables.FIRST[value]:
                return False
    return True


def program_procedure():
    global token

    procedure = 'Program'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure][0]):

        child = declaration_list_procedure()
        child.parent = root

        token = scanner.get_next_token()
        if token.value == '$':
            child = Node('$', parent=root)

        return root
    if token in Tables.FOLLOW[procedure]:
        pass
    else:
        pass


def declaration_list_procedure():
    global token

    procedure = 'Declaration-list'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure][0]):
        child = declaration_procedure()
        child.parent = root
        token = scanner.get_next_token()
        child = declaration_list_procedure()
        child.parent = root
    else:
        child = Node('epsilon', root)

    return root


def declaration_procedure():
    global token

    procedure = 'Declaration'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure][0]):
        child = declaration_initial_procedure()
        child.parent = root

        token = scanner.get_next_token()
        child = declaration_prime_procedure()
        child.parent = root
        return root
    
    if token in Tables.FOLLOW[procedure]:
        pass
    else:
        pass


def declaration_initial_procedure():
    global token

    procedure = 'Declaration-initial'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure][0]):
        child = type_specifier_procedure()
        child.parent = root

        token = scanner.get_next_token()
        if token.type == 'ID':
            child = Node(f"(ID, {token.value})", parent= root)
        else:
            pass
        return root
    
    if token in Tables.FOLLOW[procedure]:
        pass
    else:
        pass


def declaration_prime_procedure():
    global token

    procedure = 'Declaration-prime'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure][0]):
        child = fun_declaration_prime_procedure()
        child.parent = root
        return root
    if token_matches_branch(Tables.PRODUCTION[1]):
        child = var_declaration_prime_procedure()
        child.parent = root
        return root

    if token in Tables.FOLLOW[procedure]:
        pass
    else:
        pass


def var_declaration_prime_procedure():
    global token

    procedure = 'Var-declaration-prime'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[0]):
        if token.value == ';':
            child = Node('(SYMBOL, ;)', parent= root)
        else:
            pass
        return root
    if token_matches_branch(Tables.PRODUCTION[1]):
        if token.value == '[':
            child = Node('(SYMBOL, [)', parent= root)
            token = scanner.get_next_token()
        else:
            pass
        
        if token.type == 'NUM':
            child = Node(f"(NUM, {token.value})", parent= root)
            token = scanner.get_next_token()
        else:
            pass

        if token.value == ']':
            child = Node('(SYMBOL, ])', parent= root)
            token = scanner.get_next_token()
        else:
            pass

        if token.value == ';':
            child = Node('(SYMBOL, ;)', parent= root)
        else:
            pass

        return root

    if token in Tables.FOLLOW[procedure]:
        pass
    else:
        pass


def fun_declaration_prime_procedure():
    global token

    procedure = 'Fun-declaration-prime'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure][0]):
        if token.value == '(':
            child = Node('(SYMBOL, ()', parent= root)
            token = scanner.get_next_token()
        else:
            pass

        child = params_procedure()
        child.parent = root

        if token.value == ')':
            child = Node('(SYMBOL, ))', parent= root)
            token = scanner.get_next_token()
        else:
            pass

        child = compound_stmt_procedure()
        child.parent = root
    
        return root

    if token in Tables.FOLLOW[procedure]:
        pass
    else:
        pass


def type_specifier_procedure():
    global token
    procedure = 'Type-specifier'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure][0]):
        if token.value == 'int':
            child = Node('(KEYWORD, int)', parent= root)
        else:
            pass
        return root
    if token_matches_branch(Tables.PRODUCTION[procedure][1]):
        if token.value == 'void':
            child = Node('(KEYWORD, void)', parent= root)
        else:
            pass
        return root

    if token in Tables.FOLLOW[procedure]:
        pass
    else:
        pass


def params_procedure():
    global token
    procedure= 'Params'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure][0]):
        if token.value == 'int':
            child = Node('(KEYWORD, int)', parent= root)
            token = scanner.get_next_token()
        else:
            pass

        if token.type == 'ID':
            child = Node(f"(ID, {token.value})", parent= root)
            token = scanner.get_next_token()
        else:
            pass
        
        child = param_prime_procedure()
        child.parent = root

        token = scanner.get_next_token()
        child = param_list_procedure()
        child.parent = root

        return root
    if token_matches_branch(Tables.PRODUCTION[procedure][1]):
        if token.value == 'void':
            child = Node('(KEYWORD, void)', parent= root)
        else:
            pass
        return root

    if token in Tables.FOLLOW[procedure]:
        pass
    else:
        pass


def param_list_procedure():
    global token

    procedure = 'Param-list'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure][0]):
        if token.value == ',':
            child = Node('(SYMBOL, ,)', parent= root)
            token = scanner.get_next_token()
        else:
            pass

        child = param_procedure()
        child.parent = root
        
        token = scanner.get_next_token()
        child = param_list_procedure()
        child.parent = root

        return root
    
    child = Node('epsilon', parent= root)
    return root


def param_procedure():
    global token

    procedure = 'Param'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure][0]):
        child = declaration_initial_procedure()
        child.parent = root

        token = scanner.get_next_token()
        child = param_prime_procedure()
        child.parent = root

        return root
    
    if token in Tables.FOLLOW[procedure]:
        pass
    else:
        pass


def param_prime_procedure():
    global token

    procedure = 'Param-prime'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure[0]]):
        if token.value == '[':
            child = Node('(SYMBOL, [)', parent= root)
            token = scanner.get_next_token()
        else:
            pass

        if token.value == ']':
            child = Node('(SYMBOL, ])', parent= root)
        else:
            pass

        return root
    
    if token in Tables.FOLLOW[procedure]:
        pass
    else:
        pass


def compound_stmt_procedure():
    global token

    procedure = 'Compound-stmt'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure][0]):
        if token.value == '{':
            child = Node('(SYMBOL, {)', parent= root)
            token = scanner.get_next_token()
        else:
            pass

        child = declaration_list_procedure()
        child.parent = root
        
        token = scanner.get_next_token()
        child = statement_list_procedure()
        child.parent = root

        token = scanner.get_next_token()
        if token.value == '}':
            child = Node('(SYMBOL, }', parent= root)
        else:
            pass
        return root

    if token in Tables.FOLLOW[procedure]:
        pass
    else:
        pass


def statement_list_procedure():
    global token

    procedure = 'Statement-list'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure][0]):
        child = statement_procedure()
        child.parent = root

        token = scanner.get_next_token()
        child = statement_list_procedure()
        child.parent = root

        return root

    child = Node('epsilon', parent= root)
    return root


def statement_procedure():
    global token

    procedure = 'Statement'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure][0]):
        child = expression_stmt_procedure()
        child.parent = root

        return root

    if token_matches_branch(Tables.PRODUCTION[procedure][1]):
        child = compound_stmt_procedure()
        child.parent = root

        return root

    if token_matches_branch(Tables.PRODUCTION[procedure][2]):
        child = selection_stmt_procedure()
        child.parent = root

        return root

    if token_matches_branch(Tables.PRODUCTION[procedure][3]):
        child = iteration_stmt_procedure()
        child.parent = root

        return root

    if token_matches_branch(Tables.PRODUCTION[procedure][4]):
        child = return_stmt_procedure()
        child.parent = root

        return root

    if token in Tables.FOLLOW[procedure]:
        pass
    else:
        pass


def expression_stmt_procedure():
    global token

    procedure = 'Expression-stmt'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure][0]):
        child = expression_procedure()
        child.parent = root

        token = scanner.get_next_token()
        if token.value == ';':
            child = Node('(SYMBOL, ;)', parent= root)
        else:
            pass
        return root
    if token_matches_branch(Tables.PRODUCTION[procedure][1]):
        if token.value == 'break':
            child = Node('(KEYWORD, break)', parent= root)
            token = scanner.get_next_token()
        else:
            pass

        if token.value == ';':
            child = Node('(SYMBOL, ;)', parent= root)
        else:
            pass
        return root
    if token_matches_branch(Tables.PRODUCTION[procedure][2]):
        if token.value == ';':
            child = Node('(SYMBOL, ;)', parent= root)
        else:
            pass
        return root

    if token in Tables.FOLLOW[procedure]:
        pass
    else:
        pass


def selection_stmt_procedure():
    global token 

    procedure = 'Selection-stmt'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure][0]):
        if token.value == 'if':
            child = Node('(KEYWORD, if)', parent= root)
            token = scanner.get_next_token()
        else:
            pass

        if token.value == '(':
            child = Node('(SYMBOL, ()', parent= root)
            token = scanner.get_next_token()
        else:
            pass

        child = expression_procedure()
        child.parent = root

        token = scanner.get_next_token()
        if token.value == ')':
            child = Node('(SYMBOL, ))', parent= root)
            token = scanner.get_next_token()
        else:
            pass

        child = statement_procedure()
        child.parent = root

        token = scanner.get_next_token()
        child = else_stmt_procedure()
        child.parent = root

        return root
    
    if token in Tables.FOLLOW[procedure]:
        pass
    else:
        pass


def else_stmt_procedure():
    global token

    procedure = 'Else-stmt'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure][0]):
        if token.value == 'endif':
            child = Node('(KEYWORD, endif)', parent= root)
        else:
            pass

        return root
    if token_matches_branch(Tables.PRODUCTION[procedure][1]):
        if token.value == 'else':
            child = Node('(KEYWORD, else)', parent= root)
            token = scanner.get_next_token()
        else:
            pass

        child = statement_procedure()
        child.parent = root

        token = scanner.get_next_token()
        if token.value == 'endif':
            child = Node('(KEYWORD, endif)', parent= root)
        else:
            pass
        return root
    
    if token in Tables.FOLLOW[procedure]:
        pass
    else:
        pass


def iteration_stmt_procedure():
    global token

    procedure = 'Iteration-stmt'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure][0]):
        if token.value == 'repeat':
            child = Node('(KEYWORD, repeat)', parent= root)
            token = scanner.get_next_token()
        else:
            pass

        child = statement_procedure()
        child.parent = root

        token = scanner.get_next_token()
        if token.value == 'until':
            child = Node('(KEYWORD, until)', parent= root)
            token = scanner.get_next_token()
        else:
            pass

        if token.value == '(':
            child = Node('(SYMBOL, ()', parent= root)
            token = scanner.get_next_token()
        else:
            pass

        child = expression_procedure()
        child.parent = root

        token = scanner.get_next_token()
        if token.value == ')':
            child = Node('(SYMBOL, ))', parent= root)
        else:
            pass

        return root
    
    if token in Tables.FOLLOW[procedure]:
        pass
    else:
        pass


def return_stmt_procedure():
    global token

    procedure = 'Return-stmt'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure][0]):
        if token.value == 'return':
            child = Node('(KEYWORD, return)', parent= root)
            token = scanner.get_next_token()
        else:
            pass

        child = return_stmt_prime_procedure()
        child.parent = root

        return root

    if token in Tables.FOLLOW[procedure]:
        pass
    else:
        pass


def return_stmt_prime_procedure():
    global token

    procedure = 'Return-stmt-prime'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure][0]):
        if token.value == ';':
            child = Node('(SYMBOL, ;)', parent= root)
        else:
            pass

        return root
    if token_matches_branch(Tables.PRODUCTION[procedure][1]):
        child = expression_procedure()
        child.parent = root

        token = scanner.get_next_token()
        if token.value == ';':
            child = Node('(SYMBOL, ;)', parent= root)
        else:
            pass

        return root

    if token in Tables.FOLLOW[procedure]:
        pass
    else:
        pass


def expression_procedure():
    global token

    procedure = 'Expression'
    root = Node(procedure)

    if token_matches_branch(Tables.PRODUCTION[procedure][0]):
        child = simple_expression_zegond_procedure()
        child.parent = root

        return root
    if token_matches_branch(Tables.PRODUCTION[procedure][1]):
        if token.type == 'ID':
            child = Node(f"(ID, {token.value})", parent= root)
            token = scanner.get_next_token()
        else:
            pass

        child = b_procedure()
        child.parent = root

        return root
    
    if token in Tables.FOLLOW[procedure]:
        pass
    else:
        pass

tree = program_procedure()

scanner.close_file()


