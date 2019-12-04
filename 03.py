#!/usr/bin/env python

from typing import List, Tuple, Dict


class PositionMatrix:
    x_y: Dict[int, Dict[int, Dict[int, int]]] = {}
    cross_points: List[Tuple[int, int, int]] = []
    node_cur_pos: Dict[int, Tuple[int, int]] = {}
    node_acc_steps: Dict[int, int] = {}
    num_nodes: int = 0

    def __init__(self, num_nodes: int, *args, **kwargs):
        self.num_nodes = num_nodes
        self.node_acc_steps = {n: 0 for n in range(num_nodes)}
        self.node_cur_pos = {n: (0, 0) for n in range(num_nodes)}

    def get_cross_ponts(self) -> List[Tuple[int, int, int]]:
        return self.cross_points

    def visit(self, node_id: int, position: Tuple[int, int]) -> None:
        if node_id < 0 or node_id >= self.num_nodes:
            raise Exception('Bad node id')

        x, y = position

        if x not in self.x_y:
            self.x_y[x] = {}

        if y not in self.x_y[x]:
            self.x_y[x][y] = {n: 0 for n in range(self.num_nodes)}

        already_visited = self.x_y[x][y][node_id] > 0

        self.node_acc_steps[node_id] = self.node_acc_steps.get(node_id, 0) + 1

        if not already_visited:
            self.x_y[x][y][node_id] = self.node_acc_steps[node_id]
            all_visited = all(s > 0 for s in self.x_y[x][y].values())

            if all_visited:
                acc_steps = sum(self.x_y[x][y].values())
                self.cross_points.append((x, y, acc_steps))

    def move(self, node_id: int, direction: str, steps: int) -> None:
        if node_id < 0 or node_id >= self.num_nodes:
            raise Exception('Bad node id')

        cur_x, cur_y = self.node_cur_pos.get(node_id, (0, 0))

        if direction == 'U':
            for y in range(cur_y + 1, cur_y + steps + 1):
                p = (cur_x, y)
                self.visit(node_id, p)

            self.node_cur_pos[node_id] = (cur_x, cur_y + steps)
        elif direction == 'D':
            for y in reversed(range(cur_y - steps, cur_y)):
                p = (cur_x, y)
                self.visit(node_id, p)

            self.node_cur_pos[node_id] = (cur_x, cur_y - steps)
        elif direction == 'R':
            for x in range(cur_x + 1, cur_x + steps + 1):
                p = (x, cur_y)
                self.visit(node_id, p)

            self.node_cur_pos[node_id] = (cur_x + steps, cur_y)
        elif direction == 'L':
            for x in reversed(range(cur_x - steps, cur_x)):
                p = (x, cur_y)
                self.visit(node_id, p)

            self.node_cur_pos[node_id] = (cur_x - steps, cur_y)
        else:
            raise Exception(f'Unknown direction: {direction}')


def get_cross_ponts(cables: List[List[str]]) -> List[Tuple[int, int, int]]:
    p_m = PositionMatrix(num_nodes=len(cables))

    for cable_id, cable_moves in enumerate(cables):
        cur_x = 0
        cur_y = 0

        for move in cable_moves:
            direction = move[0]
            steps = int(move[1:])
            p_m.move(cable_id, direction, steps)

    return p_m.cross_points


def get_manhattan_distances(origin: Tuple[int,int], points: List[Tuple[int, int, int]]) -> List[int]:
    return [abs(origin[0] - p[0]) + abs(origin[1] - p[1]) for p in points]


def part_1(cables: List[List[str]]) -> int:
    cp = get_cross_ponts(cables)
    if not cp:
        return -1

    return min(get_manhattan_distances((0, 0), cp))


def part_2(cables: List[List[str]]) -> int:
    cp = get_cross_ponts(cables)
    if not cp:
        return -1

    return min([p[2] for p in cp])


if __name__ == "__main__":
    cables: List[List[str]] = []
    with open('03.txt', 'r') as file:
        cables = [x.split(',') for x in file.read().splitlines()]

    print(f"Part 1: {part_1(cables)}")
    print(f"Part 2: {part_2(cables)}")
