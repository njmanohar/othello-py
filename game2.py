# game2: play a 2 person game
# we did not modify this file except to put test cases at the end

from time import time

class IllegalMove(Exception):
    pass

def play(game, player1, player2, verbose = True):
    """Play a game between two players. Can raise IllegalMove"""

    next = 1 # player 1 has to move first
    player1_think = 0.0 # total think time
    player1_ply = 0
    player2_think = 0.0
    player2_ply = 0

    if verbose:
        print game
        
    last_move = None
    while not game.terminal_test():
        # make a temp copy of the game so that the player doesn't mess
        # with it
        temp = game.copy()
        # compute the next move for the player
        t1 = time()
        if next == 1:
            (value, move) = player1.play(temp, last_move)
        else:
            (value, move) = player2.play(temp, last_move)
        t2 = time()
        last_move = move
        # update player think time statistics
        if next == 1:
            player1_ply += 1
            player1_think += t2-t1
        else:
            player2_ply += 1
            player2_think += t2-t1

        if verbose:            
            print ("player %d plays %s (in %.1f s) evaluation value %d"
                   % (next, str(move), t2-t1, value))
        #check that the move is valid before applying it
        if move not in game.generate_moves():
            raise IllegalMove
        game.play_move(move)
        if verbose:
            print game
            print "(player", next, "score", -1*game.score(), ")"
        # switch the next player and continue the game play loop
        next = 3 - next


    score = game.score()
    if score > 0:
        print "player "+str(next)+" won with score", score
    elif score < 0:
        print "player "+str(3-next)+" won with score", -1*score
    else:
        winner = 0
        print "DRAW!!"

    temp = game.copy()
    player1.gameover(temp, last_move)
    player2.gameover(temp, last_move)

    if player1_ply and player2_ply:
        print "%d ply: Player 1 %.1f s per ply. Player2 %.1f s per ply" % (
            player1_ply+player2_ply, player1_think/player1_ply,
            player2_think/player2_ply)

def user_player(game):
    """Make a user player to play the game."""

    while True:
        inp = raw_input("Your Move")
        try:
            move = eval(inp)
        except SyntaxError:
            print "Error: garbage move"
            continue
        if move not in game.generate_moves():
            print "Error: illegal move", move, type(move)
            print "Valid moves are", game.generate_moves()
            continue
        break

    return (0, move)    

class player:
    def __init__(self, play_fn):
        self.play_fn = play_fn

    def play(self, game, opp_move):
        return self.play_fn(game)

    def gameover(self, game, last_move):
        pass
    
