#!/usr/bin/env python

from typing import List


def parse_program(program: List[int]) -> List[int]:
    pg_cpy = program.copy()

    i = 0
    while i < len(pg_cpy):
        code = pg_cpy[i]

        if code == 99:
            return pg_cpy
        elif code == 1:
            a = pg_cpy[i+1]
            b = pg_cpy[i+2]
            r = pg_cpy[i+3]
            pg_cpy[r] = pg_cpy[a]+pg_cpy[b]
            i+=4
        elif code == 2:
            a = pg_cpy[i+1]
            b = pg_cpy[i+2]
            r = pg_cpy[i+3]
            pg_cpy[r] = pg_cpy[a]*pg_cpy[b]
            i+=4
        else:
            raise Exception(f"Unknown code at position ({i}): {code}")

    return pg_cpy


def pg_result(pg: List[int], noun: int, verb: int) -> int:
    pg_cpy = pg.copy()
    pg_cpy[1] = noun
    pg_cpy[2] = verb
    return parse_program(pg_cpy)[0]


def part_1(pg: List[int]) -> int:
    return pg_result(pg, 12, 2)


def part_2(pg: List[int], expected_result: int) -> int:
    for noun in range(0, 100):
        for verb in range(0, 100):
            if pg_result(pg, noun, verb) == expected_result:
                return 100 * noun + verb

    raise Exception(f"Didn't found noun and verb for expected_result: {expected_result}")


if __name__ == "__main__":
    pg: List[int] = []
    with open('02.txt', 'r') as file:
        pg = [int(x) for x in file.read().split(',')]

    print(f"Part 1: {part_1(pg)}")
    print(f"Part 2: {part_2(pg, 19690720)}")
