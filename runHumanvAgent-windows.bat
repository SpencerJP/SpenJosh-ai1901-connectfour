@ECHO OFF
pipenv run python -m connectfour.game --player-one HumanPlayer --player-two StudentAgent --fast
PAUSE