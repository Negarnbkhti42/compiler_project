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
inputChar = inputFile.read(1)

def get_next_token():
    global lineno
    global inputChar

    value = inputChar

    if value in LETTER:
        inputChar = inputFile.read(1)
        while inputChar != '':
            if inputChar in LETTER or inputChar in DIGIT:
                value += inputChar
            elif inputChar in SYMBOL or inputChar in WHITESPACE:
                return (True, '({}, {})'.format('KEYWORD' if value in KEYWORD else 'ID', value))
            elif inputChar == COMMENT[0]:
                inputChar+=inputChar.read(1)
                if inputChar in COMMENT:
                    return (True, '({}, {})'.format('KEYWORD' if value in KEYWORD else 'ID', value))
                else:
                    value+=inputChar[0]
                    inputChar = inputChar[1]
                    return (False, '({}, Invalid input)'.format(value))
            else:
                value+=inputChar
                return (False, '({}, Invalid input)'.format(value))
            inputChar = inputFile.read(1)
        return (True, '({}, {})'.format('KEYWORD' if value in KEYWORD else 'ID', value))


while True:
    token = get_next_token()
    if token:
        print(token)
    else:
        break
