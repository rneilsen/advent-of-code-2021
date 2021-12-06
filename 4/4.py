from functools import reduce
from itertools import product

import sys

print(sys.version)

BOARD_SIZE = 5

class Board:
    def __init__(self, rows: list[str]):
        self.rows = [list(filter(None, row.split())) for row in rows]
        self.marked = [[False for _ in row] for row in self.rows]
        self.ended = False


    def check_win(self) -> bool:
        """Returns True if this board is in a win state, False otherwise"""
        for i in range(BOARD_SIZE):
            row = self.marked[i]
            col = [self.marked[j][i] for j in range(BOARD_SIZE)]
            fold_and = lambda x, y: x and y
            if reduce(fold_and, row) or reduce(fold_and, col):
                self.ended = True
        return self.ended


    def play(self, number: int) -> bool:
        if self.ended:
            return False
        """Marks a square if available. Returns True if this draw caused the board to win."""
        for i in range(BOARD_SIZE):
            try:
                self.marked[i][self.rows[i].index(number)] = True
                return self.check_win()
            except ValueError:
                pass
        return False


    def sum_unmarked(self) -> int:
        """Returns the sum of all unmarked values on the board"""
        return sum([int(self.rows[i][j]) for i, j in product(range(BOARD_SIZE), repeat=2) if not self.marked[i][j]])
        
    
    def __repr__(self):
        str_rows = []
        for i in range(BOARD_SIZE):
            str_rows.append(' '.join([
                        ('[' if self.marked[i][j] else ' ') + \
                        f'{self.rows[i][j]:>2}' + 
                        (']' if self.marked[i][j] else ' ')
                    for j in range(BOARD_SIZE)]))
        return '\n'.join(str_rows)



with open('input') as f:
    draws = f.readline().strip().split(',')
    f.readline()    # scrap blank line after the list of draws

    raw_rows = list(filter(None, [line.strip() for line in f.readlines()]))

boards = []
i = 0
while i < len(raw_rows):
    boards.append(Board(raw_rows[i:i+BOARD_SIZE]))
    i += BOARD_SIZE

scores = []
while len(draws) > 0:
    draw = draws.pop(0)
    for i in range(len(boards)):
        if not boards[i].ended and boards[i].play(draw):
            score = boards[i].sum_unmarked() * int(draw)
            print(f'New board wins with score {score}')
            scores.append(score)

print(f'First score: {scores[0]}, last score: {scores[-1]}')
