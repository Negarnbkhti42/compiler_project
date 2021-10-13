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

lineno = 1
starBackslash= ""

SYMBOL_TABLE = set()
TOKENS = {}
ERRORS = {}

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
        while inputChar in DIGIT:
            inputChar = inputFile.read(1)
            value += inputFile.read(1)
            if value.__contains__(LETTER):
                return (False, 'invalid number{}'.format(value))
        return(True,'(DIGIT,{})'.format(value))

# COMMENT///////////////////////////////////////////////////////////////////////////////////////////

    if value == COMMENT[0]:

        if value.startswith("//"):
            inputChar=inputFile.read(1)
            while inputChar != "\n":
                inputChar = inputFile.read(1)
                value += inputChar.read(1)

        if value.startswith("/*"):
            inputChar = inputFile.read(1)
            if inputChar=="*":
                starBackslash=inputChar
                starBackslash+=inputChar
                if starBackslash=="*/":
                    return (True, '(COMMENT,{})'.format(value))
                else:
                    return (False, 'unclosed comment{}'.format(value))


# SYMBOL////////////////////////////////////////////////////////////////////////////////////////////

    if value in SYMBOL:
        if value=="=":
            inputChar = inputFile.read(1)
            if inputChar=="=":
                value+=inputChar
                return (True, '(SYMBOL,{})'.format(value))  #==
            else:
                inputFile.seek(-1, 1)
                return (True, '(SYMBOL,{})'.format(value)) #=
        else:
            (True, '(SYMBOL,{})'.format(value)) # harchizi joz   ==  va  =



while True:
    token = get_next_token()
    if token:
        if token[0]:
            if lineno in TOKENS.keys():
                TOKENS[token[3] if token[1] == 'COMMENT' else lineno].append(f"({token[1]}, {token[2]})")
            else:
                TOKENS[token[3] if token[1] == 'COMMENT' else lineno] = [f"({token[1]}, {token[2]})"]
                
            if token[1] == 'ID':
                SYMBOL_TABLE.add(token[2])
    else:
        break

inputFile.close()
