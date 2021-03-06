from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache, reduce
import operator

moves = defaultdict(int)
for i in range(1, 4):
    for j in range(1, 4):
        for k in range(1, 4):
            moves[i + j + k] += 1

@dataclass(unsafe_hash=True)
class State:
    player_1_pos: int
    player_1_score: int
    player_2_pos: int
    player_2_score: int
    active_player: int

    def __increase_pos(self, pos, increase):
        return ((pos + increase - 1) % 10 + 1)

    def play(self, increase):
        if self.active_player == 1:
            player_1_pos = self.__increase_pos(self.player_1_pos, increase)
            player_1_score = self.player_1_score + player_1_pos
            return State(player_1_pos, player_1_score, self.player_2_pos, self.player_2_score, 2)
        else:
            player_2_pos = self.__increase_pos(self.player_2_pos, increase)
            player_2_score = self.player_2_score + player_2_pos
            return State(self.player_1_pos, self.player_1_score, player_2_pos, player_2_score, 1)

@dataclass
class Outcomes:
    player_1_wins: int
    player_2_wins: int

    def __mul__(self, other):
        return Outcomes(self.player_1_wins * other, self.player_2_wins * other)

    def __add__(self, other):
        return Outcomes(self.player_1_wins + other.player_1_wins, self.player_2_wins + other.player_2_wins)

@lru_cache(100_000)
def simulate(state):
    if state.player_1_score >= 21:
        return Outcomes(1, 0)
    elif state.player_2_score >= 21:
        return Outcomes(0, 1)
    else:
        outcomes = [simulate(state.play(increase)) * count for increase, count in moves.items()]
        return reduce(operator.add, outcomes)

# Fill up the cache, starting with almost-finished states
for p1_pos in range(10, 0, -1):
    for p2_pos in range(10, 0, -1):
        for p1_score in range(20, -1, -1):
            for p2_score in range(20, -1, -1):
                simulate(State(p1_pos, p1_score, p2_pos, p2_score, 1))
                simulate(State(p1_pos, p1_score, p2_pos, p2_score, 2))

lines = Path('21/input.txt').read_text().strip('\n').split('\n')
player_1 = int(lines[0].split(' ')[-1])
player_2 = int(lines[1].split(' ')[-1])

# Simulate using the actual state
state = State(player_1, 0, player_2, 0, 1)
outcome = simulate(state)

print('Outcome:', max(outcome.player_1_wins, outcome.player_2_wins))