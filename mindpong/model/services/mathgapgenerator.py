from enum import Enum
from random import randint
from math import sqrt, floor

OPERATORS = ['+', '-', '*', '/']
SINGLE_DIGIT_QTY = 4

class MathGapDifficulty(Enum):
    EASY = 'EASY',
    MEDIUM = 'MEDIUM',
    HARD = 'HARD',


class MathGapGenerator():
    """
    Generate two sets of addends that can be multiply together to give a pre-determined random result.
    """

    def generate(self):
        is_operation_valid = False
        while not is_operation_valid:
            operands = [randint(1, 9) for _ in range(SINGLE_DIGIT_QTY)]
            operators = [OPERATORS[randint(0, 3)] for _ in range(SINGLE_DIGIT_QTY - 1)]
            equation = ''
            for i in range(SINGLE_DIGIT_QTY):
                equation += str(operands[i]) + ' ' + operators[i] + ' ' if i != SINGLE_DIGIT_QTY - 1 else str(operands[i])
            is_operation_valid = eval(equation) % 1 != 0
        return equation


if(__name__ == '__main__'):
    mdg = MathGapGenerator()
    for _ in range(0, 100000):
        gen = mdg.generate()
        print('QST:', gen)
        print('ANS: ', eval(gen))
