from connectfour.agents.computer_player import RandomAgent
from connectfour.board import Board
import copy
#extension class of board to make up for any missing features it may have, such as counting moves
#this agent assumes that the height is 6 and width is 7
class Node(Board):
    PLAYER_ONE_ID = 1
    PLAYER_TWO_ID = 2

    def __init__(self, board, node = None, num_moves = 0):
        if node:
            self.board = copy.deepcopy(node.board)
            self.height = node.height
            self.width = node.width
            self.num_to_connect = 4
            self.num_moves = num_moves
        else:
            self.height = board.height
            self.width = board.width
            self.board = copy.deepcopy(board.board)
            self.num_moves = num_moves
            self.num_to_connect = 4

    def try_move(self, move):
        if move < 0 or move >= self.width or self.board[0][move] != 0:
            return -1

        for i in range(len(self.board)):
            if self.board[i][move] != 0:
                return i - 1
        return len(self.board) - 1

    def valid_move(self, row, col):
        return row >= 0 and self.try_move(col) == row

    def valid_moves(self):
        for col in range(self.width):
            for row in range(self.height):
                if self.valid_move(row, col):
                    yield (row, col)

    def next_state(self, turn):
        aux = copy.deepcopy(self)
        aux.num_moves = aux.num_moves + 1
        aux.last_move = turn
        print("Turn: (%d, %d)" % turn)
        aux.board[turn[0]][turn[1]] = aux.get_current_player()
        print(aux.board[turn[0]][turn[1]])
        return aux

    def get_current_player(self):
        if(self.num_moves % 2 == 1):
            return self.PLAYER_TWO_ID
        else:
            return self.PLAYER_ONE_ID



class StudentAgent(RandomAgent):
    DIMENSIONS = 42
    DEBUG = False
    DEBUG2 = False
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 43
        self.Debug = True
        self.nodes_counted = 0
        self.player_id_of_this_agent = -1

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

        if (self.player_id_of_this_agent == -1):
            if (current_move_number == 0):
                self.player_id_of_this_agent = 1
            else:
                self.player_id_of_this_agent = 2

        #valid_moves = board.valid_moves()
        #print("Valid moves: %d, movesSoFar: %d" % (len(list(valid_moves)), current_move_number))
        valid_moves = board.valid_moves()

        # no valid moves that won't cause a loss

        vals = []
        moves = []

        if self.DEBUG:
            self.nodes_counted = 0

        moveno = 0
        for move in valid_moves:
            minimum = -(self.DIMENSIONS - current_move_number) / 2

            maximum = (self.DIMENSIONS + 1 - current_move_number) / 2
            next_node = Node(board, None, current_move_number)
            next_node = next_node.next_state( move )
            moves.append( move )
            self.debug_print_board(next_node)
            while(minimum < maximum):

                medium = int(minimum + (maximum - minimum) / 2)
                if(medium <= 0 and (minimum / 2) < medium):
                     medium = minimum / 2
                elif(medium >= 0 and (maximum / 2) > medium):
                     medium = maximum / 2
                result = int(self.negamax(next_node, medium, medium + 1, 1))
                if(result <= medium ):
                     maximum = result

                else:
                    minimum = result

            print("column number: %d, calculated value: %d" % (moveno+1, minimum))
            moveno = moveno + 1
            vals.append( minimum )

        if self.DEBUG:
            print("Counted %d nodes to make this move." % self.nodes_counted)

        bestMove = moves[vals.index( max(vals) )]
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
    def valid_non_losing_moves(self, board):

        valid_moves = board.valid_moves()

        ## TODO: remove all moves that will cause you to lose the turn after
        return valid_moves


        #recursive method
    def negamax(self, node, alpha, beta, depth):
        #returns score of the board position

        #node is the game state to evaluate
        #alpha is the alpha value for the current node,
        #beta is the beta value for the current node


        ## TODO:  make sure the current player will not win this move

        #self.debug_print_board(node)

        if self.DEBUG:
            self.nodes_counted = self.nodes_counted + 1

        if depth == self.MaxDepth:
            return self.evaluateBoardState(node)
        winner_num = node.winner()
        if (winner_num == 1 or winner_num == 2):
            if self.DEBUG2:
                self.debug_print_board(node)
            return -(self.DIMENSIONS - node.num_moves) / 2
        #detect a draw
        if(node.num_moves >= self.DIMENSIONS - 2):
            if self.DEBUG2:
                self.debug_print_board(node)
            return 0

        #get a list of moves that won't cause you to lose
        valid_moves = node.valid_moves()

        # no valid moves that won't cause a loss
        if len(list(valid_moves)) == 0:
           return -(self.DIMENSIONS - node.num_moves) / 2

        # set alpha to the minimum possible value
        min = -(self.DIMENSIONS - 2 - node.num_moves) / 2
        if(alpha < min):
            alpha = min
            if(alpha >= beta):
                if self.DEBUG2:
                    print("prune a")
                return alpha #prune children.

        # set beta to the maximum possible value
        max = (self.DIMENSIONS - 1 - node.num_moves) / 2
        if(beta > max):
            beta = max
            if(alpha >= beta):
                if self.DEBUG2:
                    print("prune b")
                return beta #prune children.

        #could include transposition or a lookup table for early game stuff here.
        valid_moves = node.valid_moves()
        for move in valid_moves:
            if(self.DEBUG2):
                print("move")
            node2 = copy.deepcopy(node)
            node2.num_moves = node.num_moves + 1
            node2.last_move = move
            node2.board[move[0]][move[1]] = node2.get_current_player()
            self.debug
            score = -self.negamax(node2, -beta, -alpha, depth + 1) # recursively go through the children of this node.

            if(score >= beta):
              #save into trans table
              if self.DEBUG2:
                  print("return score %d" % score)
              return score

            if(score > alpha):
                alpha = score

        if self.DEBUG2:
            print("return alpha %d" % alpha)
        return alpha






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