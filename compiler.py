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


def skip_whitespace_and_comment():
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
                else:
                    return value
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
                if value == '':
                    return (False, 'Unclosed comment', value, start_line)
            else:
                inputFile.seek(inputFile.tell() -1)
                return (False, 'Invalid input', value[0])
        else:
            return value

def get_id(value):
    input_char = inputFile.read(1)
    while input_char != '':

        if input_char in LETTER or input_char in DIGIT:
            value += input_char
        elif input_char in SYMBOL or input_char in WHITESPACE:
            inputFile.seek(inputFile.tell()-1)
            return (True, 'KEYWORD' if value in KEYWORD else 'ID', value)
        elif input_char == COMMENT[0]:
            input_char+=input_char.read(1)

            if input_char in COMMENT:
                inputFile.seek(inputFile.tell() -2)
                return (True, 'KEYWORD' if value in KEYWORD else 'ID', value)
            else:
                value+=input_char[0]
                inputFile.seek(inputFile.tell() -1)
                return (False, 'Invalid input', value)
        else:
            value+=input_char
            return (False, 'Invalid input', value)
        input_char = inputFile.read(1)
    return (True, 'KEYWORD' if value in KEYWORD else 'ID', value)


def get_num(value):
    input_char = inputFile.read(1)
    # biad adad haro biabe

    while input_char in DIGIT:
        value += input_char
        input_char = inputFile.read(1)

    if input_char in LETTER:
        value += input_char
        return (False, 'Invalid number', value)

    if input_char != '':
        inputFile.seek(inputFile.tell() -1)
    return(True,'NUM', value)


def get_symbol(value):
    if value=="=":
        input_char = inputFile.read(1)

        if input_char=="=":
            value+=input_char
            return (True, 'SYMBOL', value)  #==
        if input_char in LETTER or input_char in DIGIT or input_char in WHITESPACE or input_char in COMMENT:
            inputFile.seek(inputFile.tell() -1)
            return (True, 'SYMBOL', value) #=
        value += input_char
        return (False, 'Invalid input', value)
    elif value == '*':
        input_char = inputFile.read(1)

        if input_char == '/':
            value += input_char
            return (False, 'Unmatched comment', value)
        else:
            inputFile.seek(inputFile.tell() -1)
            return (True, 'SYMBOL', value)
    else:
        return (True, 'SYMBOL', value) # harchizi joz   ==  va  =


def get_next_token():
    global line_num

    value = skip_whitespace_and_comment()

    if value is tuple:
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



while True:
    token = get_next_token()
    if token:
        if token[0]:

            if line_num in TOKENS.keys():
                TOKENS[line_num].append(f"({token[1]}, {token[2]})")
            else:
                TOKENS[line_num] = [f"({token[1]}, {token[2]})"]

            if token[1] == 'ID' or token[1] == 'KEYWORD':
                SYMBOL_TABLE.add(token[2])
    else:
        break

inputFile.close()


with open('tokens.txt', 'w+') as tokenFile:
    for line in TOKENS:
        tokenFile.write(f"{line}.\t{' '.join(TOKENS[line])}\n")

