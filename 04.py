#!/usr/bin/env python

from typing import Tuple, Dict


def is_valid_password_1(pw: int) -> bool:
    pw_str = str(pw)

    # It is a six-digit number
    if len(pw_str) != 6:
        return False

    adj_found = False
    for i in range(len(pw_str)-1):
        cur, nxt = pw_str[i:i+2]

        # Going from left to right, the digits never decrease
        if cur > nxt:
            return False

        # Two adjacent digits are the same (like 22 in 122345)
        if cur == nxt:
            adj_found = True

    if not adj_found:
        return False

    return True


def is_valid_password_2(pw: int) -> bool:
    pw_str = str(pw)

    if len(pw_str) != 6:
        return False

    adj_count: Dict[str, int] = {}
    for i in range(len(pw_str)-1):
        cur, nxt = pw_str[i:i+2]

        if cur > nxt:
            return False

        if cur == nxt:
            adj_count[cur] = adj_count.get(cur, 1) + 1

    if 2 not in adj_count.values():
        return False

    return True


def part_1(start: int, end: int) -> int:
    return len([x for x in range(start, end + 1) if is_valid_password_1(x)])


def part_2(start: int, end: int) -> int:
    return len([x for x in range(start, end + 1) if is_valid_password_2(x)])


if __name__ == "__main__":
    print(f"Part 1: {part_1(172930, 683082)}")
    print(f"Part 2: {part_2(172930, 683082)}")
