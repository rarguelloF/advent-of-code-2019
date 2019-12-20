#!/usr/bin/env python

from itertools import permutations
from typing import List, Tuple, Dict


class IntCodeProgram:
    program: List[str]
    restart: bool
    debug: bool

    _inputs: List[str]
    _pg: List[str]
    _pointer = 0
    _outputs: List[str]

    def __init__(self, program: List[str], restart=True, debug=False):
        self.program = program.copy()
        self._pg = program.copy()
        self._inputs = []
        self.restart = restart
        self.debug = debug

        self.opcodes = {
            '1': self._opcode_1,
            '2': self._opcode_2,
            '3': self._opcode_3,
            '4': self._opcode_4,
            '5': self._opcode_5,
            '6': self._opcode_6,
            '7': self._opcode_7,
            '8': self._opcode_8,
        }

    def __str__(self):
        return f'''
        Program:
        {'  '.join(self._pg)}
        {'  '.join(['*' if i is self._pointer else ' ' * len(x) for i, x in enumerate(self._pg)])}

        Inputs:
        {self._inputs}

        Outputs:
        {self._outputs}
        '''

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
        code_seq = ("0" * (5-len(code_seq))) + code_seq

        return code_seq[:3][::-1][:num_params]

    '''
    Opcode 1 adds together numbers read from two positions and stores
    the result in a third position. The three integers immediately after
    the opcode tell you these three positions.
    '''
    def _opcode_1(self):
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
    def _opcode_2(self):
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
    def _opcode_3(self):
        if not self._inputs:
            raise Exception(f"No remaining inputs")

        _inp = self._inputs.pop(0)

        w_result_pos = int(self._pg[self._pointer+1])
        self._pg[w_result_pos] = _inp
        self._pointer += 2

    '''
    Opcode 4 outputs the value of its only parameter.
    For example, the instruction 4,50 would output the value at address 50.
    '''
    def _opcode_4(self):
        m = self._get_mode_params(1)
        val = self._val_mode(self._pointer+1, m)
        self._outputs.append(val)

        self._pointer += 2

    '''
    Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets
    the instruction pointer to the value from the second parameter.
    Otherwise, it does nothing.
    '''
    def _opcode_5(self):
        m1, m2 = self._get_mode_params(2)
        val1 = self._val_mode(self._pointer+1, m1)
        val2 = self._val_mode(self._pointer+2, m2)

        if int(val1) != 0:
            self._pointer = int(val2)
        else:
            self._pointer += 3

    '''
    Opcode 6 is jump-if-false: if the first parameter is zero, it sets
    the instruction pointer to the value from the second parameter.
    Otherwise, it does nothing.
    '''
    def _opcode_6(self):
        m1, m2 = self._get_mode_params(2)
        val1 = self._val_mode(self._pointer+1, m1)
        val2 = self._val_mode(self._pointer+2, m2)

        if int(val1) == 0:
            self._pointer = int(val2)
        else:
            self._pointer += 3

    '''
    Opcode 7 is less than: if the first parameter is less than the second
    parameter, it stores 1 in the position given by the third parameter.
    Otherwise, it stores 0.
    '''
    def _opcode_7(self):
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
    def _opcode_8(self):
        m1, m2, _m3 = self._get_mode_params(3)
        val1 = self._val_mode(self._pointer+1, m1)
        val2 = self._val_mode(self._pointer+2, m2)
        w_result_pos = int(self._pg[self._pointer+3])

        if int(val1) == int(val2):
            self._pg[w_result_pos] = '1'
        else:
            self._pg[w_result_pos] = '0'

        self._pointer += 4

    def add_inputs(self, *inputs: int) -> None:
        self._inputs += [str(x) for x in inputs]

    def _get_output(self) -> int:
        if not self._outputs:
            return 0
        else:
            return int(self._outputs[-1])

    def output(self) -> Tuple[int, bool]:
        halted = False
        self._outputs = []

        if self.restart:
            self._pointer = 0
            self._pg = self.program.copy()

        if self.debug:
            print(self)
            input("Press enter to continue")

        while self._pointer < len(self._pg):
            code_seq = self._pg[self._pointer]
            if code_seq == "99":
                halted = True
                break

            if code_seq[-1] == '3' and not self._inputs:
                return (self._get_output(), halted)

            try:
                run_opcode = self.opcodes[code_seq[-1]]
            except KeyError:
                raise Exception(
                    f"Unknown operation at position ({self._pointer}): {code_seq}")

            run_opcode()

            if self.debug:
                print(self)
                input("Press enter to continue")

        if not self._outputs:
            return (0, halted)

        return (int(self._outputs[-1]), halted)


def calculate_thruster_signal(pg: IntCodeProgram, phase_settings: List[int]) -> int:
    signal = 0
    for p in phase_settings:
        pg.add_inputs(p, signal)
        signal, _halted = pg.output()

    return signal


def calculate_thruster_signal_feedback_loop(pg: List[str], phase_settings: List[int]) -> int:
    programs = [IntCodeProgram(pg, restart=False) for i in range(5)]
    for p, phase in zip(programs, phase_settings):
        p.add_inputs(phase)

    signal = 0
    halted = False

    while not halted:
        for idx, p in enumerate(programs):
            p.add_inputs(signal)
            signal, h = p.output()

            if h:
                halted = True

    return signal


def part_1(program: List[str]) -> int:
    pg = IntCodeProgram(program=program)

    max_signal = 0
    for phase_settings in permutations([0, 1, 2, 3, 4]):
        signal = calculate_thruster_signal(pg, list(phase_settings))
        if signal > max_signal:
            phase_settings_max = list(phase_settings)
            max_signal = signal

    return max_signal


def part_2(program: List[str]) -> int:
    max_signal = 0
    for phase_settings in permutations([5, 6, 7, 8, 9]):
        signal = calculate_thruster_signal_feedback_loop(pg, list(phase_settings))
        if signal > max_signal:
            phase_settings_max = list(phase_settings)
            max_signal = signal

    return max_signal


if __name__ == "__main__":
    pg: List[str] = []
    with open('07.txt', 'r') as file:
        pg = [x for x in file.read().replace('\n', '').split(',')]

    print(f"Part 1: {part_1(pg)}")
    print(f"Part 2: {part_2(pg)}")
