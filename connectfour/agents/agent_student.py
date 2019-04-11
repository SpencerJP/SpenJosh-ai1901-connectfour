from connectfour.agents.computer_player import RandomAgent
from connectfour.board import Board
import time
#extension class of board to make up for any missing features it may have, such as counting moves
#this agent assumes that the height is 6 and width is 7

class StudentAgent(RandomAgent):
    PLAYER_ONE_ID = 1
    PLAYER_TWO_ID = 2
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 4
        self.nodes_counted = 0
        self.id = -1
        self.run_once = False
        self.dimensions = -1
        self.enemy_id = -1
        self.debug = False

    def get_current_player(self, num_moves):
        if(num_moves % 2 == 0 or num_moves == 0):
            return self.PLAYER_ONE_ID
        else:
            return self.PLAYER_TWO_ID

    def debug_print_board(self, board):
        string = ""
        for row in board.board:
            for cell in row:
                string += str(cell)
            string += str("\n")
        print(string)

    def count_moves(self, board):
        sum = 0
        for i in range(board.height):
            for j in range(board.width):
                if board.board[i][j] != 0:
                    sum = sum + 1

        return sum

    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """
        winner_num = board.winner()
        if (winner_num != 0):
            print("FAILURE, get_move() cannot be called as there is already a winner. winner id is %d" % winner_num)
            return

        start = time.time()
        current_move_number = self.count_moves(board)

        #check which player this agent is going to be
        if self.id == -1:
            self.id = self.get_current_player(current_move_number)
            self.enemy_id = self.get_current_player(current_move_number+1)
            if (self.debug):
                print("current player is %d" %self.id)
        #check board size
        if self.dimensions == -1:
            self.dimensions = board.width * board.height

        #valid_moves = board.valid_moves()
        #print("Valid moves: %d, movesSoFar: %d" % (len(list(valid_moves)), current_move_number))
        valid_moves = self.valid_non_losing_moves(board, current_move_number)
        # if len(list(valid_moves)) == 0:
        #     valid_moves = board.valid_moves()
        # else:
        #     valid_moves = self.valid_non_losing_moves(board, current_move_number)

        for move in valid_moves:
            print("valid move: col(%d)" % (move[1] + 1))
        valid_moves = self.valid_non_losing_moves(board, current_move_number)
        # no valid moves that won't cause a loss

        vals = []
        moves = []

        self.nodes_counted = 0

        column_number = 0
        for move in valid_moves:
            minimum = int(-(self.dimensions - current_move_number) / 2)

            maximum = int((self.dimensions + 1 - current_move_number) / 2)
            next_node = board.next_state( self.id, move[1] )
            moves.append( move )
            # while(minimum < maximum): #iterative deepening of the alpha/beta limits to prune alot of moves.
            #
            #     medium = int(minimum + (maximum - minimum) / 2)
            #     print("min: %d, max: %d, med: %d" % (minimum, maximum, medium))
            #     if(medium <= 0 and (minimum / 2) < medium):
            #          medium = minimum / 2
            #     elif(medium >= 0 and (maximum / 2) > medium):
            #          medium = maximum / 2
            #     result = int(self.negamax(next_node, medium, medium + 1, current_move_number+1, 1))
            #     if(result <= medium ):
            #          maximum = result
            #
            #     else:
            #        minimum = result
            if (column_number == 0):
                self.run_once = False
            score = -self.negamax(next_node, minimum, maximum, current_move_number)
            if (self.run_once == True):
                self.run_once = False
            # print("column number: %d, calculated value: %d" % (column_number+1, minimum))
            if (self.debug):
                print("column number: %d, calculated value: %d" % (column_number+1, score))
            column_number = column_number + 1
            vals.append( score ) #todo change to minimum

        if (self.debug):
            print("Counted %d nodes to make this move." % self.nodes_counted)
        if (len(vals) != 0):
            bestMove = moves[vals.index( max(vals) )]
        else:
            valid_moves = board.valid_moves()
            bestMove = next(valid_moves)

        next_node = board.next_state( self.id, bestMove[1] )

        end = time.time()
        if (self.debug):
            print("Took %r seconds to make this move." % (end - start))
            self.debug_print_board(next_node)
        return bestMove


        #
    def dfMiniMax(self, board, depth):
        # Goal return column with maximized scores of all possible next states

        # loop through next states (cols 1..w)
        # 	call dfMinimax of each resultant state

        #if depth == self.MaxDepth:
        #    return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()

        vals = []
        moves = []
        for move in valid_moves:
            next_state = board.next_state(move)
            moves.append( move )
            vals.append( self.dfMiniMax(next_state, depth + 1) )


        if depth % 2 == 1:
            bestVal = min(vals)
        else:
            bestVal = max(vals)

        return bestVal

    #returns moves that won't cause the agent to lose next turn
    def valid_non_losing_moves(self, board, num_moves):
        """
        returns: a generator of moves that don't cause a loss the turn after

        board: the node/game state to check
        num_moves: the amount of moves to get to this point
        """
        current_player = self.get_current_player(num_moves)
        other_player = self.get_current_player(num_moves+1)
        valid_moves = board.valid_moves()
        for move in valid_moves:
            my_move = board.next_state(current_player, move[1])
            winner_num = my_move.winner()
            if(winner_num != 0):
                yield(move)
                continue
            enemy_valid_moves = my_move.valid_moves()
            failure = False
            for enemy_move in enemy_valid_moves:
                node_after = my_move.next_state(other_player, enemy_move[1])
                winner_num = node_after.winner()
                if(winner_num != 0):
                    failure = True
                    break
            if(failure == False):
                yield(move)



        #recursive method
    def negamax(self, board, alpha, beta, num_moves, sign=1, depth=0):
        """returns score of the board position

        #board is the game state to evaluate
        alpha is the alpha value for the current node,
        beta is the beta value for the current node
        num_moves is the amount of moves that have been made so far. This is used in heuristic calculations as well
        as determining who's turn it is.
        sign is either 1 or -1 depending on whether board's last move is our agent's move or the enemy's.
        1 for our move, -1 for enemy move.
        depth is how deep our search has gone so far, beginning at 0 every time.
        """


        ## TODO:  make sure the current player will not win this move

        #print("last_move: (%d, %d), sign: %d" % (board.last_move[0], board.last_move[1], sign))
        #self.debug_print_board(board)
        #print("depth: %d, alpha: %d, beta: %d" % (depth, alpha, beta))
        #self.debug_print_board(board)

        #print("before - alpha: %d, beta: %d" %( alpha, beta))
        self.nodes_counted = self.nodes_counted + 1

        #check if this board has a winner and return if it does
        winner_num = board.winner()
        if(winner_num != 0):
                if self.run_once == True:
                    print("Passing up the value %d (terminal branch), depth: %d" % (sign * (self.dimensions - num_moves) / 2, depth))
                if (winner_num == self.id):
                    return sign * -int((self.dimensions - num_moves) / 2)
                else:
                    return sign * int((self.dimensions - num_moves) / 2)
        #detect a draw
        if(num_moves >= self.dimensions - 2):
            return 0

        #get a list of moves that won't cause you to lose, but only if we're on near the top of the tree,
        #because this slows the algorithm down significantly
        if (depth < 2):
            valid_moves = self.valid_non_losing_moves(board, num_moves)
        else:
            valid_moves = board.valid_moves()

        # no valid moves that won't cause a loss (TODO)
        if len(list(valid_moves)) == 0:
            return sign * (self.dimensions - num_moves) / 2

        # set alpha to the minimum possible value ##### todo -2 if you know that your opponent cant win
        min = int(-(self.dimensions - num_moves) / 2)
        if(alpha < min):
            alpha = min
            if(alpha >= beta):
                if(self.run_once):
                    print("min %d is less than alpha %d, pruning, depth: %d" % (min, alpha, depth))
                return alpha #prune children.

        # set beta to the maximum possible value  ##### todo -1 if you KNOW you cannot win this turn
        max = int( (self.dimensions - num_moves) / 2)
        if(beta > max):
            beta = max
            if(alpha >= beta):
                if(self.run_once):
                    print("max %d is greater than beta %d, pruning, depth: %d" % (min, beta, depth))
                return beta  #prune children.

        #could include transposition or a lookup table for early game stuff here.

        if depth == self.MaxDepth:
                    maxdepthvalue = self.evaluateBoardState(board)
                    if (maxdepthvalue <= alpha):
                        return alpha
                    elif (maxdepthvalue >= beta):
                        return beta
                    return maxdepthvalue

        valid_moves = self.valid_non_losing_moves(board, self.get_current_player(num_moves))
        value  = min
        for move in valid_moves:
            next_node = board.next_state(self.get_current_player(num_moves+1), move[1])
            #print("Recursively calling negamax, depth: %d" % depth)
            result = -self.negamax(next_node, -beta, -alpha, num_moves+1, -sign, depth + 1) # recursively go through the children of this node.
            if (result > value):
                if(self.run_once):
                    print("Result %d is larger than min value %d"  % (result, value))
                value = result
            else:
                if(self.run_once):
                    print("Result %d is smaller than min value %d" % (result, value))


            #if (self.run_once):
                #print("after - score: %d, alpha: %d, beta: %d, depth: %d, my turn?: %r" %(result[0], alpha, beta, depth, (self.get_current_player(num_moves) == self.id)))

            if(result > alpha):
                alpha = result

            if(alpha >= beta):
                break


        if(self.run_once):
            print("Passing up the value %d, depth: %d" % (value, depth))
        return value





    def evaluateBoardState(self, board):

        """
        Your evaluation function should look at the current state and return a score for it.
        As an example, the random agent provided works as follows:
            If the opponent has won this game, return -1.
            If we have won the game, return 1.
            If neither of the players has won, return a random number.
        """

        """
        These are the variables and functions for board objects which may be helpful when creating your Agent.
        Look into board.py for more information/descriptions of each, or to look for any other definitions which may help you.

        Board Variables:
            board.width
            board.height
            board.last_move
            board.num_to_connect
            board.winning_zones
            board.score_array
            board.current_player_score

        Board Functions:
            get_cell_value(row, col)
            try_move(col)
            valid_move(row, col)
            valid_moves()
            terminal(self)
            legal_moves()
            next_state(turn)
            winner()
        """

        return 0
