@ECHO OFF
pipenv run python -m connectfour.game --player-one StudentAgent --player-two HumanPlayer --fast
PAUSE