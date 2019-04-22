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

        # Get set of threats for each player
        npboard = np.array(board.board)
        p1_threats = set()
        p2_threats = set()
        p1_temp, p2_temp = vertical_threat(npboard)
        p1_threats.update(p1_temp)
        p2_threats.update(p2_temp)
        p1_temp, p2_temp = horizontal_threat(npboard)
        p1_threats.update(p1_temp)
        p2_threats.update(p2_temp)
        p1_temp, p2_temp = diagonal_threat(npboard)
        p1_threats.update(p1_temp)
        p2_threats.update(p2_temp)

        # Remove bad threats
        p1_threats, p2_threats = remove_bad_threats(p1_threats, p2_threats)

        return self.player_id_compensation*(
            (
            get_threat_score(p1_threats, p2_threats) +
            central_heuristic(board)/10
        ))


def vertical_threat(board_array):
    """Function to find vertical threats for each player
    """
    h, w = board_array.shape
    p1_threats = set()
    p2_threats = set()

    mask = np.array([0, 1, 1, 1])

    for c in range(w):
        for r in range(h-3):
            if (board_array[r:r+4, c] == mask).all():
                p1_threats.add((r, c))
            elif (board_array[r:r+4, c] == 2*mask).all():
                p2_threats.add((r, c))
    return p1_threats, p2_threats


def horizontal_threat(board_array):
    """Function to find horizontal threats for each player
    """
    h, w = board_array.shape
    p1_threats = set()
    p2_threats = set()
    masks = [np.array([0,1,1,1]),
             np.array([1,0,1,1]),
             np.array([1,1,0,1]),
             np.array([1,1,1,0])]


    for c in range(w-3):
        for r in range(h):
            board_slice = board_array[r, c:c+4]
            for index, mask in enumerate(masks):
                if (board_slice == mask).all():
                    p1_threats.add((r, c+index))
                elif (board_slice == 2*mask).all():
                    p2_threats.add((r, c+index))
    return p1_threats, p2_threats


def diagonal_threat(board_array):
    """Function to find diagonal_threats for each player
    """
    h, w = board_array.shape
    p1_threats = set()
    p2_threats = set()

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
                            p1_threats.add((r+index, c+(3-index)))
                        else:
                            p1_threats.add((r+index, c+index))
                    elif (board_slice == 2*mask).all():
                        if positive_slope:
                            p2_threats.add((r+index, c+(3-index)))
                        else:
                            p2_threats.add((r+index, c+index))
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


def remove_bad_threats(p1_threats, p2_threats):
    """Function to remove bad threats from the threat sets
    """
    for r, c in p1_threats:
        # Remove any oposition threat 1 position above as it is redundant
        p2_threats.discard((r-1, c))

    for r, c in p2_threats:
        # Remove any oposition threat 1 position above as it is redundant
        p1_threats.discard((r-1, c))

    return p1_threats, p2_threats


def get_threat_score(p1, p2):
    """ Function to evaluate the score for the boards threats
    Threats that exist at lower levels of the board should score higher
    Threats by player 1 should score higher if made on odd rows,
    Threats by player 2 should score higher if make on even rows
    """
    score = 0

    for r, c in p1:
        if (6-r)%2:
            # Odd threat
            score += 1.3*r
        else:
            # Even threat
            score += 1*r

    for r, c in p2:
        if (6-r)%2:
            # Odd threat
            score -= 1*r
        else:
            # Even threat
            score -= 1.3*r

    return score
