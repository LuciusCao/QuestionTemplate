from itertools import product


class OperandSolver:
    def __init__(self,
                 formula=None,
                 target=None,
                 allow_empty=False,
                 use_parenthesis=False):

        if formula is None or target is None:
            raise Exception('必须指定等式左右两侧')

        self.operand = ['+', '-']
        if allow_empty is True:
            self.operand.append('')

        self.formula = self._convert_data(formula)
        self.target = target

    @staticmethod
    def _convert_data(data):
        if isinstance(data, int):
            return [str(data)]
        elif isinstance(data, list):
            return [str(e) for e in data]
        else:
            raise Exception('数据必须是整数或者整数的列表')

    def solve(self):
        solutions = []
        formula = '{}'.join(self.formula)
        num_blanks = len(self.formula) - 1
        possible_solutions = product(self.operand, repeat=num_blanks)

        for solution in possible_solutions:
            expression = formula.format(*solution)
            if eval(expression) == self.target:
                solutions.append([s for s in solution])

        #  if self.use_parenthesis is True:
            #  pass  # TODO

        return solutions
