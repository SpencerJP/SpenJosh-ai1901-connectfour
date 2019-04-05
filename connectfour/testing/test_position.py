from connectfour.agents.agent_student import StudentAgent
from connectfour.board import Board

import time

boards = [(
 "0012111"
 "0022122"
 "0012211" #just a test
 "0021122"
 "1112211"
 "2221122"),
("0012211"
 "0011122"
 "1112211" #should result in (1,1)
 "2221122"
 "1112211"
 "2221122"),
 ("0012211"
  "0021122"
  "1112211" #should result in (1,0)
  "1221122"
  "1112211"
  "2221122"),
  ("1200011"
   "2100022"
   "1100011" #should result in (1,0)
   "1221122"
   "1112211"
   "2221122"))]

expected_values = ["?", (1,1), (1,0)]


def debug_print_board(boardclass):
    string = ""
    for row in boardclass.board:
        for cell in row:
            string += str(cell)
        string += str("\n")
    print(string)

def convertStringToBoard(s, boardclass):
    row = 0
    col = 0
    string = ""
    for character in s:
        if(col == 7):
            row = row + 1
            col = 0
            boardclass.board[row][col] = int(character)
            col = col + 1
        else:
            boardclass.board[row][col] = int(character)
            col = col + 1

def main():
    gameboard = Board(height=6,width=7)
    i = 0
    for position in boards:
            convertStringToBoard(position, gameboard)
            agent = StudentAgent(str(i))
            start = time.time()
            result = agent.get_move(gameboard)
            end = time.time()
            print("Position no: %d, Result Move: (%d, %d), Time taken: %d" % (i, result[0], result[1], (end - start)))
            if (expected_values[i] == "?" or expected_values[i] == result):
                print("Success!")
            else:
                print("Failure")
            i = i + 1


main()