if __name__ == "__main__":
    import othello
    import minimax
    import naive_greedy
    import naive_random
    import qlearning

    # Learning phase
    qlearn = qlearning.QLearning()

    numTrials = 1000
    for trial in range(numTrials):
        if numTrials % 2 == 0:
            print "Playing game vs positional as white ", trial
            play(othello.game(), player(lambda x: minimax.alphabeta(x, 3, othello.positional_eval)),
                player(lambda x: qlearn.run(x, trial)), False)
        else:
            print "Playing game vs positional as black ", trial
            play(othello.game(), player(lambda x: qlearn.run(x, trial)), 
                player(lambda x: minimax.alphabeta(x, 3, othello.positional_eval)), False)

    numTrials = 9999999999
    print "naive random as white"
    play(othello.game(), player(lambda x: naive_random.naive_random(x)),
        player(lambda x: qlearn.run(x, numTrials)), False)
    print "naive greedy as white"
    play(othello.game(), player(lambda x: naive_greedy.naive_greedy(x)),
        player(lambda x: qlearn.run(x, numTrials + 1)), False)
    print "positional as white"
    play(othello.game(), player(lambda x: minimax.alphabeta(x, 3, othello.positional_eval)),
        player(lambda x: qlearn.run(x, numTrials + 2)), False)
    print "mobility as white"
    play(othello.game(), player(lambda x: minimax.alphabeta(x, 3, othello.mobility_eval)),
        player(lambda x: qlearn.run(x, numTrials + 3)), False)
    print "edge as white"
    play(othello.game(), player(lambda x: minimax.alphabeta(x, 3, othello.edge_eval)),
        player(lambda x: qlearn.run(x, numTrials + 4)), False)
    print "naive random as black"
    play(othello.game(), player(lambda x: qlearn.run(x, numTrials + 5)), 
        player(lambda x: naive_random.naive_random(x)), False)
    print "naive greedy as black"
    play(othello.game(), player(lambda x: qlearn.run(x, numTrials + 6)), 
        player(lambda x: naive_greedy.naive_greedy(x)), False)
    print "positional as black"
    play(othello.game(), player(lambda x: qlearn.run(x, numTrials + 7)), 
        player(lambda x: minimax.alphabeta(x, 3, othello.positional_eval)), False)
    print "mobility as black"
    play(othello.game(), player(lambda x: qlearn.run(x, numTrials + 8)), 
        player(lambda x: minimax.alphabeta(x, 3, othello.mobility_eval)), False)
    print "edge as black"
    play(othello.game(), player(lambda x: qlearn.run(x, numTrials + 9)), 
        player(lambda x: minimax.alphabeta(x, 3, othello.edge_eval)), False)

    # numTrials = 500
    # for trial in range(numTrials/2):
    #     print "Playing game vs positional as white ", trial
    #     play(othello.game(), player(lambda x: minimax.alphabeta(x, 4, othello.positional_eval)),
    #         player(lambda x: qlearn.run(x, trial)), False)
    # for trial in range(numTrials/2):
    #     print "Playing game vs mobility as white", trial
    #     play(othello.game(), player(lambda x: minimax.alphabeta(x, 4, othello.mobility_eval)),
    #         player(lambda x: qlearn.run(x, trial + (numTrials/2))), False)
    # for trial in range(numTrials/2):
    #     print "Playing game vs positional as black", trial
    #     play(othello.game(), player(lambda x: qlearn.run(x, trial + numTrials)), 
    #         player(lambda x: minimax.alphabeta(x, 4, othello.positional_eval)), False)
    # for trial in range(numTrials/2):
    #     print "Playing game vs mobility as black", trial
    #     play(othello.game(), player(lambda x: qlearn.run(x, trial + ((3 * numTrials)/2))), 
    #         player(lambda x: minimax.alphabeta(x, 4, othello.mobility_eval)), False)

    # print "naive random as white"
    # play(othello.game(), player(lambda x: naive_random.naive_random(x)),
    #     player(lambda x: qlearn.run(x, (2 * numTrials))), False)
    # print "naive greedy as white"
    # play(othello.game(), player(lambda x: naive_greedy.naive_greedy(x)),
    #     player(lambda x: qlearn.run(x, (2 * numTrials) + 1)), False)
    # print "positional as white"
    # play(othello.game(), player(lambda x: minimax.alphabeta(x, 4, othello.positional_eval)),
    #     player(lambda x: qlearn.run(x, (2 * numTrials) + 2)), False)
    # print "mobility as white"
    # play(othello.game(), player(lambda x: minimax.alphabeta(x, 4, othello.mobility_eval)),
    #     player(lambda x: qlearn.run(x, (2 * numTrials) + 3)), False)
    # print "edge as white"
    # play(othello.game(), player(lambda x: minimax.alphabeta(x, 4, othello.edge_eval)),
    #     player(lambda x: qlearn.run(x, (2 * numTrials) + 4)), False)
    # print "naive random as black"
    # play(othello.game(), player(lambda x: qlearn.run(x, (2 * numTrials) + 5)), 
    #     player(lambda x: naive_random.naive_random(x)), False)
    # print "naive greedy as black"
    # play(othello.game(), player(lambda x: qlearn.run(x, (2 * numTrials) + 6)), 
    #     player(lambda x: naive_greedy.naive_greedy(x)), False)
    # print "positional as black"
    # play(othello.game(), player(lambda x: qlearn.run(x, (2 * numTrials) + 7)), 
    #     player(lambda x: minimax.alphabeta(x, 4, othello.positional_eval)), False)
    # print "mobility as black"
    # play(othello.game(), player(lambda x: qlearn.run(x, (2 * numTrials) + 8)), 
    #     player(lambda x: minimax.alphabeta(x, 4, othello.mobility_eval)), False)
    # print "edge as black"
    # play(othello.game(), player(lambda x: qlearn.run(x, (2 * numTrials) + 9)), 
    #     player(lambda x: minimax.alphabeta(x, 4, othello.edge_eval)), False)

    # # Experiment 1:
    # # Player 1 and Player 2 are evenly matched with 3-ply deep search
    # # player 2 wins with a final score of 28
    # # player 1 0.2 s per ply player 2 0.4 s per ply
    # play(othello.game(), player(lambda x: minimax.alphabeta(x, 4, othello.positional_eval)),
    #      player(lambda x: minimax.minimax(x, 3)), False)
    
    # # Experiment 2:
    # # now we show the significance of an evaluation function
    # # we weaken player1 to 2 ply deep but use the edge eval fun
    # # player 1 now beats player 2 with a score of 58!
    # # player 1 0.1 s per ply player 2 0.4 s per ply
    # play(othello.game(), player(lambda x: minimax.alphabeta(x, 4, othello.positional_eval)),
    #      player(lambda x: naive_random.naive_random(x)), False)

    # # Experiment 1 (with alpha-beta):
    # # player 1 0.1 s per ply, player 2 0.1 s per ply
    # play(othello.game(), player(lambda x: minimax.alphabeta(x, 4, othello.positional_eval)),
    #      player(lambda x: minimax.alphabeta(x, 3)), False)

    # # Experiment 2 (with alpha-beta):
    # # player 1 0.0 s per ply player 2 0.1 s per ply
    # play(othello.game(), player(lambda x: minimax.alphabeta(x, 4, othello.positional_eval)),
    #      player(lambda x: minimax.alphabeta(x, 4, othello.edge_eval)), False)


    # # Experiment 3
    # # player 1 alpha beta with 0.1 s per ply, player 2 is naive_greedy
    # play(othello.game(), player(lambda x: minimax.alphabeta(x,4, othello.positional_eval)), player(lambda x: naive_greedy.naive_greedy(x)), False)