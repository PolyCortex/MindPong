
from enum import Enum

from mindpong.model.services.mathquestionutils import (
    generate_gap_question,
    generate_drill_question,
    TermNumber, 
    MathQuestionDifficulty)

class MathMode(Enum):
    Drill = 'Drill exercises',
    Gap = 'Fill in the blank'

class MathExercise(object):
    QUESTIONS = {
        MathMode.Drill: "Question: Resolve the following equation",
        MathMode.Gap: "Question: Fill the gap with the the following operators: (+ - x %)"
    }

    def __init__(self, mode=MathMode.Drill, difficulty=MathQuestionDifficulty.EASY, nb_terms=TermNumber.THREE):
        self.mode = mode
        self.difficulty = difficulty
        self.nb_terms = nb_terms
        self.update_question()

    def update_question(self):
        self._complete_question = generate_drill_question(self.difficulty, self.nb_terms)

    def get_question(self):
        return self.QUESTIONS[self.mode]

    def get_equation(self):
        return {
            key: self._complete_question[key] for key in self._complete_question
            if x is not "answer"
        }
    
    def get_answer(self):
       return self._complete_question["answer"]
        