class QuestionTemplate:
    '''A question template class that helps generate questions'''
    import random

    def __init__(self, question_params, random_state=None):
        self.name = question_params['name']
        self.question_type = question_params['question_type']
        self.question_body = question_params['question_body']
        self.correct_answer = question_params['correct_answer']
        self.answer_explanation = question_params['answer_explanation']

        if random_state is not None:
            self.random.seed(random_state)

        if self.question_type == 'Multiple Choices':
            self.choices = question_params['choices']
        else:
            self.choices = None

    def show_meta(self):
        '''show meta information about the question'''
        print('name: {}'.format(self.name))
        print('question type: {}'.format(self.question_type))

    def generate(self):
        '''generate a valid question via this template'''
        print('Question Generated')
        print('name: {}'.format(self.name))
        print('question type: {}'.format(self.question_type))
        print('question body: {}'.format(self.question_body))
        print('correct_answer: {}'.format(self.correct_answer))
        print('answer_explanation {}'.format(self.answer_explanation))
        if self.question_type == 'Multiple Choices':
            print('choices: {}'.format(self.choices))

