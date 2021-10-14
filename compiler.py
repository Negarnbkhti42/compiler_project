# Negar Nobakhti 98171201
# Neda Taghizadeh Serajeh 98170743

LETTER = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M'
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
DIGIT = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
KEYWORD = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return']
SYMBOL = [';', ':', ',', '[', ']', '{', '}', '(', ')', '+', '-', '*', '=', '<']
COMMENT = ['/', '*', '//' , '/*', '*/']
WHITESPACE = [' ', '\n', '\r', '\v', '\t', '\f']

inputFile = open('input.txt', 'r')

line_num = 1

SYMBOL_TABLE = set()
TOKENS = {}
ERRORS = {}


def get_id(value):
    inputChar = inputFile.read(1)
    while inputChar != '':

        if inputChar in LETTER or inputChar in DIGIT:
            value += inputChar
        elif inputChar in SYMBOL or inputChar in WHITESPACE:
            inputFile.seek(inputFile.tell()-1)
            return (True, 'KEYWORD' if value in KEYWORD else 'ID', value)
        elif inputChar == COMMENT[0]:
            inputChar+=inputChar.read(1)

            if inputChar in COMMENT:
                inputFile.seek(inputFile.tell() -2)
                return (True, 'KEYWORD' if value in KEYWORD else 'ID', value)
            else:
                value+=inputChar[0]
                inputFile.seek(inputFile.tell() -1)
                return (False, 'Invalid input', value)
        else:
            value+=inputChar
            return (False, 'Invalid input', value)
        inputChar = inputFile.read(1)
    return (True, 'KEYWORD' if value in KEYWORD else 'ID', value)


def get_num(value):
    inputChar = inputFile.read(1)
    # biad adad haro biabe

    while inputChar in DIGIT:
        value += inputChar
        inputChar = inputFile.read(1)

    if inputChar in LETTER:
        value += inputChar
        return (False, 'Invalid number', value)

    if inputChar != '':
        inputFile.seek(inputFile.tell() -1)
    return(True,'NUM', value)


def get_comment(value):
    global line_num

    value += inputFile.read(1)

    if value == '//':
        inputChar=inputFile.read(1)

        while inputChar != '\n' and inputChar != '':
            value += inputChar
            inputChar = inputFile.read(1)

        if inputChar != '':
            inputFile.seek(inputFile.tell() -1)
        return (True, 'COMMENT', value, line_num)
    elif value == '/*':
        start_line = line_num
        inputChar = inputFile.read(1)

        while inputChar != "":
            value += inputChar

            if inputChar == '\n':
                line_num += 1
            elif inputChar=="*":
                inputChar = inputFile.read(1)

                if inputChar == "/":
                    value += inputChar
                    return (True, 'COMMENT', value, start_line)
                else:
                    inputFile.seek(inputFile.tell() -1)

            inputChar = inputFile.read(1)
        return (False, 'Unclosed comment', value, start_line)
    else:
        inputFile.seek(inputFile.tell() -1)
        return (False, 'Invalid input', value, start_line)


def get_symbol(value):
    if value=="=":
        inputChar = inputFile.read(1)

        if inputChar=="=":
            value+=inputChar
            return (True, 'SYMBOL', value)  #==
        else:
            inputFile.seek(inputFile.tell() -1)
            return (True, 'SYMBOL', value) #=
    elif value == '*':
        inputChar = inputFile.read(1)

        if inputChar == '/':
            value += inputChar
            return (False, 'Unmatched comment', value)
        else:
            inputFile.seek(inputFile.tell() -1)
            return (True, 'SYMBOL', value)
    else:
        return (True, 'SYMBOL', value) # harchizi joz   ==  va  =


def get_next_token():
    global line_num

    input_char = inputFile.read(1)
    value = input_char

    while value in WHITESPACE:
        if value == '\n':
            line_num += 1
        value = inputFile.read(1)

    if value == '':
        return None


# ID/KEYWORD////////////////////
    if value in LETTER:
        return get_id(value)

# NUM///////////////////////////

    if value in DIGIT:
        return get_num(value)

# COMMENT//////////////////////

    if value == COMMENT[0]:
        return get_comment(value)



# SYMBOL//////////////////////

    if value in SYMBOL:
        return get_symbol(value)

    return (False, 'Invalid input', value)



while True:
    token = get_next_token()
    if token:
        if token[0]:
            line = str(token[3] if token[1] == 'COMMENT' else line_num)
            if line in TOKENS.keys():
                TOKENS[line].append(f"({token[1]}, {token[2]})")
            else:
                TOKENS[line] = [f"({token[1]}, {token[2]})"]

            if token[1] == 'ID':
                SYMBOL_TABLE.add(token[2])
    else:
        break

inputFile.close()
