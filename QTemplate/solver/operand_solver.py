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
        result = re.findall(r'\(\d*?\)', expr)
        if len(result) == 0:
            return True
        else:
            return False

    @staticmethod
    def _fix_sign(sign_list):
        fixed_sign_list = sign_list.copy()
        l = len(sign_list)
        reverse = False
        for i in range(l):
            if sign_list[i] == '(':
                try:
                    if sign_list[i-1] == '-':
                        reverse = True
                except IndexError:
                    pass
            elif sign_list[i] == ')':
                reverse = False
            elif reverse is True:
                if sign_list[i] == '+':
                    fixed_sign_list[i] = '-'
                elif sign_list[i] == '-':
                    fixed_sign_list[i] = '+'
                else:
                    raise Exception('奇怪的异常！')
        return fixed_sign_list

    @staticmethod
    def _sign_fixer(expr):
        sign_list = re.findall(r'\D+?', expr)
        expr_wo_symbol = re.subn(r'\D+?', '{}', expr)[0]
        fixed_sign_list = OperandSolver._fix_sign(sign_list)
        return expr_wo_symbol.format(*fixed_sign_list)

    @staticmethod
    def _solver(formula, ops, target):
        expressions = set()
        num_blanks = len(re.findall(r'{}', formula))
        possible_solutions = product(ops, repeat=num_blanks)

        for solution in possible_solutions:
            expr = formula.format(*solution)
            expr = OperandSolver._sign_fixer(expr)

            try:
                if eval(expr) == target:
                    if OperandSolver._expr_validation(expr):
                        expressions.add(expr)
            except Exception:
                pass

        return expressions

    def solve(self):
        formula = '{}'.join(self.numbers)
        exprs = OperandSolver._solver(formula, self.operands, self.target)

        if self.use_parenthesis is False:
            return exprs
        else:
            formulas = OperandSolver._add_curly_brace_to_all(exprs)
            for f in formulas:
                ops = {'(', ')', ''}
                exprs = OperandSolver._solver(f, ops, self.target)
            return exprs

    def output(self):
        expressions = self.solve()
        print(' | '.join(expressions))
