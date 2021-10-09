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

INPUT_FILE = open('input.txt', 'r')

lineno = 1

def get_next_token():
    global lineno
    global INPUT_FILE

    inputChar = INPUT_FILE.read(1)
    value = inputChar
    if value in LETTER:
        inputChar = INPUT_FILE.read(1)
        while inputChar != '':
            if inputChar in LETTER or inputChar in DIGIT:
                value += inputChar
            elif inputChar in SYMBOL or inputChar in WHITESPACE or inputChar in COMMENT:
                INPUT_FILE.seek(-1, 1)
                return (True, '({}, {})'.format('KEYWORD' if value in KEYWORD else 'ID', value))
            else:
                value+=inputChar
                return (False, '({}, Invalid input)'.format(value))
            inputChar = INPUT_FILE.read(1)
        return (True, '({}, {})'.format('KEYWORD' if value in KEYWORD else 'ID', value))

# //////////////////////////////////////////////////////////////////////////////////////////////////
    if value in DIGIT:
        inputChar = INPUT_FILE.read(1)

        # biad adad haro biabe
        while inputChar != '':
            if inputChar in DIGIT:
                value += inputChar
            elif inputChar in LETTER:
                value += inputChar
                return (False, '{}, invalid number'.format(value))
            else:
                INPUT_FILE.seek(-1, 1)
                return (True, '(NUM, {})'.format(value))
            inputChar = INPUT_FILE.read(1)
        return (True, '(NUM, {})'.format(value))

# //////////////////////////////////////////////////////////////////////////////////////////////////
    return (False, f"({value}, invalid input")

while True:
    token = get_next_token()
    if token:
        print(token)
    else:
        break
