import re

from itertools import product


class OperandSolver:
    def __init__(self,
                 formula=None,
                 target=None,
                 allow_empty=False,
                 use_parenthesis=False):

        if formula is None or target is None:
            raise Exception('必须指定等式左右两侧')

        if isinstance(formula, list) and len(formula) == 1:
            raise Exception('必须由超过一个数组成的列表')

        self.use_parenthesis = use_parenthesis

        self.operands = {'+', '-'}
        if allow_empty is True:
            self.operands.add('')

        self.formula = self._convert_data(formula)
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

    def solve(self):
        expressions = set()
        formula = '{}'.join(self.formula)
        num_blanks = len(self.formula) - 1
        possible_solutions = product(self.operands, repeat=num_blanks)

        for solution in possible_solutions:
            expr = formula.format(*solution)
            if eval(expr) == self.target:
                expressions.add(expr)

        if self.use_parenthesis is False:
            return expressions
        else:
            formulas = OperandSolver._add_curly_brace_to_all(expressions)
            expressions = set()
            for f in formulas:
                ops = {'(', ')', ''}
                num_blanks = len(re.findall(r'{}', f))
                possible_solutions = product(ops, repeat=num_blanks)

                for solution in possible_solutions:
                    expr = f.format(*solution)
                    try:
                        if eval(expr) == self.target:
                            if OperandSolver._expr_validation(expr):
                                expressions.add(expr)
                    except Exception:
                        pass

            return expressions

