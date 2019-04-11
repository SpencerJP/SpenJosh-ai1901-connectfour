import time
from connectfour.game import Game
from connectfour.agents.agent_student import StudentAgent
from connectfour.agents.computer_player import MonteCarloAgent
from connectfour.ui import start_game

def main():
    full_time_start = time.time()
    i = 0
    while(i != 30):
        if (i == 0 or i % 2 == 0):
            g = Game(
                StudentAgent("StudentAgent"),
                MonteCarloAgent("MonteCarlo"),
                6,
                7,
                True,
                True
            )
            start_game(g, graphics=(False))
            i += 1
        else:
            g = Game(
                MonteCarloAgent("MonteCarlo"),
                StudentAgent("StudentAgent"),
                6,
                7,
                True,
                True
            )
            start_game(g, graphics=(False))
            i += 1

main()
