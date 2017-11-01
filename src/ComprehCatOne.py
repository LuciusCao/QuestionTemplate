from QuestionTemplate import QuestionTemplate


class ComprehCatOne(QuestionTemplate):
    def __init__(self, name):
        QuestionTemplate.__init__(self, name)


if __name__ == "__main__":
    example = ComprehCatOne("this is name")
    example.generate()
