#!/usr/bin/env python

from typing import List


def calculate_fuel(module: int) -> int:
    return int(module / 3) - 2


def calculate_total_fuel(module: int) -> int:
    total_fuel = 0
    fuel = calculate_fuel(module)

    while fuel > 0:
        total_fuel += fuel
        fuel = calculate_fuel(fuel)

    return total_fuel


def part_1(modules: List[int]) -> int:
    total_fuel = 0
    for m in modules:
        total_fuel += calculate_fuel(m)

    return total_fuel


def part_2(modules: List[int]) -> int:
    total_fuel = 0
    for m in modules:
        total_fuel += calculate_total_fuel(m)

    return total_fuel


if __name__ == "__main__":
    modules: List[int] = []
    with open('01.txt', 'r') as file:
        modules = [int(x) for x in file.read().splitlines()]

    print(f"Part 1: {part_1(modules)}")
    print(f"Part 2: {part_2(modules)}")
