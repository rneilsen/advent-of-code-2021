import numpy as np
from collections import deque
import time
start_time = time.time()

positions = [4, 8]
# positions = [9, 10]

positions = [p - 1 for p in positions]

def det_die():
    while True:
        for i in range(1, 101):
            yield i

def rolls(die):
    while True:
        yield (next(die), next(die), next(die))

scores = [0, 0]
die = det_die()
roller = rolls(die)

target = 1000    
player = 0
num_rolls = 0
while max(scores) < target:
    positions[player] = (positions[player] + sum(next(roller))) % 10
    num_rolls += 3
    scores[player] += positions[player] + 1
    player = 1 - player

print(f'Part 1: {min(scores) * num_rolls} ({time.time() - start_time:0.2f}s)')
start_time = time.time()

# number of universes generated for each possible sum on Dirac die
dirac_results = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

positions = (4, 8)
target = 21
wins = [0, 0]
positions = (9, 10) # input

positions = tuple(pos - 1 for pos in positions)
# gamestate: (p1pos, p2pos, p1score, p2score, player, universes)
gamestates = deque([positions + (0, 0, 0, 1)])
states_processed = 0
while gamestates:
    state = gamestates.popleft()
    player = state[-2]
    for result, univ_count in dirac_results.items():
        new_pos = (state[player] + result) % 10
        new_score = state[2+player] + new_pos + 1
        num_universes = state[-1] * univ_count
        
        if new_score >= target:
            wins[player] += num_universes
        else:
            if player == 0:
                new_state = (new_pos, state[1], new_score, state[3], 1, num_universes)
            else:
                new_state = (state[0], new_pos, state[2], new_score, 0, num_universes)
            gamestates.append(new_state)
    states_processed += 1
    if states_processed % 100000 == 0:
        print(f'{states_processed} processed, {len(gamestates)} remaining')

print(f'Part 2: {max(wins)} ({states_processed} states processed in {time.time() - start_time:0.2f}s)')