import numpy as np
from connectfour.agents.computer_player import RandomAgent

class StudentAgent(RandomAgent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 4
        # Conpensation for if StudentAgent is player 1(=1) or 2(=-1)
        self.player_id_compensation = 1 if int(name[-1]) == 1 else -1

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
            moves.append(move)
            vals.append(self.dfMiniMax(next_state, 1))

        bestMove = moves[vals.index(max(vals))]
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

            moves.append(move)
            vals.append(self.dfMiniMax(next_state, depth + 1))


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
        These are the variables and functions for board objects

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
            return self.player_id_compensation * 10000
        if board.winner() == 2:
            return self.player_id_compensation * -10000
        npboard = np.array(board.board)
        return self.player_id_compensation*(
            (
                vertical_threat(npboard) + horizontal_threat(npboard)
                + diagonal_threat(npboard))**2
            + central_heuristic(board)/10
        )


def vertical_threat(board_array):
    """Function to find vertical threats for each player
    """
    h, w = board_array.shape
    p1_threats = []
    p2_threats = []

    mask = np.array([0, 1, 1, 1])

    for c in range(w):
        for r in range(h-3):
            if (board_array[r:r+4, c] == mask).all():
                p1_threats.append((r, c))
            elif (board_array[r:r+4, c] == 2*mask).all():
                p2_threats.append((r, c))
    return p1_threats, p2_threats


def horizontal_threat(board_array):
    """Function to find horizontal threats for each player
    """
    h, w = board_array.shape
    p1_threats = []
    p2_threats = []
    masks = [np.array([0,1,1,1]),
             np.array([1,0,1,1]),
             np.array([1,1,0,1]),
             np.array([1,1,1,0])]


    for c in range(w-3):
        for r in range(h):
            board_slice = board_array[r, c:c+4]
            for index, mask in enumerate(masks):
                if (board_slice == mask).all():
                    p1_threats.append((r, c+index))
                elif (board_slice == 2*mask).all():
                    p2_threats.append((r, c+index))
    return p1_threats, p2_threats


def diagonal_threat(board_array):
    """Function to find diagonal_threats for each player
    """
    h, w = board_array.shape
    p1_threats = []
    p2_threats = []

    masks = [np.array([0,1,1,1]),
             np.array([1,0,1,1]),
             np.array([1,1,0,1]),
             np.array([1,1,1,0])]

    for c in range(w-3):
        for r in range(h-3):
            board_slices = [board_array[r:r+4, c:c+4].diagonal(),
                            np.fliplr(board_array[r:r+4, c:c+4]).diagonal()]
            for positive_slope, board_slice in enumerate(board_slices):
                for index, mask in enumerate(masks):
                    if (board_slice == mask).all():
                        if positive_slope:
                            p1_threats.append((r+index, c+(3-index)))
                        else:
                            p1_threats.append((r+index, c+index))
                    elif (board_slice == 2*mask).all():
                        if positive_slope:
                            p2_threats.append((r+index, c+(3-index)))
                        else:
                            p2_threats.append((r+index, c+index))
    return p1_threats, p2_threats


def central_heuristic(board):
    """Simple heuristic to favour boards that have more central tokens
    Returns the sum of the tokens multiplied by their distance from edge of board
    outer column = 0, middle column = 3 for a 7 column board
    """
    middle_score = 0
    middle_col = round((board.width+1)/2)-1
    for row in board.board:
        for col in range(board.width):
            score = middle_col-abs(middle_col-col)
            if row[col] == 1:
                middle_score += score
            elif row[col] == 2:
                middle_score -= score
    return middle_score
