import re

from itertools import product


class OperandSolver:
    def __init__(self,
                 numbers=None,
                 target=None,
                 allow_empty=False,
                 use_parenthesis=False):

        if numbers is None or target is None:
            raise Exception('必须指定等式左右两侧')

        if isinstance(numbers, list) and len(numbers) == 1:
            raise Exception('必须由超过一个数组成的列表')

        self.use_parenthesis = use_parenthesis

        self.operands = {'+', '-'}
        if allow_empty is True:
            self.operands.add('')

        self.numbers = self._convert_data(numbers)
        self.target = target

    @staticmethod
    def _convert_data(data):
        if isinstance(data, list):
            return [str(e) for e in data]
        else:
            raise Exception('数据必须是整数的列表')

    @staticmethod
    def _add_curly_brace_to_one(expression):
        template_formula = re.subn(r'\d+', '{}', expression)[0]
        numbers = re.findall(r'\d+', expression)
        numbers_with_curly_brace = ['{}' + n + '{}' for n in numbers]
        return template_formula.format(*numbers_with_curly_brace)

    @staticmethod
    def _add_curly_brace_to_all(expressions):
        return [OperandSolver._add_curly_brace_to_one(e) for e in expressions]

    @staticmethod
    def _expr_validation(expr):
        result = re.findall(r'\(\d{0,1}\)', expr)
        if len(result) == 0:
            return True
        else:
            return False

    @staticmethod
    def _solver(formula, ops, target):
        expressions = set()
        num_blanks = len(re.findall(r'{}', formula))
        possible_solutions = product(ops, repeat=num_blanks)

        for solution in possible_solutions:
            expr = formula.format(*solution)
            try:
                if eval(expr) == target:
                    if OperandSolver._expr_validation(expr):
                        expressions.add(expr)
            except Exception:
                pass

        return expressions

    def solve(self):
        formula = '{}'.join(self.numbers)
        expressions = OperandSolver._solver(formula, self.operands, self.target)

        if self.use_parenthesis is False:
            return expressions
        else:
            formulas = OperandSolver._add_curly_brace_to_all(expressions)
            for f in formulas:
                ops = {'(', ')', ''}
                expressions = OperandSolver._solver(f, ops, self.target)
            return expressions
