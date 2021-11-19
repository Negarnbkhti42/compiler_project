class Token:

    def __init__(self, valid, type, value, line):
        self.valid = valid
        self.type = type
        self.value = value
        self.line = line

LETTER = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
DIGIT = set("0123456789")
KEYWORD = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return', 'endif']
SYMBOL = [';', ':', ',', '[', ']', '{', '}', '(', ')', '+', '-', '*', '=', '<']
COMMENT = ['/', '*', '//', '/*', '*/']
WHITESPACE = set(" \n\r\v\t\f")

inputFile = 0

line_num = 1
pointer_position = 0

def openFile(input_file):
    global inputFile
    inputFile = open(input_file, 'r')

def close_file():
    inputFile.close()
    
def get_char():
    ''' Reads one character from file, returns character and position '''
    global pointer_position

    pointer_position += 1
    char = inputFile.read(1)
    if char == '\n':
        pointer_position += 1
    return char


def move_pointer(offset):
    ''' returns back in file '''
    global pointer_position

    pointer_position += offset
    inputFile.seek(pointer_position)
    


def skip_whitespace_and_comment():
    ''' for skipping unneeded whitespaces and comments '''
    
    global line_num

    while True:
        value = get_char()
        if value in WHITESPACE:
            if value == '\n':
                line_num += 1


        elif value == COMMENT[0]:
            value += get_char()

            if value == '//':
                value = get_char()

                while value != '\n' and value != '':
                    value = get_char()

                if value == '\n':
                    line_num += 1
            elif value == '/*':
                start_line = line_num
                input_char = get_char()

                while input_char != '':
                    value += input_char
                    if input_char == '\n':
                        line_num += 1
                    elif input_char == '*':
                        input_char = get_char()

                        if input_char == "/":
                            break
                        elif input_char == '\n':
                            value+= input_char
                            line_num += 1

                    input_char = get_char()
                if input_char == '':
                    return Token(False, 'Unclosed comment', value, start_line)
            else:
                move_pointer(-1)
                if value == '/\n':
                    move_pointer(-1)
                return Token(False, 'Invalid input', value[0], line_num)
        else:
            return value


def get_id(value):
    ''' returns IDs and KEYWORDs '''

    input_char = get_char()
    while input_char != '':

        if input_char in LETTER or input_char in DIGIT:
            value += input_char
        elif input_char in SYMBOL or input_char in WHITESPACE:
            move_pointer(-1)
            return Token(True, 'KEYWORD' if value in KEYWORD else 'ID', value, line_num)
        elif input_char == COMMENT[0]:
            input_char += get_char()

            if input_char in COMMENT:
                move_pointer(-2)
                return Token(True, 'KEYWORD' if value in KEYWORD else 'ID', value, line_num)
            else:
                value += input_char[0]
                move_pointer(-1)
                return Token(False, 'Invalid input', value, line_num)
        else:
            value += input_char
            return Token(False, 'Invalid input', value, line_num)
        input_char = get_char()
    return Token(True, 'KEYWORD' if value in KEYWORD else 'ID', value, line_num)


def get_num(value):
    ''' returns NUMs '''

    input_char = get_char()
    # biad adad haro biabe

    while input_char in DIGIT:
        value += input_char
        input_char = get_char()

    if input_char in LETTER:
        value += input_char
        return Token(False, 'Invalid number', value, line_num)

    if input_char != '':
        move_pointer(-1)
    return Token(True, 'NUM', value, line_num)


def get_symbol(value):
    ''' returns SYMBOLs '''

    if value=="=":
        input_char = get_char()

        if input_char == "=":
            value += input_char
            return Token(True, 'SYMBOL', value, line_num)  # ==
        if input_char in LETTER or input_char in DIGIT or input_char in WHITESPACE or input_char in COMMENT:
            move_pointer(-1)
            return Token(True, 'SYMBOL', value, line_num)  # =
        value += input_char
        return Token(False, 'Invalid input', value, line_num)
    elif value == '*':
        input_char = get_char()

        if input_char == '/':
            value += input_char
            return Token(False, 'Unmatched comment', value, line_num)
        elif input_char in LETTER or input_char in DIGIT or input_char in WHITESPACE:
            move_pointer(-1)
            return Token(True, 'SYMBOL', value, line_num)
        else:
            value += input_char
            return Token(False, 'Invalid input', value, line_num)
    else:
        return Token(True, 'SYMBOL', value, line_num)  # harchizi joz   ==  va  =


def get_new_token():
    ''' the ultimate function for finding tokens '''

    value = skip_whitespace_and_comment()

    if isinstance(value, tuple):
        return value

    if value == '':
        return Token(True, 'EOF', '$', line_num)

    # ID/KEYWORD////////////////////
    if value in LETTER:
        return get_id(value)

    # NUM///////////////////////////

    if value in DIGIT:
        return get_num(value)

    # SYMBOL//////////////////////

    if value in SYMBOL:
        return get_symbol(value)

    return Token(False, 'Invalid input', value, line_num)

def get_next_token():
    while True:
        token = get_new_token()
        if token.valid:
            return token
