# Negar Nobakhti 98171201
# Neda Taghizadeh Serajeh 98170743

LETTER = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M'
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
DIGIT = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
KEYWORD = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return']
SYMBOL = [';', ':', ',', '[', ']', '{', '}', '(', ')', '+', '-', '*', '=', '<']
SLASH = '/'
STAR = '*'
WHITESPACE = [' ', '\n', '\r', '\v', '\t', '\f']

inputFile = open('input.txt', 'r')
lines = inputFile.readlines()

lineno = 3
position = 3

def get_next_token():
    global position
    global lineno

    if position >= len(lines[lineno - 1]):
        if lineno == len(lines):
            return None
        lineno+=1
        position = 0

    line = lines[lineno - 1]
    value = line[position]

    if value in LETTER:
        for position in range(position, len(line)):
            if line[position] in LETTER or line[position] in DIGIT:
                value += line[position]
            elif line[position] in SYMBOL or line[position in WHITESPACE]:
                return (True, '({}, {})'.format('KEYWORD' if value in KEYWORD else 'ID', value))
            elif line[position] == SLASH:
                if line[position + 1] == SLASH or line[position + 1] == STAR:
                    return (True, '(id, {})'.format(value))
                else:
                    value += line[position]
                    return (False, '({}, Invalid input)'.format(value))
            else:
                value += line[position]
                return (False, '({}, Invalid input)'.format(value))

while lineno <= len(lines):
    token = get_next_token()
