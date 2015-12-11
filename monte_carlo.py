# monte_carlo.py
# makes next move by running Monte Carlo simulations of games by making random moves to determine which moves wins with the highest probability
# simulations is the number of simulations we make for each move

import random

#recursively makes random moves on the game until it reaches a terminal state and returns the result
def make_random_move(game):
    if game.terminal_test():
        score = 0
        for i in range(8):
            for j in range(8):
                score += game.board[i][j]
        # black won
        if score < 0:
            return -1
        # white won
        elif score > 0:
            return 1
        # draw
        else:
            return 0
    else:
        validMoves = game.generate_moves()
        random_move = random.choice(validMoves)
        game.play_move(random_move)
        make_random_move(game)
        return 0

def monte_carlo(game, simulations):
    validMoves = game.generate_moves()
    scores = {}
    for key in validMoves:
        scores[key] = 0
    for move in scores.keys():
        for _ in range(simulations):
            new_game = game.copy()
            new_game.play_move(move)
            #update scores[move] by the result of the game played that took move
            scores[move] += make_random_move(new_game)
    #black wants to minimize scores since -1 means win for black
    if game.player == -1:
        return (0,min(scores, key=scores.get))
    #white wants to maximize scores
    elif game.player == 1:
        return (0,max(scores, key=scores.get))
    
    return 0