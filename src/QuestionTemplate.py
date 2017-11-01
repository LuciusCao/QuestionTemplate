class QuestionTemplate:
    def __init__(self, name):
        self.name = name

    def generate(self):
        print("success {}".format(self.name))

