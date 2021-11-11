'''
compiler design project

group members:
    Negar Nobakhti 98171201
    Neda Taghizadeh Serajeh 98170743
'''
import scanner

RECOGNIZED_IDS = []
TOKENS = {}
ERRORS = {}

def add_token_to_dict(line, token_type, token_value):
    ''' adds valid tokens to the dict object '''

    if line in TOKENS.keys():
        TOKENS[line].append(f"({token_type}, {token_value})")
    else:
        TOKENS[line] = [f"({token_type}, {token_value})"]

    if token_type == 'ID' and token_value not in RECOGNIZED_IDS:
        RECOGNIZED_IDS.append(token_value)


def add_tokens_to_file():
    ''' puts all recognized tokens in a file '''

    with open('tokens.txt', 'w+') as tokenFile:
        for line, tokens in TOKENS.items():
            tokenFile.write(f"{line}.\t{' '.join(tokens)}\n")


def addErrorToDict(line, error_type, error_value):
    ''' adds errors to the dict object'''

    if line in ERRORS.keys():
        ERRORS[line].append(f"({error_value}, {error_type})")
    else:
        ERRORS[line] = [f"({error_value}, {error_type})"]


def addErrorToFile():
    ''' put all errors in a file '''

    fileForError = open('lexical_errors.txt', 'w+')

    if len(ERRORS) == 0:
        fileForError.write("There is no lexical error.")
    else:
        for line, error in ERRORS.items():
            fileForError.write(f"{line}.\t{' '.join(error)}\n")

    fileForError.close()

def add_symbols_to_table():
    '''put all symbols in a file '''

    with open('symbol_table.txt', 'w+') as symbol_file:
        index = 1
        for keyword in scanner.KEYWORD:
            symbol_file.write(f"{index}.\t{keyword}\n")
            index += 1
        for identifier in RECOGNIZED_IDS:
            symbol_file.write(f"{index}.\t{identifier}\n")
            index += 1

scanner.openFile('input.txt')

while True:
    token = scanner.get_next_token()
    if token:
        if token[0]:
            add_token_to_dict(line= scanner.line_num,token_type= token[1], token_value= token[2])

        else:
            line = 0
            value = ''
            if token[1] == 'Unclosed comment':
                line = token[3]
                if len(token[2]) > 7:
                    value = token[2][:7] + '...'
                else:
                    value = token[2]
            else:
                line = scanner.line_num
                value = token[2]

            addErrorToDict(line= line, error_type=token[1], error_value=value)


    else:
        break

scanner.close_file()

add_tokens_to_file()
addErrorToFile()
add_symbols_to_table()
