import re

from itertools import product


class OperandSolver:
    def __init__(self,
                 numbers=None,
                 target=None,
                 allow_empty=False,
                 ops=None,
                 use_parenthesis=False):

        if numbers is None or target is None:
            raise Exception('必须指定等式左右两侧')

        if isinstance(numbers, list) and len(numbers) == 1:
            raise Exception('必须由超过一个数组成的列表')

        self.use_parenthesis = use_parenthesis

        if ops is None:
            self.ops = {'+', '-', '*', '/'}
        elif not ops.issubset({'+', '-', '*', '/'}):
            raise Exception('公式符号必须为+-*/中的一部分')
        else:
            self.ops = ops

        if allow_empty is True:
            self.ops.add('')

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
    def _parenthesis_number_validation(expr):
        num_left = re.findall(r'\(', expr)
        num_right = re.findall(r'\)', expr)
        if len(num_left) <= 1 and len(num_right) <= 1:
            return True
        else:
            return False

    @staticmethod
    def _single_number_validation(expr):
        result = re.findall(r'\(\d*?\)', expr)
        if len(result) == 0:
            return True
        else:
            return False

    @staticmethod
    def _parenthesis_validation(expr):
        result_left = re.findall(r'\)\d+?', expr)
        result_right = re.findall(r'\d+?\(', expr)
        if len(result_left) == 0 and len(result_right) == 0:
            return True
        else:
            return False

    @staticmethod
    def _expr_validation(expr):
        paren_num_valid = OperandSolver._parenthesis_number_validation(expr)
        single_num_valid = OperandSolver._single_number_validation(expr)
        paren_valid = OperandSolver._parenthesis_validation(expr)

        if paren_num_valid and single_num_valid and paren_valid:
            return True
        else:
            return False

    @staticmethod
    def _result_validation(exprs, target):
        return (expr for expr in exprs if eval(expr) == target)

    @staticmethod
    def _fix_sign(sign_list):
        fixed_sign_list = sign_list.copy()
        reverse = False
        for i, sign in enumerate(sign_list):
            if sign == '(':
                try:
                    if sign_list[i-1] in {'-', '/'}:
                        reverse = True
                except IndexError:
                    pass
            elif sign == ')':
                reverse = False
            elif reverse is True:
                if sign == '+':
                    fixed_sign_list[i] = '-'
                elif sign == '-':
                    fixed_sign_list[i] = '+'
                elif sign == '*':
                    fixed_sign_list[i] = '/'
                elif sign == '/':
                    fixed_sign_list[i] = '*'
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
    def _solver_wo_parenthesis(formula, ops, target):
        expressions = set()
        num_blanks = len(re.findall(r'{}', formula))
        possible_solutions = product(ops, repeat=num_blanks)

        for solution in possible_solutions:
            expr = formula.format(*solution)
            #  if eval(expr) == target:
                #  expressions.add(expr)
            expressions.add(expr)

        return expressions

    @staticmethod
    def _solver_for_parenthesis(formula, target):
        expressions = set()
        num_blanks = len(re.findall(r'{}', formula))

        possibilities = []

        for i in range(num_blanks - 1):
            for j in range(i + 1, num_blanks):
                possibility = ['' for i in range(num_blanks)]
                possibility[i] = '('
                possibility[j] = ')'
                possibilities.append(possibility)

        for p in possibilities:
            expr = formula.format(*p)
            valid_expr = OperandSolver._expr_validation(expr)

            if valid_expr:
                expr = OperandSolver._sign_fixer(expr)

                if eval(expr) == target:
                    expressions.add(expr)

        return expressions

    def solve(self):
        formula = '{}'.join(self.numbers)
        exprs = OperandSolver._solver_wo_parenthesis(formula,
                                                     self.ops,
                                                     self.target)

        if self.use_parenthesis is False:
            return exprs
        else:
            formulas = OperandSolver._add_curly_brace_to_all(exprs)
            for f in formulas:
                paren = OperandSolver._solver_for_parenthesis(f, self.target)
                exprs = exprs.union(paren)
            return exprs

    def output(self):
        expressions = self.solve()
        print(' | '.join(expressions))
