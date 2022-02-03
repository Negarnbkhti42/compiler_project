PRODUCTION = {
    'Program': [['Declaration-list', '$']],
    'Declaration-list': [['Declaration', 'Declaration-list'], ['EPSILON']],
    'Declaration': [['Declaration-initial', 'Declaration-prime']],
    'Declaration-initial':  [['Type-specifier', '#add_id', 'ID']],
    'Declaration-prime': [['Fun-declaration-prime'], ['Var-declaration-prime']],
    'Var-declaration-prime': [['#declare_int', ';'], ['[', '#pnum', 'NUM', ']', '#declare_arr', ';']],
    'Fun-declaration-prime':  [['#func_id', '(', 'Params', ')', '#label', '#set_func_temps', '#start_func', 'Compound-stmt', '#end_func', '#return_address', '#declare_func']],
    'Type-specifier': [['#add_type', 'int'], ['#add_type', 'void']],
    'Params': [['#add_type', 'int', '#add_id', 'ID', 'Param-prime', 'Param-list'], ['void']],
    'Param-list': [[',', 'Param', 'Param-list'], ['EPSILON']],
    'Param': [['Declaration-initial', 'Param-prime']],
    'Param-prime': [['#declare_arr', '[', ']'], ['#declare_int', 'EPSILON']],
    'Compound-stmt': [['{', 'Declaration-list', 'Statement-list', '}']],
    'Statement-list': [['Statement', 'Statement-list'], ['EPSILON']],
    'Statement': [['Expression-stmt'], ['Compound-stmt'], ['Selection-stmt'], ['Iteration-stmt'], ['Return-stmt']],
    'Expression-stmt': [['Expression', ';'], ['break', '#break', ';'], [';']],
    'Selection-stmt': [['if', '(', 'Expression', ')', '#save', 'Statement', 'Else-stmt']],
    'Else-stmt': [['#jpf', 'endif'], ['else', '#jpf_save', 'Statement', '#jp', 'endif']],
    'Iteration-stmt': [['repeat', '#save', '#break_start', 'Statement', 'until', '(', 'Expression', ')', '#jpf_iter', '#break_end']],
    'Return-stmt': [['return', 'Return-stmt-prime']],
    'Return-stmt-prime': [[';', '#return'], ['Expression', ';', '#return_value']],
    'Expression': [['Simple-expression-zegond'], ['#pid', 'ID', 'B']],
    'B': [['=', 'Expression', '#assign'], ['[', 'Expression', '#set_index', ']', 'H'], ['Simple-expression-prime']],
    'H': [['=', 'Expression', '#assign'], ['G', 'D', 'C']],
    'Simple-expression-zegond': [['Additive-expression-zegond', 'C']],
    'Simple-expression-prime': [['Additive-expression-prime', 'C']],
    'C': [['Relop', 'Additive-expression', '#op_exec'], ['EPSILON']],
    'Relop': [['#addop', '<'], ['#addop', '==']],
    'Additive-expression': [['Term', 'D']],
    'Additive-expression-prime': [['Term-prime', 'D']],
    'Additive-expression-zegond': [['Term-zegond', 'D']],
    'D': [['Addop', 'Term', '#op_exec', 'D'], ['EPSILON']],
    'Addop': [['#addop', '+'], ['#addop', '-']],
    'Term': [['Factor', 'G']],
    'Term-prime': [['Factor-prime', 'G']],
    'Term-zegond': [['Factor-zegond', 'G']],
    'G': [['#addop', '*', 'Factor', '#op_exec', 'G'], ['EPSILON']],
    'Factor': [['(', 'Expression', ')'], ['#pid', 'ID', 'Var-call-prime'], ['#pnum', 'NUM']],
    'Var-call-prime': [['(', 'Args', ')', '#func_call'], ['Var-prime']],
    'Var-prime': [['[', 'Expression', '#set_index', ']'], ['EPSILON']],
    'Factor-prime': [['(', 'Args', ')', '#func_call'], ['EPSILON']],
    'Factor-zegond': [['(', 'Expression', ')'], ['#pnum', 'NUM']],
    'Args': [['Arg-list'], ['EPSILON']],
    'Arg-list': [['#increase_arg_given', 'Expression', 'Arg-list-prime']],
    'Arg-list-prime': [[',', '#increase_arg_given', 'Expression', 'Arg-list-prime'], ['EPSILON']]
}

