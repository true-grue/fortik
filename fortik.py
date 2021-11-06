import sys


def parse(words, tokens, pos=0):
    ast = [[]]
    while pos < len(tokens):
        if tokens[pos] == '[':
            ast.append([])
        elif tokens[pos] == ']':
            quote = ast.pop()
            ast[-1].append(('push', quote))
        elif tokens[pos] == 'is':
            pos += 1
            name = tokens[pos]
            words[name] = ast[-1].pop()[1]
        elif tokens[pos].isdigit():
            ast[-1].append(('push', int(tokens[pos])))
        else:
            ast[-1].append(('call', tokens[pos]))
        pos += 1
    return ast[0]


def execute(words, stack, ast):
    for tag, val in ast:
        if tag == 'push':
            stack.append(val)
        elif tag == 'call':
            if val in words:
                execute(words, stack, words[val])
            elif val in PRIMS:
                PRIMS[val](words, stack)
            else:
                sys.exit('unknown word: ' + val)


def dup(words, stack):
    stack.append(stack[-1])


def drop(words, stack):
    stack.pop()


def dot(words, stack):
    print(stack.pop())


def emit(words, stack):
    print(chr(stack.pop()), end='')


def ifelse(words, stack):
    f_ast, t_ast = stack.pop(), stack.pop()
    execute(words, stack, t_ast if stack.pop() else f_ast)


def binop(func):
    def word(words, stack):
        tos = stack.pop()
        stack.append(func(stack.pop(), tos))
    return word


PRIMS = {
    '+': binop(lambda a, b: a + b),
    '-': binop(lambda a, b: a - b),
    '*': binop(lambda a, b: a * b),
    '/': binop(lambda a, b: a // b),
    '<': binop(lambda a, b: int(a < b)),
    'dup': dup,
    'drop': drop,
    '.': dot,
    'emit': emit,
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
