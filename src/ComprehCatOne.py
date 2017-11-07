from QuestionTemplate import QuestionTemplate


class ComprehCatOne(QuestionTemplate):
    pass


if __name__ == "__main__":
    QUESTION_PARAMS = {
        'name': 'Olympic Math Comprehensive Category One',
        'question_type': 'Filling the blank',
        'question_body': 'body',
        'correct_answer': 2,
        'answer_explanation': 'exp'
    }
    example = ComprehCatOne(QUESTION_PARAMS)
    example.generate()
