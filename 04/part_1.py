import numpy as np
from pathlib import Path


def create_board(input_part):
    board = np.fromstring(input_part, dtype=int, sep=" ").reshape(5, 5)
    return board

def mark(board, draw):
    board[board == draw] = -1

def is_winner(board):
    return (board == -1).all(axis=0).any() or (board == -1).all(axis=1).any()

def get_score(board):
    board[board == -1] = 0
    return np.sum(board)

input = Path('04/input.txt').read_text()

input_parts = input.split("\n\n")

draws = [int(number) for number in input_parts[0].split(",")]
boards = [create_board(input_part) for input_part in input_parts[1:]]

for draw in draws:
    for board in boards:
        mark(board, draw)
        if is_winner(board):
            print('Answer:', draw * get_score(board))
            exit()
