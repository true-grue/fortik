# Author: Peter Sovietov

import sys


def compile_colon(words, tokens):
    name, defined = tokens.pop(0), []
    while tokens[0] != ';':
        defined.append(tokens.pop(0))
    tokens.pop(0)
    words[name] = parse(words, defined)


def parse(words, tokens):
    code = []
    while tokens:
        word = tokens.pop(0)
        if word.isdigit():
            code.append(('int', int(word)))
        elif word == ':':
            compile_colon(words, tokens)
        elif word == 'repeat':
            code += [('code', tokens.pop(0)), ('call', 'repeat')]
        elif word == 'ifelse':
            code += [('code', tokens.pop(0)),
                     ('code', tokens.pop(0)), ('call', 'ifelse')]
        else:
            code.append(('call', word))
    return code


def execute(words, stack, code):
    for t, v in code:
        if t in ('int', 'code'):
            stack.append(v)
        elif t == 'call':
            if v in words:
                execute(words, stack, words[v])
            elif v in PRIMS:
                PRIMS[v](words, stack)
            else:
                sys.exit('unknown word: ' + v)


def binop(func):
    def word(words, stack):
        tos = stack.pop()
        stack.append(func(stack.pop(), tos))
    return word


def repeat(words, stack):
    code = stack.pop()
    for _ in range(stack.pop()):
        execute(words, stack, words[code])


def ifelse(words, stack):
    code2, code1 = stack.pop(), stack.pop()
    execute(words, stack, words[code1 if stack.pop() else code2])


def dup(words, stack):
    stack.append(stack[-1])


def drop(words, stack):
    stack.pop()


def dot(words, stack):
    print(stack.pop())


def emit(words, stack):
    print(chr(stack.pop()), end='')


PRIMS = {
    '+': binop(lambda a, b: a + b),
    '-': binop(lambda a, b: a - b),
    '*': binop(lambda a, b: a * b),
    '/': binop(lambda a, b: a // b),
    '<': binop(lambda a, b: int(a < b)),
    'repeat': repeat,
    'ifelse': ifelse,
    'dup': dup,
    'drop': drop,
    '.': dot,
    'emit': emit
}


def repl(words, stack):
    while True:
        execute(words, stack, parse(words, input('> ').split()))


source = '''
: cr 10 emit ;
: star 42 emit ;
: star-line dup repeat star cr ;
: star-rect repeat star-line drop ;
4 8 star-rect
: fact1 drop 1 ;
: fact2 dup 1 - fact * ;
: fact dup 1 < ifelse fact1 fact2 ;
5 fact .'''

words, stack = {}, []
execute(words, stack, parse(words, source.split()))
repl(words, stack)
