"""Spencer and Josh's agent for playing Connect 4."""
import math
import time
from connectfour.agents.computer_player import RandomAgent


PLAYER_ONE_ID = 1
PLAYER_TWO_ID = 2

def get_current_player(num_moves):
    """Counts the moves and returns player 1 if move count is even, returns player 2 if odd"""
    if(num_moves % 2 == 0 or num_moves == 0):
        return PLAYER_ONE_ID
    return PLAYER_TWO_ID

def debug_print_board(board):
    """Prints out the board argument into the terminal, followed by a newline."""
    string = ""
    for row in board.board:
        for cell in row:
            string += str(cell)
        string += str("\n")
    print(string)

def count_moves(board):
    """counts the amount of tokens that have been inserted into the board."""
    sum_of_moves = 0
    for i in range(board.height):
        for j in range(board.width):
            if board.board[i][j] != 0:
                sum_of_moves += 1

    return sum_of_moves

def valid_non_losing_moves(board, num_moves):
    """
    returns: a generator of moves that don't cause a loss the turn after

    board: the node/game state to check
    num_moves: the amount of moves to get to this point
    """
    current_player = get_current_player(num_moves)
    other_player = get_current_player(num_moves+1)

    valid_moves = board.valid_moves()
    #loop through each move
    for move in valid_moves:
        my_move = board.next_state(current_player, move[1])
        winner_num = my_move.winner()
        #if we win then this is a valid move that won't cause us to lose,
        #and there is no reason to continue the search either.
        if winner_num != 0:
            yield move
            break
        enemy_valid_moves = my_move.valid_moves()
        failure = False
        #loop through the enemy's moves after our move.
        #if there is a single move that they can make in which they can win,
        #this whole move of ours is a bust, so don't yield it.
        for enemy_move in enemy_valid_moves:
            node_after = my_move.next_state(other_player, enemy_move[1])
            winner_num = node_after.winner()
            if winner_num != 0:
                failure = True
                break
        if not failure:
            yield move

def count_non_losing_moves(board, num_moves):
    """
    I made this method because I feel that that the
    count_non_losing_moves() generator method is inappropriate.
    returns: a sum of moves that don't cause an immediate loss

    board: the node/game state to check
    num_moves: the amount of moves to get to this point
    """
    current_player = get_current_player(num_moves)
    other_player = get_current_player(num_moves+1)

    valid_moves = board.valid_moves()
    sum_of_moves = 0
    #loop through each move
    for move in valid_moves:
        my_move = board.next_state(current_player, move[1])
        winner_num = my_move.winner()
        #if we win then this is a valid move that won't cause us to lose,
        #and there is no reason to continue the search either,
        #we can safely return one so that the algorithm continues.
        if winner_num != 0:
            return 1
        enemy_valid_moves = my_move.valid_moves()
        failure = False
        #loop through the enemy's moves after our move.
        #if there is a single move that they can make in which they can win,
        #this whole move of ours is a bust, so don't yield it.
        for enemy_move in enemy_valid_moves:
            node_after = my_move.next_state(other_player, enemy_move[1])
            winner_num = node_after.winner()
            if winner_num != 0:
                failure = True
                break

        if not failure:
            sum_of_moves += 1
    return sum_of_moves

 # pylint: disable=too-many-instance-attributes
