import sys


def parse(words, tokens):
    ast = [[]]
    define = False
    for token in tokens:
        match token:       
            case '[':
                ast.append([])
            case ']':
                code = ast.pop()
                ast[-1].append(('push', code))
            case 'is':
                define = True
            case num if num.isdigit():
                ast[-1].append(('push', int(num)))
            case _:
                ast[-1].append(('is' if define else 'call', token))
                define = False
               
    return ast[0]


def execute(words, stack, ast):
    for node in ast:
        match node:
            case ('is', name):
                words[name] = stack.pop()
            case ('push', value):
                stack.append(value)
            case ('call', name):
                if name in words:
                    execute(words, stack, words[name])
                elif name in PRIMS:
                    PRIMS[name](words, stack)
                else:
                    sys.exit('unknown word: ' + name)


def binop(func):
    def word(words, stack):
        tos = stack.pop()
        stack.append(func(stack.pop(), tos))
    return word


def ifelse(words, stack):
    f_ast, t_ast = stack.pop(), stack.pop()
    execute(words, stack, t_ast if stack.pop() else f_ast)


PRIMS = {
    '+': binop(lambda a, b: a + b),
    '-': binop(lambda a, b: a - b),
    '*': binop(lambda a, b: a * b),
    '/': binop(lambda a, b: a // b),
    '<': binop(lambda a, b: int(a < b)),
    'dup': lambda words, stack: stack.append(stack[-1]),
    'drop': lambda words, stack: stack.pop(),
    '.': lambda words, stack: print(stack.pop()),
    'ifelse': ifelse
}


def repl(words, stack):
    while True:
        execute(words, stack, parse(words, input('> ').split()))


source = '''
[ dup * ] is square
[ dup 2 < [ drop 1 ] [ dup 1 - fact * ] ifelse ] is fact
[ dup [ 1 - odd ] [ drop 1 ] ifelse ] is even
[ dup [ 1 - even ] [ drop 0 ] ifelse ] is odd
4 square .
5 fact .
42 dup even . odd .
'''

words, stack = {}, []
execute(words, stack, parse(words, source.split()))
repl(words, stack)