FIRST = {
    'Program': ['$', 'int', 'void'],
    'Declaration-list': ['EPSILON', 'int', 'void'],
    'Declaration': ['int', 'void'],
    'Declaration-initial': ['int', 'void'],
    'Declaration-prime': ['(', ';', '['],
    'Var-declaration-prime': [';', '['],
    'Fun-declaration-prime': ['('],
    'Type-specifier': ['int', 'void'],
    'Params': ['int', 'void'],
    'Param-list': [',', 'EPSILON'],
    'Param': ['int', 'void'],
    'Param-prime': ['[', 'EPSILON'],
    'Compound-stmt': ['{'],
    'Statement-list': ['EPSILON', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM'],
    'Statement': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM'],
    'Expression-stmt': ['break', ';', 'ID', '(', 'NUM'],
    'Selection-stmt': ['if'],
    'Else-stmt': ['endif', 'else'],
    'Iteration-stmt': ['repeat'],
    'Return-stmt': ['return'],
    'Return-stmt-prime': [';', 'ID', '(', 'NUM'],
    'Expression': ['ID', '(', 'NUM'],
    'B': ['=', '[', '(', '*', '+', '-', '<', '==', 'EPSILON'],
    'H': ['=', '*', 'EPSILON', '+', '-', '<', '=='],
    'Simple-expression-zegond': ['(', 'NUM'],
    'Simple-expression-prime': ['(', '*', '+', '-', '<', '==', 'EPSILON'],
    'C': ['EPSILON', '<', '=='],
    'Relop': ['<', '=='],
    'Additive-expression': ['(', 'ID', 'NUM'],
    'Additive-expression-prime': ['(', '*', '+', '-', 'EPSILON'],
    'Additive-expression-zegond': ['(', 'NUM'],
    'D': ['EPSILON', '+', '-'],
    'Addop': ['+', '-'],
    'Term': ['(', 'ID', 'NUM'],
    'Term-prime': ['(', '*', 'EPSILON'],
    'Term-zegond': ['(', 'NUM'],
    'G': ['*', 'EPSILON'],
    'Factor': ['(', 'ID', 'NUM'],
    'Var-call-prime': ['(', '[', 'EPSILON'],
    'Var-prime': ['[', 'EPSILON'],
    'Factor-prime': ['(', 'EPSILON'],
    'Factor-zegond': ['(', 'NUM'],
    'Args': ['EPSILON', 'ID', '(', 'NUM'],
    'Arg-list': ['ID', '(', 'NUM'],
    'Arg-list-prime': [',', 'EPSILON']
}

FOLLOW = {
    'Program': [],
    'Declaration-list': ['$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'],
    'Declaration': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'],
    'Declaration-initial': ['(', ';', '[', ',', ')'],
    'Declaration-prime': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'],
    'Var-declaration-prime': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'],
    'Fun-declaration-prime': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'],
    'Type-specifier': ['ID'],
    'Params': [')'],
    'Param-list': [')'],
    'Param': [',', ')'],
    'Param-prime': [',', ')'],
    'Compound-stmt': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'],
    'Statement-list': ['}'],
    'Statement': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'],
    'Expression-stmt': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'],
    'Selection-stmt': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'],
    'Else-stmt': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'],
    'Iteration-stmt': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'],
    'Return-stmt': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'],
    'Return-stmt-prime': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'endif', 'else', 'until'],
    'Expression': [';', ')', ']', ','],
    'B': [';', ')', ']', ','],
    'H': [';', ')', ']', ','],
    'Simple-expression-zegond': [';', ')', ']', ','],
    'Simple-expression-prime': [';', ')', ']', ','],
    'C': [';', ')', ']', ','],
    'Relop': ['(', 'ID', 'NUM'],
    'Additive-expression': [';', ')', ']', ','],
    'Additive-expression-prime': ['<', '==', ';', ')', ']', ','],
    'Additive-expression-zegond': ['<', '==', ';', ')', ']', ','],
    'D': ['<', '==', ';', ')', ']', ','],
    'Addop': ['(', 'ID', 'NUM'],
    'Term': ['+', '-', ';', ')', '<', '==', ']', ','],
    'Term-prime': ['+', '-', '<', '==', ';', ')', ']', ','],
    'Term-zegond': ['+', '-', '<', '==', ';', ')', ']', ','],
    'G': ['+', '-', '<', '==', ';', ')', ']', ','],
    'Factor': ['*', '+', '-', ';', ')', '<', '==', ']', ','],
    'Var-call-prime': ['*', '+', '-', ';', ')', '<', '==', ']', ','],
    'Var-prime': ['*', '+', '-', ';', ')', '<', '==', ']', ','],
    'Factor-prime': ['*', '+', '-', '<', '==', ';', ')', ']', ','],
    'Factor-zegond': ['*', '+', '-', '<', '==', ';', ')', ']', ','],
    'Args': [')'],
    'Arg-list': [')'],
    'Arg-list-prime': [')']
}
