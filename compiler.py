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

lineNum = 1

def get_next_token():
    global lineNum
    global inputFile

    input_char = inputFile.read(1)
    value = input_char

    while value in WHITESPACE:
        value = inputFile.read(1)
        if value == '\n':
            lineNum += 1

    if value == '':
        return None


# ID/KEYWORD////////////////////////////////////////////////////////////////////////////////////////
    if value in LETTER:
        input_char = inputFile.read(1)
        while input_char != '':
            if input_char in LETTER or input_char in DIGIT:
                value += input_char
            elif input_char in SYMBOL or input_char in WHITESPACE:
                inputFile.seek(-1, 1)
                return (True, '({}, {})'.format('KEYWORD' if value in KEYWORD else 'ID', value))
            elif input_char == COMMENT[0]:
                input_char+=input_char.read(1)
                if input_char in COMMENT:
                    inputFile.seek(-2, 1)
                    return (True, '({}, {})'.format('KEYWORD' if value in KEYWORD else 'ID', value))
                else:
                    value+=input_char[0]
                    inputFile.seek(-1, 1)
                    return (False, '({}, Invalid input)'.format(value))
            else:
                value+=input_char
                return (False, '({}, Invalid input)'.format(value))
            input_char = inputFile.read(1)
        return (True, '({}, {})'.format('KEYWORD' if value in KEYWORD else 'ID', value))

# NUM///////////////////////////////////////////////////////////////////////////////////////////////

    if value in DIGIT:
        # biad adad haro biabe
        input_char = inputFile.read(1)
        while input_char in DIGIT:
            value += input_char
            input_char = inputFile.read(1)
        if input_char in LETTER:
            value += input_char
            return (False, 'invalid number{}'.format(value))
        else:
            if input_char != '':
                inputFile.seek(-1, 1)
            return (True,'(DIGIT,{})'.format(value))

# COMMENT///////////////////////////////////////////////////////////////////////////////////////////

    if value == COMMENT[0]:
        input_char += inputFile.read(1)

        if input_char == COMMENT[2]:
            value = input_char
            input_char=inputFile.read(1)
            while input_char != "\n" or input_char != '':
                value += input_char
                input_char = inputFile.read(1)
            if input_char == '\n':
                inputFile.seek(-1, 1)
            return (True, '(Comment, {}'.format(value))

        if input_char == COMMENT[3]:
            value = input_char
            input_char = inputFile.read(1)
     
            while input_char != '':
                if input_char == COMMENT[1]:
                    input_char += inputFile.read(1)
                    if input_char == COMMENT[4]:
                        return (True, '(COMMENT,{})'.format(value))
                value += input_char
                input_char = inputFile.read(1)

            return (False, 'unclosed comment{}'.format(value))
        
    if value == COMMENT[1]:
        input_char += inputFile.read(1)
        if input_char == COMMENT[4]:
            value = input_char
            return (False, 'unmatched comment, {}'.format(value))
        else:
            inputFile.seek(-1, 1)


# SYMBOL////////////////////////////////////////////////////////////////////////////////////////////

    if value in SYMBOL:
        if value=="=":
            input_char = inputFile.read(1)
            if input_char=="=":
                value+=input_char
                return (True, '(SYMBOL,{})'.format(value))  #==
            else:
                inputFile.seek(-1, 1)
                return (True, '(SYMBOL,{})'.format(value)) #=
        else:
            return (True, '(SYMBOL,{})'.format(value)) # harchizi joz   ==  va  =



while True:
    token = get_next_token()
    if token:
        print(token)
    else:
        break

inputFile.close()
