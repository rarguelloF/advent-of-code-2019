#!/usr/bin/env python

from typing import List


class IntCodeProgram:
    program: List[str]

    _pg_input: str
    _pg: List[str]
    _pointer = 0
    _outputs: List[str] = []

    def __init__(self, program: List[str]):
        self.program = program.copy()
        self.opcodes = {
            '1': self.opcode_1,
            '2': self.opcode_2,
            '3': self.opcode_3,
            '4': self.opcode_4,
            '5': self.opcode_5,
            '6': self.opcode_6,
            '7': self.opcode_7,
            '8': self.opcode_8,
        }

    def _val_mode(self, pos: int, mode: str) -> str:
        val = self._pg[pos]
        if mode == "0":
            return self._pg[int(val)]
        elif mode == "1":
            return val
        else:
            raise Exception(f"Unknown mode: {mode}")

    def _get_mode_params(self, num_params: int) -> str:
        code_seq = self._pg[self._pointer]
        code_seq = ("0" * (num_params+2-len(code_seq))) + code_seq
        return code_seq[:num_params][::-1]

    def parse(self, pg_input: str) -> List[str]:
        self._pg_input = pg_input
        self._pointer = 0
        self._outputs = []
        self._pg = self.program.copy()

        while self._pointer < len(self._pg):
            code_seq = self._pg[self._pointer]
            if code_seq == "99":
                break

            try:
                run_opcode = self.opcodes[code_seq[-1]]
            except KeyError:
                raise Exception(f"Unknown operation at position ({self._pointer}): {code_seq}")

            run_opcode()

        return self._outputs

    '''
    Opcode 1 adds together numbers read from two positions and stores
    the result in a third position. The three integers immediately after
    the opcode tell you these three positions.
    '''
    def opcode_1(self):
        m1, m2, _m3 = self._get_mode_params(3)
        val1 = self._val_mode(self._pointer+1, m1)
        val2 = self._val_mode(self._pointer+2, m2)
        w_result_pos = int(self._pg[self._pointer+3])

        self._pg[w_result_pos] = str(int(val1)+int(val2))
        self._pointer += 4

    '''
    Opcode 2 multiplies together numbers read from two positions and stores
    the result in a third position. The three integers immediately after
    the opcode tell you these three positions.
    '''
    def opcode_2(self):
        m1, m2, _m3 = self._get_mode_params(3)
        val1 = self._val_mode(self._pointer+1, m1)
        val2 = self._val_mode(self._pointer+2, m2)
        w_result_pos = int(self._pg[self._pointer+3])

        self._pg[w_result_pos] = str(int(val1)*int(val2))
        self._pointer += 4

    '''
    Opcode 3 takes a single integer as input and saves it to the position
    given by its only parameter. For example, the instruction 3,50 would
    take an input value and store it at address 50.
    '''
    def opcode_3(self):
        w_result_pos = int(self._pg[self._pointer+1])
        self._pg[w_result_pos] = self._pg_input
        self._pointer += 2

    '''
    Opcode 4 outputs the value of its only parameter.
    For example, the instruction 4,50 would output the value at address 50.
    '''
    def opcode_4(self):
        m = self._get_mode_params(1)
        val = self._val_mode(self._pointer+1, m)

        self._outputs.append(val)
        self._pointer += 2

    '''
    Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets
    the instruction pointer to the value from the second parameter.
    Otherwise, it does nothing.
    '''
    def opcode_5(self):
        m1, m2 = self._get_mode_params(2)
        val1 = self._val_mode(self._pointer+1, m1)
        val2 = self._val_mode(self._pointer+2, m2)

        if val1 is not '0':
            self._pointer = int(val2)
        else:
            self._pointer += 3

    '''
    Opcode 6 is jump-if-false: if the first parameter is zero, it sets
    the instruction pointer to the value from the second parameter.
    Otherwise, it does nothing.
    '''
    def opcode_6(self):
        m1, m2 = self._get_mode_params(2)
        val1 = self._val_mode(self._pointer+1, m1)
        val2 = self._val_mode(self._pointer+2, m2)

        if val1 is '0':
            self._pointer = int(val2)
        else:
            self._pointer += 3

    '''
    Opcode 7 is less than: if the first parameter is less than the second
    parameter, it stores 1 in the position given by the third parameter.
    Otherwise, it stores 0.
    '''
    def opcode_7(self):
        m1, m2, _m3 = self._get_mode_params(3)
        val1 = self._val_mode(self._pointer+1, m1)
        val2 = self._val_mode(self._pointer+2, m2)
        w_result_pos = int(self._pg[self._pointer+3])

        if int(val1) < int(val2):
            self._pg[w_result_pos] = '1'
        else:
            self._pg[w_result_pos] = '0'

        self._pointer += 4

    '''
    Opcode 8 is equals: if the first parameter is equal to the second parameter,
    it stores 1 in the position given by the third parameter.
    Otherwise, it stores 0.
    '''
    def opcode_8(self):
        m1, m2, _m3 = self._get_mode_params(3)
        val1 = self._val_mode(self._pointer+1, m1)
        val2 = self._val_mode(self._pointer+2, m2)
        w_result_pos = int(self._pg[self._pointer+3])

        if int(val1) == int(val2):
            self._pg[w_result_pos] = '1'
        else:
            self._pg[w_result_pos] = '0'

        self._pointer += 4


def part_1(program: List[str]) -> str:
    pg = IntCodeProgram(program=program)
    o = pg.parse('1')
    return o[-1]


def part_2(program: List[str]) -> str:
    pg = IntCodeProgram(program=program)
    o = pg.parse('5')
    return o[-1]


if __name__ == "__main__":
    pg: List[str] = []
    with open('05.txt', 'r') as file:
        pg = [x for x in file.read().replace('\n', '').split(',')]

    print(f"Part 1: {part_1(pg)}")
    print(f"Part 2: {part_2(pg)}")
