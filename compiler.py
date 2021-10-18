'''
compiler design project

group members:
    Negar Nobakhti 98171201
    Neda Taghizadeh Serajeh 98170743
'''

LETTER = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
          'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
          'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M'
          'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
          'X', 'Y', 'Z']
DIGIT = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
KEYWORD = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return']
SYMBOL = [';', ':', ',', '[', ']', '{', '}', '(', ')', '+', '-', '*', '=', '<']
COMMENT = ['/', '*', '//', '/*', '*/']
WHITESPACE = [' ', '\n', '\r', '\v', '\t', '\f']

inputFile = open('input.txt', 'r')

line_num = 1

RECOGNIZED_IDS = []
TOKENS = {}
ERRORS = {}


def skip_whitespace_and_comment():
    ''' for skipping unneeded whitespaces and comments '''
    
    global line_num

    while True:
        value = inputFile.read(1)
        if value in WHITESPACE:
            if value == '\n':
                line_num += 1


        elif value == COMMENT[0]:
            value += inputFile.read(1)

            if value == '//':
                value = inputFile.read(1)

                while value != '\n' and value != '':
                    value = inputFile.read(1)

                if value == '\n':
                    line_num += 1
            elif value == '/*':
                start_line = line_num
                input_char = inputFile.read(1)

                while input_char != '':
                    value += input_char
                    if input_char == '\n':
                        line_num += 1
                    elif input_char == '*':
                        input_char = inputFile.read(1)

                        if input_char == "/":
                            break

                    input_char = inputFile.read(1)
                if input_char == '':
                    return (False, 'Unclosed comment', value, start_line)
            else:
                inputFile.seek(inputFile.tell() - 1)
                return (False, 'Invalid input', value[0])
        else:
            return value


def get_id(value):
    ''' returns IDs and KEYWORDs '''

    input_char = inputFile.read(1)
    while input_char != '':

        if input_char in LETTER or input_char in DIGIT:
            value += input_char
        elif input_char in SYMBOL or input_char in WHITESPACE:
            inputFile.seek(inputFile.tell() - 1)
            return (True, 'KEYWORD' if value in KEYWORD else 'ID', value)
        elif input_char == COMMENT[0]:
            input_char += input_char.read(1)

            if input_char in COMMENT:
                inputFile.seek(inputFile.tell() - 2)
                return (True, 'KEYWORD' if value in KEYWORD else 'ID', value)
            else:
                value += input_char[0]
                inputFile.seek(inputFile.tell() - 1)
                return (False, 'Invalid input', value)
        else:
            value += input_char
            return (False, 'Invalid input', value)
        input_char = inputFile.read(1)
    return (True, 'KEYWORD' if value in KEYWORD else 'ID', value)


def get_num(value):
    ''' returns NUMs '''

    input_char = inputFile.read(1)
    # biad adad haro biabe

    while input_char in DIGIT:
        value += input_char
        input_char = inputFile.read(1)

    if input_char in LETTER:
        value += input_char
        return (False, 'Invalid number', value)

    if input_char != '':
        inputFile.seek(inputFile.tell() - 1)
    return (True, 'NUM', value)


def get_symbol(value):
    ''' returns SYMBOLs '''

    if value=="=":
        input_char = inputFile.read(1)

        if input_char == "=":
            value += input_char
            return (True, 'SYMBOL', value)  # ==
        if input_char in LETTER or input_char in DIGIT or input_char in WHITESPACE or input_char in COMMENT:
            inputFile.seek(inputFile.tell() - 1)
            return (True, 'SYMBOL', value)  # =
        value += input_char
        return (False, 'Invalid input', value)
    elif value == '*':
        input_char = inputFile.read(1)

        if input_char == '/':
            value += input_char
            return (False, 'Unmatched comment', value)
        elif input_char in LETTER or input_char in DIGIT or input_char in WHITESPACE:
            inputFile.seek(inputFile.tell() - 1)
            return (True, 'SYMBOL', value)
        else:
            value += input_char
            return (False, 'Invalid input', value)
    else:
        return (True, 'SYMBOL', value)  # harchizi joz   ==  va  =


def get_next_token():
    ''' the ultimate function for finding tokens '''

    value = skip_whitespace_and_comment()

    if isinstance(value, tuple):
        return value

    if value == '':
        return None

    # ID/KEYWORD////////////////////
    if value in LETTER:
        return get_id(value)

    # NUM///////////////////////////

    if value in DIGIT:
        return get_num(value)

    # SYMBOL//////////////////////

    if value in SYMBOL:
        return get_symbol(value)

    return (False, 'Invalid input', value)


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
        for keyword in KEYWORD:
            symbol_file.write(f"{index}.\t{keyword}\n")
            index += 1
        for identifier in RECOGNIZED_IDS:
            symbol_file.write(f"{index}.\t{identifier}\n")
            index += 1


while True:
    token = get_next_token()
    if token:
        if token[0]:
            add_token_to_dict(line= line_num,token_type= token[1], token_value= token[2])

        else:
            line = token[3] if token[1] == 'Unclosed comment' else line_num
            addErrorToDict(line= line, error_type=token[1], error_value=token[2])


    else:
        break

inputFile.close()

add_tokens_to_file()
addErrorToFile()
add_symbols_to_table()
