from enum import Enum

from random import randint

OPERATORS = ['+', '-', '*', '/']


class MathDrillDifficulty(Enum):
    EASY = 'EASY',
    MEDIUM = 'MEDIUM',
    HARD = 'HARD',

class TermNumber(Enum):
    TWO = 2,
    THREE = 3


class MathDrillGeneratorService():
    def generate(self, difficulty: MathDrillDifficulty, term_number: TermNumber):
        operator = OPERATORS[randint(0, 3)]
        first_term = randint(0, self._first_term_max_number(difficulty, operator))
        equation = self._add_suffix_term(difficulty, first_term, operator)
        if term_number == TermNumber.THREE:
            extra_operator = OPERATORS[randint(0, 3)]
            return self._add_suffix_term(difficulty, '(' + equation + ')', extra_operator)
        return equation

    def _add_suffix_term(self, difficulty: MathDrillDifficulty, a, operator):
        is_operation_valid = False
        while(not is_operation_valid):
            min_number = 0 if operator != '/' else 1
            b = randint(min_number, self._second_term_max_number(difficulty, operator))
            is_operation_valid = self._is_generation_valid(operator, eval(str(a)), b)
        return str(a) + ' ' + operator + ' ' + str(b)

    def _is_generation_valid(self, operator, a, b):
            if operator == '-':
                return a >= b # Ensure positive result
            elif operator == '/':
                return (a % b) == 0 # Ensure integer result
            else:
                return True

    def _first_term_max_number(self, difficulty: MathDrillDifficulty, operator):
        if difficulty == MathDrillDifficulty.EASY:
            return 9
        elif difficulty == MathDrillDifficulty.MEDIUM:
            return 999 if operator == '+' or operator == '-' else 144
        elif difficulty == MathDrillDifficulty.HARD:
            return 999
        elif difficulty == MathDrillDifficulty.VERY_HARD:
            return 999

    def _second_term_max_number(self, difficulty: MathDrillDifficulty, operator):
        if difficulty == MathDrillDifficulty.EASY:
            return 9
        elif difficulty == MathDrillDifficulty.MEDIUM:
            return 999 if operator == '+' or operator == '-' else 12
        elif difficulty == MathDrillDifficulty.HARD:
            return 9999 if operator == '+' or operator == '-' else 99


if(__name__ == '__main__'):
    mdg = MathDrillGeneratorService()
    i = 100
    while i>0:
        generation = mdg.generate(MathDrillDifficulty.EASY, TermNumber.THREE)
        i-= 1
        print('QST:', generation)
        print('ANS: ', eval(generation))
