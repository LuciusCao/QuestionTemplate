class Solver(object):
    def __init__(self, content=None, config=None):
        self.content = content
        self.config = config

    def solve(self):
        return set()

    def output(self):
        answers = self.solve()
        print(' | '.join(answers))
