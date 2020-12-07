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
        elif word[0] == ":":
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
    start_pc = pc
    while code[pc - 1] != (";", None):
        pc += 1
    words[name] = code[start_pc:pc]
    return pc


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
            n = stack.pop()
            for _ in range(n):
                execute(words, stack, words[v])
        elif t == "ifelse":
            w1, w2 = v
            if stack.pop():
                execute(words, stack, words[w1])
            else:
                execute(words, stack, words[w2])
        elif t == "ret":
            break
    return pc


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
