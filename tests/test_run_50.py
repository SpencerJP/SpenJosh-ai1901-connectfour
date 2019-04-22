import time
from connectfour.game import Game
from connectfour.agents.agent_student import StudentAgent
from connectfour.agents.agent_heuristic import JoshAgent
from connectfour.agents.computer_player import MonteCarloAgent, RandomAgent
from connectfour.ui import start_game


"""This is only designed to work in the testing branch"""

def debug_print_board(boardclass):
    string = ""
    for row in boardclass.board:
        for cell in row:
            string += str(cell)
        string += str("\n")
    print(string)

def main():
    #test_randomagent(2)
    #test_montecarlo(2)
    test_joshagent(2)


def test_randomagent(games=30):
    winsum = 0
    i = 0
    while(i != games):
        full_time_start = time.time()
        if (i == 0 or i % 2 == 0):
            print("Game %d" % i)
            game_time_start = time.time()
            g = Game(
                StudentAgent("StudentAgent 1"),
                RandomAgent("RandomAgent 2"),
                6,
                7,
                True,
                True
            )
            g.player_one.debug = False

            result = start_game(g, graphics=(False))
            debug_print_board(g.board)
            game_time_end = time.time()
            print("Game %d took %r seconds to finish!" % (i, (game_time_end-game_time_start)))
            if(result[0] == 1):
                winsum += 1
                print("Win total: %d" % winsum)
            elif(result[0] == 3):
                print("Draw!")
            i += 1
        else:
            print("Game %d" % i)
            game_time_start = time.time()
            g = Game(
                RandomAgent("RandomAgent 1 "),
                StudentAgent("StudentAgent 2"),
                6,
                7,
                True,
                True
            )
            g.player_two.debug = False
            result = start_game(g, graphics=(False))
            debug_print_board(g.board)
            game_time_end = time.time()
            print("Game %d took %r seconds to finish!" % (i, (game_time_end-game_time_start)))
            if(result[0] == 2):
                winsum += 1
                print("Win total: %d" % winsum)
            elif(result[0] == 3):
                    print("Draw!")
            i += 1
        full_time_end = time.time()
        print("Win percentage: %dpercent - Took %d minutes, average turn time was %r seconds" % ( ((winsum/i) * 100), (full_time_end - full_time_start)/60, (full_time_end - full_time_start)/(result[1]/2) ) )


def test_montecarlo(games=30):
    full_time_start = time.time()
    winsum = 0
    i = 0
    while(i != games):
        if (i == 0 or i % 2 == 0):
            print("Game %d" % i)
            game_time_start = time.time()
            g = Game(
                StudentAgent("StudentAgent 1"),
                MonteCarloAgent("MonteCarloAgent 2"),
                6,
                7,
                True,
                True
            )
            g.player_one.debug = False

            result = start_game(g, graphics=(False))
            debug_print_board(g.board)
            game_time_end = time.time()
            print("Game %d took %r seconds to finish!" % (i, (game_time_end-game_time_start)))
            if(result[0] == 1):
                winsum += 1
                print("Win total: %d" % winsum)
            elif(result[0] == 3):
                print("Draw!")
            i += 1
        else:
            print("Game %d" % i)
            game_time_start = time.time()
            g = Game(
                MonteCarloAgent("MonteCarloAgent"),
                StudentAgent("StudentAgent"),
                6,
                7,
                True,
                True
            )
            g.player_two.debug = False
            result = start_game(g, graphics=(False))
            debug_print_board(g.board)
            game_time_end = time.time()
            print("Game %d took %r seconds to finish!" % (i, (game_time_end-game_time_start)))
            if(result[0] == 2):
                winsum += 1
                print("Win total: %d" % winsum)
            elif(result[0] == 3):
                print("Draw!")
            i += 1
        full_time_end = time.time()
        print("Win percentage: %dpercent - Took %d minutes, average turn time was %r seconds" % ( ((winsum/i) * 100), (full_time_end - full_time_start)/60, (full_time_end - full_time_start)/(result[1]/2) ) )

def test_joshagent(games=30):
    full_time_start = time.time()
    winsum = 0
    i = 0
    while(i != games):
        if (i == 0 or i % 2 == 0):
            print("Game %d" % i)
            game_time_start = time.time()
            g = Game(
                StudentAgent("StudentAgent 1"),
                JoshAgent("HeuristicAgent 2"),
                6,
                7,
                True,
                True
            )
            g.player_one.debug = False

            result = start_game(g, graphics=(False))
            debug_print_board(g.board)
            game_time_end = time.time()
            print("Game %d took %r seconds to finish!" % (i, (game_time_end-game_time_start)))
            if(result[0] == 1):
                winsum += 1
                print("Win total: %d" % winsum)
            elif(result[0] == 3):
                print("Draw!")
            i += 1
        else:
            print("Game %d" % i)
            game_time_start = time.time()
            g = Game(
                JoshAgent("HeuristicAgent 1"),
                StudentAgent("StudentAgent 2"),
                6,
                7,
                True,
                True
            )
            g.player_two.debug = False
            result = start_game(g, graphics=(False))
            debug_print_board(g.board)
            game_time_end = time.time()
            print("Game %d took %r seconds to finish!" % (i, (game_time_end-game_time_start)))
            if(result[0] == 2):
                winsum += 1
                print("Win total: %d" % winsum)
            elif(result[0] == 3):
                print("Draw!")
            i += 1
        full_time_end = time.time()
        print("Win percentage: %dpercent - Took %d minutes, average turn time was %r seconds" % ( ((winsum/i) * 100), (full_time_end - full_time_start)/60, (full_time_end - full_time_start)/(result[1]/2) ) )

main()
