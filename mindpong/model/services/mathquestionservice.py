from enum import Enum
from random import randint

OPERATORS = ['+', '-', '*', '/']
OPERANDS_GAP_QTY = 4


class MathQuestionDifficulty(Enum):
    EASY = 'EASY',
    MEDIUM = 'MEDIUM',
    HARD = 'HARD',


class TermNumber(Enum):
    TWO = 2,
    THREE = 3


class MathQuestionService():
    def generate_gap_question(self, difficulty: MathQuestionDifficulty):
        if not isinstance(difficulty, MathQuestionDifficulty):
            raise TypeError('difficulty should be of type MathQuestionDifficulty')
        is_operation_valid = False
        answer = 0
        while not is_operation_valid:
            operands = [randint(1, self._operands_max_number(difficulty))
                        for _ in range(OPERANDS_GAP_QTY)]
            operators = [OPERATORS[randint(0, 3)]
                         for _ in range(OPERANDS_GAP_QTY - 1)]
            equation = ''
            for i in range(OPERANDS_GAP_QTY):
                equation += str(operands[i]) + ' ' + operators[i] + \
                    ' ' if i != OPERANDS_GAP_QTY - 1 else str(operands[i])
            answer = eval(equation)
            is_operation_valid = answer % 1 == 0
        return {"operands": operands, "operators": operators, "answer": answer}

    def generate_drill_question(self, difficulty: MathQuestionDifficulty, term_number: TermNumber):
        if not isinstance(difficulty, MathQuestionDifficulty):
            raise TypeError('difficulty should be of type MathQuestionDifficulty')
        if not isinstance(term_number, TermNumber):
            raise TypeError('term_number should be of type TermNumber')
        operator = OPERATORS[randint(0, 3)]
        first_term = randint(
            0, self._first_term_max_number(difficulty, operator))
        equation = self._add_suffix_term(difficulty, first_term, operator)
        if term_number == TermNumber.THREE:
            extra_operator = OPERATORS[randint(0, 3)]
            equation = self._add_suffix_term(
                difficulty, '(' + equation + ')', extra_operator)
        return {"equation": equation, "answer": eval(equation)}

    def _operands_max_number(self, difficulty):
        if difficulty == MathQuestionDifficulty.EASY:
            return 9
        elif difficulty == MathQuestionDifficulty.MEDIUM:
            return 99
        elif difficulty == MathQuestionDifficulty.HARD:
            return 999

    def _add_suffix_term(self, difficulty: MathQuestionDifficulty, a: int, operator: str):
        is_operation_valid = False
        while(not is_operation_valid):
            min_number = 0 if operator != '/' else 1
            b = randint(min_number, self._second_term_max_number(
                difficulty, operator))
            is_operation_valid = self._is_generation_valid(
                operator, eval(str(a)), b)
        return str(a) + ' ' + operator + ' ' + str(b)

    def _is_generation_valid(self, operator, a, b):
            if operator == '-':
                return a >= b  # Ensure positive result
            elif operator == '/':
                return (a % b) == 0  # Ensure integer result
            else:
                return True

    def _first_term_max_number(self, difficulty: MathQuestionDifficulty, operator):
        if difficulty == MathQuestionDifficulty.EASY:
            return 9
        elif difficulty == MathQuestionDifficulty.MEDIUM:
            return 999 if operator == '+' or operator == '-' else 144
        elif difficulty == MathQuestionDifficulty.HARD:
            return 999

    def _second_term_max_number(self, difficulty: MathQuestionDifficulty, operator):
        if difficulty == MathQuestionDifficulty.EASY:
            return 9
        elif difficulty == MathQuestionDifficulty.MEDIUM:
            return 999 if operator == '+' or operator == '-' else 12
        elif difficulty == MathQuestionDifficulty.HARD:
            return 9999 if operator == '+' or operator == '-' else 99
