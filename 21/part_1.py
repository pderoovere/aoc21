from pathlib import Path

class Die:

    def __init__(self):
        self.value = -1
        self.nb_rolls = 0

    def roll(self):
        self.value = (self.value % 100) + 1
        self.nb_rolls += 1
        return self.value + 1


class Player:

    def __init__(self, starting_pos):
        self.pos = starting_pos
        self.score = 0

    def play(self, die):
        print('Player 1 playing on', self.pos, 'with score', self.score)
        increase = 0
        for _ in range(3):
            increase += die.roll()
        self.pos = ((self.pos + increase - 1) % 10 + 1)
        self.score += self.pos
        print('Changed to', self.pos, 'after increase with', increase, 'with score', self.score)
        return self.score


lines = Path('21/input.txt').read_text().strip('\n').split('\n')
player_1 = Player(int(lines[0].split(' ')[-1]))
player_2 = Player(int(lines[1].split(' ')[-1]))
die = Die()

def play():
    while True:
        if player_1.play(die) >= 1000:
            return player_2.score * die.nb_rolls
        if player_2.play(die) >= 1000:
            return player_1.score * die.nb_rolls

print('Answer', play())