import re


from itertools import product
from QTemplate.solver.solver import Solver


class OperandSolver(Solver):
    '''
    Description:
        Operand solver for Olympic math problems, supported operands: + - * /.
        Given numbers and target, test takers are required to find the proper
        combination of operands that makes the equation holds
        numbers: list of int
        target: int
        allow_empty: boolean, if True, [1,1] can be considered as 11, in fact,
        an empty string '' will be added to self.ops
        ops: set of operands, specify a subset for certain type of questions
        use_parenthesis: boolean, if True, the answer will include ONLY ONE
        pair of parenthesis

    Usage:
        solver = OperandSolver(numbers=[1,1], target=2)
        solver.solve()

    Documentation:
        |> add {} to numbers, [1, 2, 3] -> 1{}2{}3
        |> enumerate all possible combinations
        |> based on each combination in possible expression add {} to
           expression, 1+2+3 -> {}1{}+{}2{}+{}3{}
        |> enumerate all possible combinations of parenthesis. skipped if
           use_parenthesis is False
        |> check validation of expressions
        |> fix sign of all expressions
        |> use expressions that make the equation hold
    '''
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
    def _division_by_zero_validation(expr):
        try:
            eval(expr)
        except ZeroDivisionError:
            return False
        except Exception:
            return False
        else:
            return True

    @staticmethod
    def _expr_validation(expr):
        paren_num_valid = OperandSolver._parenthesis_number_validation(expr)
        single_num_valid = OperandSolver._single_number_validation(expr)
        paren_valid = OperandSolver._parenthesis_validation(expr)
        calc_valid = OperandSolver._division_by_zero_validation(expr)

        expr_valid = paren_num_valid and single_num_valid and paren_valid

        if expr_valid and calc_valid:
            return True
        else:
            return False

    @staticmethod
    def _result_validation(exprs, target):
        return {expr for expr in exprs if eval(expr) == target}

    @staticmethod
    def _fix_sign(sign_list):
        fixed_sign_list = sign_list.copy()
        reverse = {'add_sub': False, 'mul_div': False}

        for i, sign in enumerate(sign_list):
            cur_sign = sign

            if i == 0:
                prev_sign = ''
            else:
                prev_sign = sign_list[i-1]

            if sign == '(':
                if prev_sign == '-':
                    reverse['add_sub'] = True
                elif prev_sign == '/':
                    reverse['mul_div'] = True
            elif sign == ')':
                reverse['add_sub'] = False
                reverse['mul_div'] = False
            elif reverse['add_sub'] == True:
                if cur_sign == '-':
                    fixed_sign_list[i] = '+'
                elif cur_sign == '+':
                    fixed_sign_list[i] = '-'
            elif reverse['mul_div'] == True:
                if cur_sign == '*':
                    fixed_sign_list[i] = '/'
                elif cur_sign == '/':
                    fixed_sign_list[i] = '*'

        return fixed_sign_list

    @staticmethod
    def _sign_fixer(expr):
        sign_list = re.findall(r'\D+?', expr)
        expr_wo_symbol = re.subn(r'\D+?', '{}', expr)[0]
        fixed_sign_list = OperandSolver._fix_sign(sign_list)
        return expr_wo_symbol.format(*fixed_sign_list)

    @staticmethod
    def _filler_wo_parenthesis(formula, ops):
        expressions = set()
        num_blanks = len(re.findall(r'{}', formula))
        possible_solutions = product(ops, repeat=num_blanks)

        for solution in possible_solutions:
            expr = formula.format(*solution)
            expressions.add(expr)

        return expressions

    @staticmethod
    def _filler_for_parenthesis(formula):
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
                expressions.add(expr)

        return expressions

    def solve(self):
        formula = '{}'.join(self.numbers)
        exprs = OperandSolver._filler_wo_parenthesis(formula, self.ops)

        if self.use_parenthesis is False:
            exprs = exprs
        else:
            formulas = OperandSolver._add_curly_brace_to_all(exprs)
            for f in formulas:
                paren = OperandSolver._filler_for_parenthesis(f)
                exprs = exprs.union(paren)
        return OperandSolver._result_validation(exprs, self.target)
