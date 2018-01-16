import re
from itertools import permutations, product


class MatchGameSolver:
    def __init__(self, question, num_moves, mode):
        self.question = question
        self.num_moves = num_moves
        self.mode = mode
        self.expr = MatchGameSolver._replace_with_curly_brace(self.question)
        self.digits = MatchGameSolver._extract_numbers(self.question)

        # dirty code below, should be cleaned someday
        if mode == '+':

            if num_moves == 1:
                self._cmd = [['add_one']]
            elif num_moves == 2:
                self._cmd = [['add_two'], ['add_one', 'add_one']]
            else:
                raise Exception('数字只允许1和2')

        elif mode == '-':

            if num_moves == 1:
                self._cmd = [['remove_one']]
            elif num_moves == 2:
                self._cmd = [['remove_two'], ['remove_one', 'remove_one']]
            else:
                raise Exception('数字只允许1和2')

        elif mode == 'o':

            if num_moves == 1:
                self._cmd = [['self_one'],
                             ['remove_one', 'add_one'],
                             ['add_one', 'remove_one']]
            elif num_moves == 2:
                self._cmd = [
                    ['self_two'],
                    ['remove_one', 'remove_one', 'add_one', 'add_one'],
                    ['remove_one', 'add_one', 'remove_one', 'add_one'],
                    ['remove_one', 'add_one', 'add_one', 'remove_one'],
                    ['add_one', 'add_one', 'remove_one', 'remove_one'],
                    ['add_one', 'remove_one', 'add_one', 'remove_one'],
                    ['add_one', 'remove_one', 'remove_one', 'add_one'],
                    ['add_two', 'remove_two'],
                    ['remove_two', 'add_two']
                ]
            else:
                raise Exception('数字只允许1和2')

        else:

            raise Exception('模式必须是+-o中的一个')

        self.lookup_table = {
            'add_one': {
                '0': ('8',),
                '1': ('7',),
                '3': ('9',),
                '5': ('6', '9'),
                '6': ('8',),
                '9': ('8', ),
                '-': ('+',)
            },
            'add_two': {
                '1': ('4',),
                '2': ('8',),
                '3': ('8',),
                '4': ('9',),
                '5': ('8',),
                '7': ('3',)
            },
            'remove_one': {
                '6': ('5',),
                '7': ('1',),
                '8': ('0', '6', '9'),
                '9': ('3', '5'),
                '+': ('-',)
            },
            'remove_two': {
                '3': ('7',),
                '4': ('1',),
                '8': ('2', '3', '5'),
                '9': ('4',)
            },
            'self_one': {
                '0': ('6', '9'),
                '2': ('3',),
                '3': ('2', '5'),
                '5': ('3',),
                '6': ('0', '9'),
                '9': ('0', '6')
            },
            'self_two': {
                '2': ('5',),
                '5': ('2',)
            }
        }

    @staticmethod
    def _extract_numbers(question):
        return re.findall(r'[\d\+\-]', question)

    @staticmethod
    def _replace_with_curly_brace(question):
        return re.subn(r'[\d\+\-]', '{}', question)[0]

    @staticmethod
    def _judge_expression(expr):
        splited = expr.split('=')
        left = splited[0]
        right = splited[1]

        if eval(left) == eval(right):
            return True
        else:
            return False

    @staticmethod
    def _get_possibilities(pos_info, temp_store, digits):
        temp = product(*temp_store, repeat=1)
        result = set()
        for i, t in enumerate(temp):
            new_digits = digits.copy()
            for j, each_pos in enumerate(pos_info):
                new_digits[each_pos] = t[j]
            result.add(tuple(new_digits))
        return result

    @staticmethod
    def _solve(lookup_table, expr, digits, cmd):
        solutions = set()

        for each_cmd in cmd:
            num_steps = len(each_cmd)
            num_digits = len(digits)
            move_positions = permutations(range(num_digits), num_steps)
            for position_combo in move_positions:
                temp_store = [[] for i in range(num_steps)]
                pos_info = []
                for i, each_pos in enumerate(position_combo):
                    pos_info.append(each_pos)
                    try:
                        step = each_cmd[i]
                        digit = digits[each_pos]
                        possible_moves = lookup_table[step][digit]
                        for move in possible_moves:
                            temp_store[i].append(move)
                    except KeyError:
                        pass
                possibilities = MatchGameSolver._get_possibilities(pos_info,
                                                                   temp_store,
                                                                   digits)
                for posibility in possibilities:
                    new_expr = expr.format(*posibility)
                    if MatchGameSolver._judge_expression(new_expr):
                        solutions.add(new_expr)

        return solutions

    def solve(self):
        solutions = set()
        solution = MatchGameSolver._solve(self.lookup_table,
                                          self.expr,
                                          self.digits,
                                          self._cmd)
        solutions = solutions.union(solution)
        return solutions

    def output(self):
        solutions = self.solve()
        print(' | '.join(solutions))
