@ECHO OFF
pipenv run python -m cProfile -o output.profile C:\Users\Spencer\Documents\GitHub\SpenJoshAI\connectfour\game.py --player-one HumanPlayer --player-two StudentAgent --fast
PAUSE