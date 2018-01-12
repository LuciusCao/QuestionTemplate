import re


class MatchGameSolver:
    def __init__(self, question, num_moves, mode):
        self.question = question
        self.num_moves = num_moves
        self.mode = mode

        if mode == '+':

            if num_moves == 1:
                self._cmd = 'add_one'
            elif num_moves == 2:
                self._cmd == 'add_two'
            else:
                raise Exception('数字只允许1和2')

        elif mode == '-':

            if num_moves == 1:
                self._cmd = 'remove_one'
            elif num_moves == 2:
                self._cmd = 'remove_two'
            else:
                raise Exception('数字只允许1和2')

        elif mode == 'o':

            if num_moves == 1:
                self._cmd = 'self_one'
            elif num_moves == 2:
                self._cmd = 'self_two'
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
    def _get_question_and_key(question):
        return question.split('=')

    @staticmethod
    def _judge_expression(expr):
        splited = MatchGameSolver._get_question_and_key(expr)
        left = splited[0]
        right = splited[1]

        if eval(left) == eval(right):
            return True
        else:
            return False

    def _solve_for_add_one(self, expr, digit_list, cmd):
        solutions = set()
        length = len(digit_list)

        for i in range(length):
            digit = digit_list[i]
            try:
                possible_moves = self.lookup_table[cmd][digit]
                for move in possible_moves:
                    new_digit_list = digit_list.copy()
                    new_digit_list[i] = move
                    new_expr = expr.format(*new_digit_list)
                    if MatchGameSolver._judge_expression(new_expr):
                        solutions.add(new_expr)
            except KeyError:
                pass

        return solutions

    def solve(self):
        expr = MatchGameSolver._replace_with_curly_brace(self.question)
        digit_list = MatchGameSolver._extract_numbers(self.question)
        if self.mode == '+' and self.num_moves == 1:
            solutions = self._solve_for_add_one(expr, digit_list, self._cmd)
        return solutions

    def output(self):
        solutions = self.solve()
        print(' | '.join(solutions))
