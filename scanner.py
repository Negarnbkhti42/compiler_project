class Token:

    def __init__(self, valid, type, value, line):
        self.valid = valid
        self.type = type
        self.value = value
        self.line = line


LETTER = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
DIGIT = set("0123456789")
KEYWORD = ['if', 'else', 'void', 'int', 'repeat',
           'break', 'until', 'return', 'endif']
SYMBOL = [';', ':', ',', '[', ']', '{', '}', '(', ')', '+', '-', '*', '=', '<']
COMMENT = ['/', '//', '/*', '*/']
WHITESPACE = set(" \n\r\v\t\f")

inputFile = 0

line_num = 1
last_read = ' '


def openFile(input_file):
    global inputFile
    inputFile = open(input_file, 'r')


def close_file():
    inputFile.close()


def get_char():
    ''' Reads one character from file, returns character and position '''
    global last_read
    global line_num

    if last_read == '\n':
        line_num += 1
    last_read = inputFile.read(1)
    return last_read


def skip_whitespace_and_comment():
    ''' for skipping unneeded whitespaces and comments '''

    global line_num
    global last_read

    value = last_read

    while True:

        if value == COMMENT[0] or value == COMMENT[2] or value == COMMENT[3]:
            if value == COMMENT[0]:
                value += get_char()

            if value == '//':
                value = get_char()

                while value != '\n' and value != '':
                    value = get_char()

            elif value == '/*':
                start_line = line_num
                input_char = get_char()

                while input_char != '':
                    value += input_char
                    if input_char == '*':
                        input_char = get_char()

                        if input_char == "/":
                            break

                    input_char = get_char()
                if input_char == '':
                    return Token(False, 'Unclosed comment', value, start_line)
            else:
                return Token(False, 'Invalid input', value[0], line_num)
        elif value not in WHITESPACE:
            return value
        value = get_char()


def get_id(value):
    ''' returns IDs and KEYWORDs '''
    global last_read

    input_char = get_char()
    while input_char != '':

        if input_char in LETTER or input_char in DIGIT:
            value += input_char
        elif input_char in SYMBOL or input_char in WHITESPACE:
            return Token(True, 'KEYWORD' if value in KEYWORD else 'ID', value, line_num)
        elif input_char == COMMENT[0]:
            input_char += get_char()

            if input_char in COMMENT:
                last_read = input_char

                return Token(True, 'KEYWORD' if value in KEYWORD else 'ID', value, line_num)
            else:
                value += input_char[0]
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

    return Token(True, 'NUM', value, line_num)


def get_symbol(value):
    ''' returns SYMBOLs '''

    if value == "=":
        input_char = get_char()

        if input_char == "=":
            value += input_char
            get_char()
            return Token(True, 'SYMBOL', value, line_num)  # ==
        if input_char in LETTER or input_char in DIGIT or input_char in WHITESPACE or input_char in COMMENT:
            return Token(True, 'SYMBOL', value, line_num)  # =
        value += input_char
        return Token(False, 'Invalid input', value, line_num)
    elif value == '*':
        input_char = get_char()

        if input_char == '/':
            value += input_char
            get_char()
            return Token(False, 'Unmatched comment', value, line_num)
        elif input_char in LETTER or input_char in DIGIT or input_char in WHITESPACE:
            return Token(True, 'SYMBOL', value, line_num)
        else:
            value += input_char
            return Token(False, 'Invalid input', value, line_num)
    else:
        # harchizi joz   ==  va  =
        get_char()
        return Token(True, 'SYMBOL', value, line_num)


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
