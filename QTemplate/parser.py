import random

from fractions import Fraction
from lark import Lark


GRAMMAR = """
start: syntax

syntax: "整数" NUMBER NUMBER -> int
      | "小数" NUMBER NUMBER [NUMBER] -> float
      | "分数" NUMBER NUMBER -> fraction
      | "质数" NUMBER NUMBER -> prime

%import common.INT -> NUMBER
%import common.WS
%ignore WS
"""

PARSER = Lark(GRAMMAR)


def run_command(command, random_state=None):
    parse_tree = PARSER.parse(command)
    tree = parse_tree.children
    cmd = tree[0]

    return run_syntax(cmd, random_state=random_state)


def run_syntax(cmd, random_state=None):
    if random_state is not None:
        random.seed(random_state)

    if cmd.data == 'int':
        args = cmd.children
        return generate_int(args)

    elif cmd.data == 'float':
        args = cmd.children
        return generate_float(args)

    elif cmd.data == 'fraction':
        args = cmd.children
        return generate_fraction(args)

    elif cmd.data == 'prime':
        args = cmd.children
        return roll(generate_prime_list(args))

    else:
        raise Exception('未知指令')


def generate_int(args):
    floor = int(args[0])
    ceil = int(args[1])
    check_interval(floor, ceil)
    return random.randint(floor, ceil)


def generate_float(args):
    floor = int(args[0])
    ceil = int(args[1])

    try:
        acc = int(args[2])
    except IndexError:
        acc = 2

    check_interval(floor, ceil)
    rand_float = random.random() * (ceil - floor) + floor
    return round(rand_float, acc)


def generate_fraction(args):
    numerator = int(args[0])
    denominator = int(args[1])
    return Fraction(numerator, denominator)


def generate_prime_list(args):
    floor = int(args[0])
    ceil = int(args[1])

    if floor < 2:
        floor = 2

    check_interval(floor, ceil)
    prime_list = [i for i in range(floor, ceil+1)]

    for num in prime_list:
        for i in range(2, num):
            if num % i == 0:
                prime_list.remove(num)
                break

    if len(prime_list) == 0:
        raise Exception('{}到{}范围内没有质数'.format(floor, ceil))

    return prime_list


def roll(list_of_number):
    random.shuffle(list_of_number)
    return list_of_number.pop()


def check_interval(floor, ceil):
    if ceil < floor:
        raise Exception('取值范围{}到{}错误'.format(floor, ceil))
