class MatchGameSolver:
    def __init__(self, question, num_moves, mode):
        self.question = question
        self.num_moves = num_moves
        self.mode = mode
        self.lookup_table = {
            'add_one': {
                0: (8,),
                1: (7,),
                3: (9,),
                5: (6, 9),
                6: (8,),
                9: (8, )
            },
            'add_two': {
                1: (4,),
                2: (8,),
                3: (8,),
                4: (9,),
                5: (8,),
                7: (3,)
            },
            'remove_one': {
                6: (5,),
                7: (1,),
                8: (0, 6, 9),
                9: (3, 5)
            },
            'remove_two': {
                3: (7,),
                4: (1,),
                8: (2, 3, 5),
                9: (4,)
            },
            'self_one': {
                0: (6, 9),
                2: (3,),
                3: (2, 5),
                5: (3,),
                6: (0, 9),
                9: (0, 6)
            },
            'self_two': {
                2: (5,),
                5: (2,)
            }
        }
