from connectfour.agents.computer_player import RandomAgent
from connectfour.board import Board
import copy
#extension class of board to make up for any missing features it may have, such as counting moves
#this agent assumes that the height is 6 and width is 7

class StudentAgent(RandomAgent):
    DIMENSIONS = 42
    PLAYER_ONE_ID = 1
    PLAYER_TWO_ID = 2
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 5
        self.nodes_counted = 0
        self.id = -1
        self.run_once = False

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


        current_move_number = self.count_moves(board)

        if self.id == -1:
            self.id = self.get_current_player(current_move_number)
            print("Current Player is %d" % self.id)

        #valid_moves = board.valid_moves()
        #print("Valid moves: %d, movesSoFar: %d" % (len(list(valid_moves)), current_move_number))
        valid_moves = board.valid_moves()

        # no valid moves that won't cause a loss

        vals = []
        moves = []

        self.nodes_counted = 0

        column_number = 0
        for move in valid_moves:
            minimum = int(-(self.DIMENSIONS - current_move_number) / 2)

            maximum = int((self.DIMENSIONS + 1 - current_move_number) / 2)
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
            #         minimum = result
            # if (column_number == 2):
            #     self.run_once = True
            score = self.negamax(next_node, -self.MaxDepth, self.MaxDepth, current_move_number+1, 0)
            if (self.run_once == True):
                self.run_once = False
            # print("column number: %d, calculated value: %d" % (column_number+1, minimum))
            print("column number: %d, calculated value: %d" % (column_number+1, score[0]))
            column_number = column_number + 1
            vals.append( score[0] ) #todo change to minimum

        print("Counted %d nodes to make this move." % self.nodes_counted)

        bestMove = moves[vals.index( max(vals) )]
        next_node = board.next_state( self.id, bestMove[1] )
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
    def valid_non_losing_moves(self, board, current_player_id):
        valid_moves = board.valid_moves()
        for move in valid_moves:
            next_node = board.next_state(current_player_id, move[1])
            winner_num = next_node.winner()
            if(winner_num == current_player_id or winner_num == 0):
                yield(move)
        return valid_moves


        #recursive method
    def negamax(self, board, alpha, beta, num_moves, depth):
        #returns score of the board position

        #node is the game state to evaluate
        #alpha is the alpha value for the current node,
        #beta is the beta value for the current node


        ## TODO:  make sure the current player will not win this move

        #print("depth: %d, alpha: %d, beta: %d" % (depth, alpha, beta))
        #self.debug_print_board(board)

        #print("before - alpha: %d, beta: %d" %( alpha, beta))
        self.nodes_counted = self.nodes_counted + 1


        winner_num = board.winner()
        if(winner_num != 0):
                if (self.run_once):
                    self.debug_print_board(board)
                return ((self.DIMENSIONS - num_moves) / 2, False)
        #detect a draw
        if(num_moves >= self.DIMENSIONS - 2):
            return (0, False)

        #get a list of moves that won't cause you to lose
        valid_moves = self.valid_non_losing_moves(board, self.get_current_player(num_moves))

        # no valid moves that won't cause a loss (TODO)
        if len(list(valid_moves)) == 0:
            return (-(self.DIMENSIONS - num_moves) / 2, False)

        # set alpha to the minimum possible value ##### todo -2 if you know that your opponent cant win
        min = -(self.DIMENSIONS - num_moves) / 2
        if(alpha < min):
            alpha = min
            if(alpha >= beta):
                return (alpha, False) #prune children.

        # set beta to the maximum possible value  ##### todo -1 if you KNOW you cannot win this turn
        max = (self.DIMENSIONS - num_moves) / 2
        if(beta > max):
            beta = max
            if(alpha >= beta):
                return (beta, False)  #prune children.

        #could include transposition or a lookup table for early game stuff here.

        if depth == self.MaxDepth:
                    return (self.evaluateBoardState(board), True)

        valid_moves = self.valid_non_losing_moves(board, self.get_current_player(num_moves))
        for move in valid_moves:
            next_node = board.next_state(self.get_current_player(num_moves), move[1])
            #print("Recursively calling negamax, depth: %d" % depth)
            result = self.negamax(next_node, -beta, -alpha, num_moves+1, depth + 1) # recursively go through the children of this node.

            #if (self.run_once):
                #print("after - score: %d, alpha: %d, beta: %d, depth: %d, my turn?: %r" %(result[0], alpha, beta, depth, (self.get_current_player(num_moves) == self.id)))

            #have to "flip" the sign of the result score as part of the minmax, which is why they all have negative signs
            if(-result[0] >= beta):
              #todo save into trans table
              #prune
              return (-result[0], False)

            if(-result[0] > alpha):
                if(result[1]==False):
                    alpha = -result[0]



        return (alpha, False)





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