class StudentAgent(RandomAgent):
    """Our agent class."""
    def __init__(self, name):
        super().__init__(name)
        self.max_depth = 4
        self.id = -1
        self.dimensions = -1
        self.enemy_id = -1
        self.debug = True
        self.transpos_table = {}
        self.middle_col = -1

    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """
        start = time.time()

        #check how many moves have occurred so far on this board.
        current_move_number = count_moves(board)

        #check board size
        if self.dimensions == -1:
            self.dimensions = board.width * board.height
            self.middle_col = round((board.width+1)/2)-1

        #variable depth to make the algorithm less slow
        #5 is a constant here because anything above that begins to go very slow.
        self.max_depth = min([int(math.sqrt(current_move_number)) + 1, 5])
        if current_move_number == 0:
            #hardcoded first move because there is no point calculating anything.
            return ((board.height-1), self.middle_col)


        #check which player this agent is going to be and set it (as in id, will be either 1 or 2)
        if self.id == -1:
            self.id = get_current_player(current_move_number)
            self.enemy_id = get_current_player(current_move_number+1)



        #get a generator of moves that will not cause this player to lose
        valid_moves = valid_non_losing_moves(board, current_move_number)

        vals = []
        moves = []

        for move in valid_moves:
            minimum = int(-(self.dimensions - current_move_number) / 2)

            maximum = int((self.dimensions + 1 - current_move_number) / 2)
            next_node = board.next_state(self.id, move[1])
            moves.append(move)

            #iterative deepening of the alpha/beta limits to prune alot of moves,
            #using a null depth window.
            while minimum < maximum:

                medium = int(minimum + (maximum - minimum) / 2)
                if(minimum / 2) < medium <= 0:
                    medium = minimum / 2
                elif(maximum / 2) > medium >= 0:
                    medium = maximum / 2
                result = -int(self.negamax(next_node, medium, medium + 1, current_move_number))
                if result <= medium:
                    maximum = result

                else:
                    minimum = result

            if self.debug:
                print("column number: %d, calculated value: %d" % (move[1]+1, minimum))
            vals.append(minimum)


        #check if there is at least 1 valid move that won't cause us to lose.
        #If not then we're guaranteed to lose so just pick the first one.
        if vals:
            best_move = moves[vals.index(max(vals))]
        else:
            valid_moves = board.valid_moves()
            best_move = next(valid_moves)

        next_node = board.next_state(self.id, best_move[1])

        end = time.time()
        print("Took %r seconds to make this move." % (end - start))

        if self.debug:
            print("Placed a piece in (%d, %d)" % (best_move[0], best_move[1]))
            debug_print_board(next_node)

        return best_move


    def negamax(self, board, alpha, beta, num_moves, sign=1, depth=0):
        """returns score of the board position

        board is the game state to evaluate.
        alpha is the alpha value for the current node

        beta is the beta value for the current node

        num_moves is the amount of moves that have been made so far.
        This is used in heuristic calculations as well
        as determining who's turn it is.

        sign is either 1 or -1 depending on whether board's
        last move is our agent's move or the enemy's.
        1 for our move, -1 for enemy move.

        depth is how deep our search has gone so far, beginning at 0 from get_move().
        """

        #check if this board has a winner and return if it does
        #this is the heuristic of our algorithm.
        #The number it returns is scored on how many moves
        #it would take to guarantee a victory for a perfect player.
        winner_num = board.winner()
        if winner_num != 0:
            if winner_num == self.id:
                return sign * -int((self.dimensions - num_moves) / 2)
            return sign * int((self.dimensions - num_moves) / 2)

        #detect a draw, once 40 tokens are on the board in a 6*7 game and no one has won already,
        #no one can possibly win now.
        if num_moves >= self.dimensions - 2:
            return 0

        # no valid moves that won't cause a loss, aka dead end
        sum_of_moves = count_non_losing_moves(board, num_moves)
        if sum_of_moves == 0:
            return sign * (self.dimensions - num_moves) / 2

        # set alpha to the minimum possible value
        minimum = int(-(self.dimensions - num_moves) / 2)
        if alpha < minimum:
            alpha = minimum
            if alpha >= beta:
                return alpha #prune children.

        # set beta to the maximum possible value
        maximum = int((self.dimensions - num_moves) / 2)
        if beta > maximum:
            beta = maximum
            if alpha >= beta:
                return beta  #prune children.

        #could include transposition or a lookup table for early game stuff here.

        if depth == self.max_depth:
            max_depthvalue = self.evaluate_board_state(board, num_moves)
            if max_depthvalue <= alpha:
                return alpha
            if max_depthvalue >= beta:
                return beta
            return max_depthvalue


        valid_moves = board.valid_moves()

        #set the value to the minimum possible
        value = minimum
        for move in valid_moves:
            next_node = board.next_state(get_current_player(num_moves+1), move[1])
            # recursively go through the children of this node.
            result = -self.negamax(next_node, -beta, -alpha, num_moves+1, -sign, depth + 1)

            #self.transpos_table[bytes(next_node)] = value

            #if the child node is the biggest so far, replace the previous biggest
            if result > value:
                value = result

            # if the result is bigger than the current minimum, set the minimum to the new result
            if result > alpha:
                alpha = result

            if alpha >= beta:
                #don't bother searching the remainder of the moves as this will be the best one
                break

        #pass up the value we found
        return value





    def evaluate_board_state(self, board, num_moves):

        """
        Your evaluation function should look at the current state and return a score for it.
        As an example, the random agent provided works as follows:
            If the opponent has won this game, return -1.
            If we have won the game, return 1.
            If neither of the players has won, return a random number.
        """

        """
        These are the variables and functions for board objects
         which may be helpful when creating your Agent.
        Look into board.py for more information/descriptions of each,
         or to look for any other definitions which may help you.

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

        score_sum = []
        for row in board.board:
            for col in range(board.width):
                if row[col] == get_current_player(num_moves):
                    score_sum.append(self.middle_col-abs(self.middle_col-col))

        score = sum(score_sum)
        return score
