from connectfour.agents.agent_student import StudentAgent
from connectfour.board import Board

import time

boards = [("0001221"
           "1002121"
           "2001212" #(2,2), 1's turn https://i.imgur.com/IXoqPJq.png
           "1022211"
           "1021122"
           "1021211"),
           ("0000000"
              "0000000"
              "0000000" #(2,2), 1's turn https://i.imgur.com/IXoqPJq.png
              "0010000"
              "0010000"
              "0010000"),
               ("0000000"
                "0000000"
                "0000000" #(2,2), 1's turn https://i.imgur.com/IXoqPJq.png
                "0020000"
                "0020000"
                "0020000"),
          ("0000000"
         "1000000"
         "2000000" #(2,2), 1's turn https://i.imgur.com/IXoqPJq.png
         "1020000"
         "1020000"
         "1020000"),
            ("0000000"
            "0000000"
            "0000000" #(2,2), 1's turn https://i.imgur.com/IXoqPJq.png
            "0010000"
            "0020000"
            "0010000"),

            ("0022212"
             "0011121"
             "0022212" #expected (2,1), current turn is 1 https://i.imgur.com/y2Kpq0C.png  left column = -3 right column = 0
             "2211121"
             "1122212"
             "2211121"),
            ("0012211"
             "0011122"
             "2112211" #should result in (1,1), current turn is 1 https://i.imgur.com/N9yD8DF.png, left column = 0, right column = 2
             "2221122"
             "1112211"
             "2221122"),
             ("0012211"
              "0021122"
              "1212211" #should result in (1,0), current turn is 1
              "1221122"
              "1112211"
              "2221122"),
              ("1200021"
              "1200012"
              "2120021"
              "1221221" #should result in (2,4), left=-1,middle=-1,right=1
              "2112112"
              "1221221")]


expected_values = [(2,2), (2,2), (2,2), "?", (2,2), (2,1), (1,1), (1,0), (2,4)]

# expected_values = [(2, 2)]


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
            result = agent.get_move(gameboard)
            print("Position no: %d, Result Move: (%d, %d)" % (i, result[0], result[1]))
            if (expected_values[i] == "?" or expected_values[i] == result):
                print("Success!")
            else:
                print("Failure")
            i = i + 1


main()
