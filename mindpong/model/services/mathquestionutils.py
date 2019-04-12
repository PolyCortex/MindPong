from enum import Enum
from random import randint

OPERATORS = ['+', '-', '*', '/']
OPERANDS_GAP_QTY = 4
MAX_GAP_ANSWER = 99999
MIN_GAP_ANSWER = 0

class MathQuestionDifficulty(Enum):
    EASY = 'Easy'
    MEDIUM = 'Medium'
    HARD = 'Hard'


class TermNumber(Enum):
    TWO = 2
    THREE = 3


def generate_gap_question(difficulty: MathQuestionDifficulty):
    if not isinstance(difficulty, MathQuestionDifficulty):
        raise TypeError('difficulty should be of type MathQuestionDifficulty')
    is_operation_valid = False
    answer = 0
    while not is_operation_valid:
        operands = [str(randint(1, operands_max_number(difficulty)))
                    for _ in range(OPERANDS_GAP_QTY)]
        operators = [OPERATORS[randint(0, 3)]
                        for _ in range(OPERANDS_GAP_QTY - 1)]
        equation = ''
        for i in range(OPERANDS_GAP_QTY):
            equation += str(operands[i]) + ' ' + operators[i] + \
                ' ' if i != OPERANDS_GAP_QTY - 1 else str(operands[i])
        answer = eval(equation)
        is_operation_valid = answer % 1 == 0 and MIN_GAP_ANSWER < answer < MAX_GAP_ANSWER
    return {"operands": operands, "operators": operators, "answer": answer}

def generate_drill_question(difficulty: MathQuestionDifficulty, term_number: TermNumber):
    if not isinstance(difficulty, MathQuestionDifficulty):
        raise TypeError('difficulty should be of type MathQuestionDifficulty')
    if not isinstance(term_number, TermNumber):
        raise TypeError('term_number should be of type TermNumber')
    operator = OPERATORS[randint(0, 3)]
    first_term = randint(
        0, first_term_max_number(difficulty, operator))
    equation = add_suffix_term(difficulty, first_term, operator)
    if term_number == TermNumber.THREE:
        extra_operator = OPERATORS[randint(0, 3)]
        equation = add_suffix_term(
            difficulty, '(' + equation + ')', extra_operator)
    return {"equation": equation, "answer": eval(equation)}

def operands_max_number(difficulty):
    if difficulty == MathQuestionDifficulty.EASY:
        return 9
    elif difficulty == MathQuestionDifficulty.MEDIUM:
        return 99
    elif difficulty == MathQuestionDifficulty.HARD:
        return 999

def add_suffix_term(difficulty: MathQuestionDifficulty, a: int, operator: str):
    is_operation_valid = False
    while(not is_operation_valid):
        min_number = 0 if operator != '/' else 1
        b = randint(min_number, second_term_max_number(
            difficulty, operator))
        is_operation_valid = is_generation_valid(
            operator, eval(str(a)), b)
    return str(a) + ' ' + operator + ' ' + str(b)

def is_generation_valid(operator, a, b):
        if operator == '-':
            return a >= b  # Ensure positive result
        elif operator == '/':
            return (a % b) == 0  # Ensure integer result
        else:
            return True

def first_term_max_number(difficulty: MathQuestionDifficulty, operator):
    if difficulty == MathQuestionDifficulty.EASY:
        return 9
    elif difficulty == MathQuestionDifficulty.MEDIUM:
        return 999 if operator == '+' or operator == '-' else 144
    elif difficulty == MathQuestionDifficulty.HARD:
        return 999

def second_term_max_number(difficulty: MathQuestionDifficulty, operator):
    if difficulty == MathQuestionDifficulty.EASY:
        return 9
    elif difficulty == MathQuestionDifficulty.MEDIUM:
        return 999 if operator == '+' or operator == '-' else 12
    elif difficulty == MathQuestionDifficulty.HARD:
        return 9999 if operator == '+' or operator == '-' else 99
