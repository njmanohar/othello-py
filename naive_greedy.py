# naive_greedy.py
# makes the next move by choosing the move that flips the most pieces
# in case of ties, a random choice is made

import random

def naive_greedy(game):
    validMoves = game.generate_moves()
    bestMoves = []
    bestScore = -(float("inf"))
    #iterate through moves and check which one results in the highest score (most pieces of our color)
    for move in validMoves:
        newGame = game.copy()
        newGame.play_move(move)
        newScore = newGame.score() * -1
        if newScore > bestScore:
            bestScore = newScore
            bestMoves = [move]
        elif newScore == bestScore:
            bestMoves.append(move)
    #if ties occur, randomly select from the list of tied moves
    return (bestScore, random.choice(bestMoves))