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

def get_id(value):
    input_char = inputFile.read(1)
    while input_char != '':
        if input_char in LETTER or input_char in DIGIT:
            value += input_char
        elif input_char in SYMBOL or input_char in WHITESPACE:
            inputFile.seek(-1, 1)
            return True, 'KEYWORD' if value in KEYWORD else 'ID', value
        elif input_char == COMMENT[0]:
            input_char+=input_char.read(1)
            if input_char in COMMENT:
                inputFile.seek(-2, 1)
                return True, 'KEYWORD' if value in KEYWORD else 'ID', value
            else:
                value+=input_char[0]
                inputFile.seek(-1, 1)
                return False, 'Invalid input', value
        else:
            value+=input_char
            return False, 'Invalid input', value
        input_char = inputFile.read(1)
    return True, 'KEYWORD' if value in KEYWORD else 'ID', value


def get_num(value):
    input_char = inputFile.read(1)
    while input_char in DIGIT:
        value += input_char
        input_char = inputFile.read(1)
    if input_char in LETTER:
        value += input_char
        return False, 'Invalind number', value
    else:
        if input_char != '':
            inputFile.seek(-1, 1)
        return True, 'NUM', value


def getComment(value):
    global line_num

    input_char = value + inputFile.read(1)

    if input_char == COMMENT[2]:
        value = input_char
        input_char=inputFile.read(1)
        while input_char != "\n" or input_char != '':
            value += input_char
            input_char = inputFile.read(1)
        if input_char == '\n':
            inputFile.seek(-1, 1)
        return True, 'COMMENT', value

    if input_char == COMMENT[3]:
        value = input_char
        input_char = inputFile.read(1)
        start_line = line_num

        while input_char != '':
            if input_char == COMMENT[1]:
                input_char += inputFile.read(1)
                if input_char == COMMENT[4]:
                    return True, 'COMMENT', value, start_line
            if input_char == '\n':
                line_num += 1
            value += input_char
            input_char = inputFile.read(1)
        return False, 'Unclosed comment', value, start_line


def get_symbol(value):
    if value=="=":
        input_char = inputFile.read(1)
        if input_char=="=":
            value+=input_char
            return True, 'SYMBOL', value # ==
        else:
            inputFile.seek(-1, 1)
            return True, 'SYMBOL', value # =
    else:
        return True, 'SYMBOL', value # harchizi joz   ==  va  =


def get_next_token():
    global line_num

    input_char = inputFile.read(1)
    value = input_char

    while value in WHITESPACE:
        value = inputFile.read(1)
        if value == '\n':
            line_num += 1

    if value == '':
        return None


# ID/KEYWORD////////////////////////////////////////////////////////////////////////////////////////
    if value in LETTER:
        return get_id(value)

# NUM///////////////////////////////////////////////////////////////////////////////////////////////

    if value in DIGIT:
        # biad adad haro biabe
        return get_num(value)

# COMMENT///////////////////////////////////////////////////////////////////////////////////////////

    if value == COMMENT[0]:
        return getComment(value)

    if value == COMMENT[1]:
        input_char += inputFile.read(1)
        if input_char == COMMENT[4]:
            value = input_char
            return False, 'Unmatched comment', value
        else:
            inputFile.seek(-1, 1)


# SYMBOL////////////////////////////////////////////////////////////////////////////////////////////

    if value in SYMBOL:
        return get_symbol(value)



while True:
    token = get_next_token()
    if token:
        print(token)
    else:
        break

inputFile.close()
