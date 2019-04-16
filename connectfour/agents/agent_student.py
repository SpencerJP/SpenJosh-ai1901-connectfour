from connectfour.agents.computer_player import RandomAgent
import random
import numpy as np

class StudentAgent(RandomAgent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 5


    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            next_state = board.next_state(self.id, move[1])
            moves.append( move )
            vals.append( self.dfMiniMax(next_state, 1) )

        bestMove = moves[vals.index( max(vals) )]
        return bestMove

    def dfMiniMax(self, board, depth):
        # Goal return column with maximized scores of all possible next states
        
        if depth == self.MaxDepth:
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            if depth % 2 == 1:
                next_state = board.next_state(self.id % 2 + 1, move[1])
            else:
                next_state = board.next_state(self.id, move[1])
                
            moves.append( move )
            vals.append( self.dfMiniMax(next_state, depth + 1) )

        
        if depth % 2 == 1:
            bestVal = min(vals)
        else:
            bestVal = max(vals)

        return bestVal

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
        if board.winner() == 1:
            score = 10000
        elif board.winner() == 2:
            score = -10000
        else:
            score_sum = []
            middle_col = round((board.width+1)/2)-1
            for row in board.board:
                for col in range(board.width):
                    if row[col] == 1:
                        score_sum.append(middle_col-abs(middle_col-col))
            score = sum(score_sum)
        return score


def vertical_threat(board_array):
    """Function to determine how many vertical threats exist
    returns score for how many more threats player1 has over player2
    """
    h, w = board_array.shape
    score = 0

    mask = np.array([0, 1, 1, 1])

    for c in range(w):
        for r in range(h-3):
            if (board_array[r:r+4, c] == mask).all():
                score += 1
            elif (board_array[r:r+4, c] == 2*mask).all():
                score -= 1
    return score


def horizontal_threat(board_array):
    """Function to determine how many horizontal threats exist
    returns score for how many more threats player1 has over player2
    """
    h, w = board_array.shape
    score = 0

    masks = [np.array([1,1,1,0]),
             np.array([1,1,0,1]),
             np.array([1,0,1,1]),
             np.array([0,1,1,1])]


    for c in range(w-3):
        for r in range(h):
            board_slice = board_array[r, c:c+4]
            for mask in masks:
                if (board_slice == mask).all():
                    score += 1
                elif (board_slice == 2*mask).all():
                    score -= 1
    return score
