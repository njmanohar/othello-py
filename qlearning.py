#qlearning.py
#Implementation of the Q Learning Agent
import random, util, math, sys

class QLearning():

	def __init__(self):
		self.values = util.Counter()
        #values set for the (a,b,c) vector for the temperature that controls exploration
        #gamma = 1, so no discount factor, and a learning rate of 0.1
		self.alpha = 0.1
		self.gamma = 1
		self.temp_a = 1
		self.temp_b = 0.9999995
		self.temp_c = 0.002

	def getQValue(self, game, action):
		"""
		  Returns Q(state,action)
		  Should return 0.0 if we have never seen a state
		  or the Q node value otherwise
		"""
		game_board = tuple(tuple(x) for x in game.board)
		return self.values[(game_board, action)]

	def computeValueFromQValues(self, game):
		"""
		  Returns max_action Q(state,action)
		  where the max is over legal actions.  Note that if
		  there are no legal actions, which is the case at the
		  terminal state, you should return a value of 0.0.
		"""
		"*** YOUR CODE HERE ***"

        #simply return the q-value of the best action if one exists; otherwise return 0.0
		best_action = self.computeActionFromQValues(game)
		if best_action == None:
			return 0.0
		else:
			game_board = tuple(tuple(x) for x in game.board)
			return self.values[(game_board, best_action)]

	def computeActionFromQValues(self, game):
		"""
		  Compute the best action to take in a state.  Note that if there
		  are no legal actions, which is the case at the terminal state,
		  you should return None.
		"""
		"*** YOUR CODE HERE ***"
		actions = game.generate_moves()

		if len(actions) == 0:
			return None

        # track all best actions - if there are ties, keep all
		best_actions = []
		max_val = -sys.maxint - 1
		for action in actions:
			if self.getQValue(game, action) > max_val:
				best_actions = [action]
				max_val = self.getQValue(game, action)
			elif self.getQValue(game, action) == max_val:
				best_actions.append(action)

        # randomly choose from best actions
		return random.choice(best_actions)

	def getAction(self, game, numPlayed):
		"""
		  Compute the action to take in the current state.  With
		  probability self.epsilon, we should take a random action and
		  take the best policy action otherwise.  Note that if there are
		  no legal actions, which is the case at the terminal state, you
		  should choose None as the action.

		  HINT: You might want to use util.flipCoin(prob)
		  HINT: To pick randomly from a list, use random.choice(list)
		"""

		actions = game.generate_moves()

		if len(actions) == 0:
			return None

		temperature = 0

		prob_actions = {}

        #use temperature according to explanation in writeup to select whether or not to explore
		if self.temp_a * (self.temp_b ** numPlayed) >= self.temp_c:
			temperature = self.temp_a * (self.temp_b ** numPlayed)
			for _action in actions:
				summation = 0
				for action in actions:
					summation += math.exp(self.getQValue(game, action) / temperature)
				prob_actions[_action] = math.exp(self.getQValue(game, _action)) / summation

			r = random.random()
			for action in prob_actions.keys():
				if r < prob_actions[action]:
					return action
				else:
					r -= prob_actions[action]
			return None
		else: 
			return self.computeActionFromQValues(game)

	def update(self, game, action, nextGame, reward):
		"""
		  The parent class calls this to observe a
		  state = action => nextState and reward transition.
		  You should do your Q-Value update here

		  NOTE: You should never call this function,
		  it will be called on your behalf
		"""
		"*** YOUR CODE HERE ***"
		# update Q-values according to equation
		game_board = tuple(tuple(x) for x in game.board)
		self.values[(game_board, action)] = self.getQValue(game, action) + \
		        self.alpha * (reward + (self.gamma * self.computeValueFromQValues(nextGame)) - self.getQValue(game, action))

    # def getPolicy(self, game):
    #     return self.getAction(game)

	def getValue(self, game):
		return self.computeValueFromQValues(game)

	def run(self, game, numPlayed):
        #threshold is # of occupied squares when we start checking for terminal states
		threshold = 60
		game_copy = game.copy()
		action = self.getAction(game_copy, numPlayed)
		game_copy.play_move(action)
		num_occupied = 0
		for i in range(8):
			for j in range(8):
				if game_copy.board[i][j] != 0:
					num_occupied = num_occupied + 1

        #check for terminal states
		if num_occupied >= threshold:
			if game_copy.terminal_test():
				score = 0
				for i in range(8):
					for j in range(8):
						score += game_copy.board[i][j]

				if score * game.player < 0: #player lost
					self.update(game, action, game_copy, -1)
				elif score * game.player > 0: #player won
					self.update(game, action, game_copy, 1)
				else: #draw
					self.update(game, action, game_copy, 0)
			else:
				updated = 0
				opp_moves = game_copy.generate_moves()
				num_lost = 0
				num_moves = len(opp_moves)
				for move in opp_moves:
					if updated == 0:
						new_game = game_copy.copy()
						new_game.play_move(move)
						if new_game.terminal_test():
							score = 0
							for i in range(8):
								for j in range(8):
									score += game_copy.board[i][j]

							if score * game_copy.player < 0: #opponent lost
								num_lost = num_lost + 1
                                #if every opponent move results in a win for us
								if num_lost == num_moves:
									self.update(game, action, game_copy, 1)
									updated = 1
									break
                            #if the opponent can win the game
							elif score * game_copy.player > 0: #opponent won
								self.update(game, action, game_copy, -1)
								updated = 1
								break

				if updated == 0:
					self.update(game, action, game_copy, 0)
		else:
			self.update(game, action, game_copy, 0)
				


		return (0, action)
