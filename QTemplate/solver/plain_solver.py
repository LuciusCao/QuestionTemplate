from QTemplate.solver.solver import Solver


class PlainSolver(Solver):
    def __init__(self, content):
        if not (isinstance(content, str) or all(isinstance(c, str) for c in content)):
            raise Exception('content must be string or iterables with string only')

        Solver.__init__(self, content)
        
    def solve(self):
        try:
            answers = {eval(c) for c in content}
        except:
            answers = set()

        return answers
