# Author: Peter Sovietov

import sys


def parse(source):
    code = []
    tokens = source.split()
    while tokens:
        word = tokens.pop(0)
        if word.isdigit():
            code.append(("num", int(word)))
        elif word in "+-*/<>=":
            code.append(("op", word))
        elif word == ":":
            code.append((":", tokens.pop(0)))
        elif word == ";":
            code.append((";", None))
        elif word == "repeat":
            code.append(("repeat", tokens.pop(0)))
        elif word == "ifelse":
            code.append(("ifelse", (tokens.pop(0), tokens.pop(0))))
        else:
            code.append(("call", word))
    return code


def define(words, name, code, pc):
    compiled = []
    while code[pc] != (";", None):
        compiled.append(code[pc])
        pc += 1
    words[name] = compiled
    return pc + 1


def execute(words, stack, code, pc=0):
    while pc < len(code):
        t, v = code[pc]
        pc += 1
        if t == "num":
            stack.append(v)
        elif t == "op":
            b, a = stack.pop(), stack.pop()
            if v == "+":
                stack.append(a + b)
            elif v == "-":
                stack.append(a - b)
            elif v == "*":
                stack.append(a * b)
            elif v == "/":
                stack.append(a // b)
            elif v == "<":
                stack.append(int(a < b))
            elif v == ">":
                stack.append(int(a > b))
            elif v == "=":
                stack.append(int(a == b))
        elif t == ":":
            pc = define(words, v, code, pc)
        elif t == "call":
            if v in words:
                execute(words, stack, words[v])
            elif v in PRIMS:
                PRIMS[v](words, stack)
            else:
                sys.exit("unknown word: " + v)
        elif t == "repeat":
            for _ in range(stack.pop()):
                execute(words, stack, words[v])
        elif t == "ifelse":
            w = v[0] if stack.pop() else v[1]
            execute(words, stack, words[w])


def repl():
    words, stack = {}, []
    while True:
        execute(words, stack, parse(input("> ")))


def dot(words, stack):
    print(stack.pop())


def dup(words, stack):
    stack.append(stack[-1])


def drop(words, stack):
    stack.pop()


def emit(words, stack):
    print(chr(stack.pop()), end="")


PRIMS = {
    "dup": dup,
    "drop": drop,
    ".": dot,
    "emit": emit
}

source = """
: cr 10 emit ;
: star1 42 emit ;
: star2 10 repeat star1 cr ;
: star 10 repeat star2 ;
star
: fact1 drop 1 ;
: fact2 dup 1 - fact * ;
: fact dup 1 < ifelse fact1 fact2 ;
5 fact .
"""

execute({}, [], parse(source))
repl()
