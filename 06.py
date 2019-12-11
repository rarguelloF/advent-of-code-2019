#!/usr/bin/env python

from typing import List, Dict, Set


class OrbitMap:
    _map: Dict[str, str] = {}

    def __init__(self, orbits: List[str]):
        for o in orbits:
            a, b = o.split(')')
            self._map[b] = a

    def num_orbits(self, elem: str) -> int:
        if elem not in self._map:
            return 0

        return 1 + self.num_orbits(self._map[elem])

    def path_to_center(self, elem: str, path: List[str] = []) -> List[str]:
        if elem not in self._map:
            return path

        return self.path_to_center(self._map[elem], path + [elem])

    def elems(self) -> List[str]:
        return list(self._map.keys())


def part_1(orbits: List[str]) -> int:
    o_map = OrbitMap(orbits)
    total = 0

    for elem in o_map.elems():
        total += o_map.num_orbits(elem)

    return total


def part_2(orbits: List[str]) -> int:
    o_map = OrbitMap(orbits)

    you_path = o_map.path_to_center('YOU')
    santa_path = o_map.path_to_center('SAN')

    for y_e, s_e in zip(you_path[::-1], santa_path[::-1]):
        if y_e == s_e:
            common_node = y_e
        else:
            break

    return you_path.index(common_node) + santa_path.index(common_node) - 2


if __name__ == '__main__':
    orbits: List[str] = []
    with open('06.txt', 'r') as file:
        orbits = [x for x in file.read().split('\n')][:-1]

    print(f'Part 1: {part_1(orbits)}')
    print(f'Part 2: {part_2(orbits)}')
