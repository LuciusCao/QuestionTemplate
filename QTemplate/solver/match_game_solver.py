import re


class MatchGameSolver:
    def __init__(self, question, num_moves, mode):
        self.question = question
        self.num_moves = num_moves
        self.mode = mode

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
    def _extract_numbers_from_question(question):
        return re.findall(r'[\d\+\-]', question)

    @staticmethod
    def _replace_with_curly_brace(question):
        return re.subn(r'[\d\+\-]', '{}', question)[0]

    @staticmethod
    def _get_question_and_key(question):
        return question.split('=')

    def _solve_for_add_one(self, question):
        expr = MatchGameSolver._replace_with_curly_brace(question)
        digit_list = MatchGameSolver._extract_numbers_from_question(question)
        solutions = set()
        length = len(digit_list)

        for i in range(length):
            digit = digit_list[i]
            try:
                possible_moves = self.lookup_table['add_one'][digit]
            except KeyError:
                break

            for move in possible_moves:
                new_digit_list = digit_list.copy()
                new_digit_list[i] = move
                new_expr = expr.format(*new_digit_list)

            splited = MatchGameSolver._get_question_and_key(new_expr)
            left = splited[0]
            right = splited[1]
            if eval(left) == eval(right):
                solutions.add(expr)

        return solutions

    def solve(self):
        if self.mode == '+' and self.num_moves == 1:
            solutions = self._solve_for_add_one(self.question)
        return solutions

    def output(self):
        solutions = self.solve()
        print(' | '.join(solutions))
