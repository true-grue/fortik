import sys


def parse(words, tokens):
    ast, new = [[]], False
    for token in tokens:
        if new:
            words[token] = ast[-1].pop()[1]
            new = False
        elif token == '[':
            ast.append([])
        elif token == ']':
            quote = ast.pop()
            ast[-1].append(('push', quote))
        elif token == 'is':
            new = True
        elif token.isdigit():
            ast[-1].append(('push', int(token)))
        else:
            ast[-1].append(('call', token))
    return ast[0]


def execute(words, stack, ast):
    for op, val in ast:
        if op == 'push':
            stack.append(val)
        elif op == 'call':
            if val in words:
                execute(words, stack, words[val])
            elif val in PRIMS:
                PRIMS[val](words, stack)
            else:
                sys.exit('unknown word: ' + val)


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
[
  dup 1 < [ drop 1 ] [ dup 1 - fact * ] ifelse
] is fact
5 fact .
'''

words, stack = {}, []
execute(words, stack, parse(words, source.split()))
repl(words, stack)
