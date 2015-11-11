# naive_random.py
# makes next move by randomly choosing from valid moves

import random

def naive_random(game):
    validMoves = game.generate_moves()
    return (0,random.choice(validMoves))