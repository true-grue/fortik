import sys


def parse(words, tokens):
    ast, op = [[]], 'call'
    for token in tokens:
        match token:
            case '[':
                ast.append([])
            case ']':
                code = ast.pop()
                ast[-1].append(('push', code))
            case 'is' | 'to':
                op = token
            case num if num.isdigit():
                ast[-1].append(('push', int(num)))
            case _:
                ast[-1].append((op, token))
                op = 'call'
    return ast[0]


def execute(words, stack, ast):
    for node in ast:
        match node:
            case ('is', name):
                words[name] = stack.pop()
            case ('to', name):
                words[name] = [('push', stack.pop())]
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
[ dup 2 < [ drop 1 ] [ dup 1 - fact * ] ifelse ] is fact  5 fact .
[ dup [ 1 - odd ] [ drop 1 ] ifelse ] is even
[ dup [ 1 - even ] [ drop 0 ] ifelse ] is odd  42 dup even . odd .
[ to b to a  b a ] is swap
[ 0 swap - ] is neg
[ to a to b to c  b b * 4 a c * * - ] is D  5 neg 4 neg 1 D .
'''

words, stack = {}, []
execute(words, stack, parse(words, source.split()))
repl(words, stack)
