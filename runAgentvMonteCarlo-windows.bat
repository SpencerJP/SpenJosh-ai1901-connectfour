@ECHO OFF
pipenv run python -m connectfour.game --player-one MonteCarloAgent --player-two StudentAgent --fast
PAUSE