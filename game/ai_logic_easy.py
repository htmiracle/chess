import random
from chess_board import ChessBoard
from game_logic import GameLogic


class AILogicEasy:
    def __init__(self, board):
        self.board = board

    def random_piece(self, turn):
        choosing = 1
        while choosing:
            x = random.randint(0, 9)
            y = random.randint(0, 8)
            if self.board.board[x][y]:
                if self.board.board[x][y].color == "red":
                    print([x, y])
                    print(self.board.board[x][y].name)
                    break
        return x, y

    # 预测返回值为一个坐标
    def easy_ai_run(self):
        gamelogic = GameLogic(self.board)
        chess_board = self.board.board
        end_position = gamelogic.piece_logic
        while 1:
            start_x, start_y = self.random_piece(0)
            end_pos = end_position(chess_board[start_x][start_y])
            if end_pos:
                break
        end = random.choice(end_pos)
        print(end_pos)
        return start_x, start_y, end[0], end[1]


ai = AILogicEasy(ChessBoard())
ai.easy_ai_run()

ads = random.choice([1,2,3])
print(ads)
