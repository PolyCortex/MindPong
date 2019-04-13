
from enum import Enum

from mindpong.model.services.mathquestionutils import (
    generate_gap_question,
    generate_drill_question,
    TermNumber, 
    MathQuestionDifficulty)

class MathMode(Enum):
    Drill = "Drill exercises"
    Gap = "Fill in the blank"

class MathExercise(object):
    QUESTIONS = {
        MathMode.Drill: "Question: Resolve the following equation",
        MathMode.Gap: "Question: Fill the gap with the the following operators: (+ - x %)"
    }

    def __init__(self, mode=MathMode.Drill, difficulty=MathQuestionDifficulty.EASY, nb_terms=TermNumber.THREE):
        self.mode = mode
        self.difficulty = difficulty
        self.nb_terms = nb_terms
        self.has_shown_answer = False
        self.update_question()

    def update_question(self):
        if self.mode is MathMode.Drill:
            self._complete_question = generate_drill_question(self.difficulty, self.nb_terms)
        else:
            self._complete_question = generate_gap_question(self.difficulty)

    def get_question(self):
        return self.QUESTIONS[self.mode]

    def get_equation(self):
        if self.mode is MathMode.Drill:
            return self._complete_question['equation'] + " = _"
        else:
            operands = " _ ".join(self._complete_question['operands'])
            return "%s = %i"%(operands, self._complete_question['answer'])
    
    def get_answer(self):
        result = ""

        if self.mode is MathMode.Drill:
            result = self.get_equation()[:-1] + " " + str(int(self._complete_question["answer"]))
        else:
            for i in range(len(self._complete_question['operands']) - 1):
                result += self._complete_question['operands'][i] + " "
                result += self._complete_question['operators'][i] + " "

            result += self._complete_question['operands'][-1]
            result = "%s = %i"%(result, self._complete_question["answer"])
        
        return result
        