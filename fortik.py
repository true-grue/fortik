import operator


def parse(tokens):
    stack = [[]]
    op = 'call'
    for token in tokens:
        match token:
            case '[':
                stack.append([])
            case ']':
                code = stack.pop()
                stack[-1].append(('push', code))
            case 'is' | 'to':
                op = token
            case num if num.isdigit():
                stack[-1].append(('push', int(num)))
            case _:
                stack[-1].append((op, token))
                op = 'call'
    return stack[0]


def execute(words, stack, tree):
    words = words.copy()
    for node in tree:
        match node:
            case ('is', name):
                words[name] = stack.pop()
            case ('to', name):
                words[name] = [('push', stack.pop())]
            case ('push', value):
                stack.append(value)
            case ('call', name) if name in words:
                execute(words, stack, words[name])
            case ('call', name) if name in LIB:
                LIB[name](words, stack)
            case _:
                raise SystemExit(f'unknown word: {name}')
    return words


def binop(func):
    def word(words, stack):
        tos = stack.pop()
        stack.append(func(stack.pop(), tos))
    return word


def ifelse(words, stack):
    f_tree, t_tree = stack.pop(), stack.pop()
    execute(words, stack, t_tree if stack.pop() else f_tree)


LIB = {
    '+': binop(operator.add),
    '-': binop(operator.sub),
    '*': binop(operator.mul),
    '/': binop(operator.floordiv),
    '<': binop(operator.lt),
    '.': lambda _, stack: print(stack.pop()),
    'ifelse': ifelse
}


def repl(words, stack):
    while True:
        words = execute(words, stack, parse(input('> ').split()))


tokens = '''
[ to a  a a ] is dup
[ to a ] is drop
[ to b to a  b a ] is swap
[ 0 swap - ] is neg
[ to c to b to a  b b * 4 a c * * - ] is D

5 neg 4 neg 1 D .

[ to n  n 2 < [ 1 ] [ n n 1 - fact * ] ifelse ] is fact

5 fact .

[ to n  n [ n 1 - odd ] [ 1 ] ifelse ] is even
[ to n  n [ n 1 - even ] [ 0 ] ifelse ] is odd

42 dup even . odd .
'''.split()

repl(execute({}, [], parse(tokens)), [])
