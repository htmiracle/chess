from chess_board import ChessBoard
from game_logic import GameLogic


# 打印可以选中移动棋子后，它可以移动到的目标点
def print_access(end_pos, chess_board):
    for i in range(0, 10):
        for j in range(0, 9):
            if [i, j] in end_pos:
                print("十", end=" ")
            elif chess_board[i][j] is None:
                print("〇", end=" ")
            else:
                print(chess_board[i][j].name, end=" ")
        print()


def print_board(chess_board):
    for line in chess_board:
        for item in line:
            if item is None:
                print("〇", end=" ")
            else:
                print(item.name, end=" ")
        print()


def make_move(start_pos, end_pos, board):
    board[start_pos[0]][start_pos[1]], board[end_pos[0]][end_pos[1]] = None, board[start_pos[0]][start_pos[1]]
    board[end_pos[0]][end_pos[1]].position = [end_pos[0], end_pos[1]]
    return board


class GameManager:
    def __init__(self, player1, player2, board, logic):
        self.players = [player1, player2]
        self.current_turn = 0  # 0是红色方,1是黑色方
        self.board = board
        self.logic = logic

    #
    def run(self):
        running = True  # 棋盘正在运行
        gamelogic = GameLogic(self.board)  # 生成一个GameLogic的对象
        chess_board = self.board.board  # 初始化棋盘，存入chess_board里
        end_position = gamelogic.piece_logic  # 计算可落点的函数，传参为起点坐标

        while running:
            start_x, start_y = self.input_start(chess_board)
            end_pos = end_position(chess_board[start_x][start_y])
            if not end_pos:
                print("该棋子不可以移动")
                continue
            print_access(end_pos, chess_board)
            while 1:
                end_x, end_y = int(input("请输入终止格：\n")), int(input())
                if [end_x, end_y] in end_pos:
                    bd = make_move([start_x, start_y], [end_x, end_y], chess_board)
                    break
            print_board(bd)
            self.next_turn()

    def input_start(self, chess_board):
        inputing = True  # 正在输入起始点
        while inputing:
            if self.current_turn == 0:
                print("红方出棋")
            else:
                print("黑方出棋")
            start_x, start_y = int(input("请输入起始格：\n")), int(input())
            if not chess_board[start_x][start_y]:
                continue
            if self.current_turn == 0 and chess_board[start_x][start_y].color == "red":
                break
            if self.current_turn == 1 and chess_board[start_x][start_y].color == "black":
                break
        return start_x, start_y

    def next_turn(self):
        # 切换当前回合
        self.current_turn = 1 - self.current_turn

    def get_current_player(self):
        # 获取当前玩家
        return self.players[self.current_turn]

    def process_move(self, start_pos, end_pos):
        # 处理玩家移动请求
        current_player = self
        if current_player.make_move(start_pos, end_pos, self.board, self.logic):
            if self.logic.check_win():
                return f"{current_player.name} wins!"
            self.next_turn()
            return "Move successful"
        return "Invalid move"


gamemannager = GameManager(1, 2, ChessBoard(), GameLogic(ChessBoard()))
gamemannager.run()
