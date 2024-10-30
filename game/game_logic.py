from chess_piece import ChessPiece
from chess_board import ChessBoard


def is_in_board(x, y):
    return 0 <= x <= 9 and 0 <= y <= 8


# 判断落点是否在黑方九宫格里
def is_in_black_barrack(x, y):
    return 7 <= x <= 9 and 3 <= y <= 5


# 判断落点是否在黑方九宫格里
def is_in_red_barrack(x, y):
    return 0 <= x <= 2 and 3 <= y <= 5


# 判断落点是否在红方
def is_in_red(x, y):
    return 0 <= x <= 4 and 0 <= y <= 8


# 判断落点是否在黑方
def is_in_black(x, y):
    return 5 <= x <= 9 and 0 <= y <= 8


class GameLogic:
    def __init__(self, board):
        self.board = board

    def could_eat(self, x, y, piece):
        if self.board.board[x][y] is not None:
            if self.board.board[x][y].color == piece.color:  # 颜色相等则不可以吃，不把他加入目标队列
                return False
        return True

    # 所有棋子的基础移动逻辑
    def piece_logic(self, piece):
        new_position = []

        # 兵的移动逻辑
        if piece.name == "兵":
            if piece.position[0] <= 4:
                if self.could_eat(piece.position[0] + 1, piece.position[1], piece):  # 检测目标点上有棋子时是否可以吞噬
                    new_position.append([piece.position[0] + 1, piece.position[1]])
            elif piece.position[0] <= 8:
                dst = [piece.position[0], piece.position[1] + 1]
                if is_in_board(dst[0], dst[1]):
                    if self.could_eat(dst[0], dst[1], piece):
                        new_position.append(dst)
                dst = [piece.position[0], piece.position[1] - 1]
                if is_in_board(dst[0], dst[1]):
                    if self.could_eat(dst[0], dst[1], piece):
                        new_position.append(dst)
                if self.could_eat(piece.position[0] + 1, piece.position[1], piece):
                    new_position.append([piece.position[0] + 1, piece.position[1]])
            else:
                if piece.position[1] + 1 <= 8:
                    if self.could_eat(piece.position[0], piece.position[1] + 1, piece):
                        new_position.append([piece.position[0], piece.position[1] + 1])
                if piece.position[1] - 1 >= 0:
                    if self.could_eat(piece.position[0], piece.position[1] - 1, piece):
                        new_position.append([piece.position[0], piece.position[1] - 1])
        # 卒的移动逻辑
        if piece.name == "卒":
            if piece.position[0] >= 5:
                if self.could_eat(piece.position[0] - 1, piece.position[1], piece):  # 检测目标点上有棋子时是否可以吞噬
                    new_position.append([piece.position[0] - 1, piece.position[1]])
            elif piece.position[0] >= 1:
                dst = [piece.position[0], piece.position[1] + 1]
                if is_in_board(dst[0], dst[1]):
                    if self.could_eat(dst[0], dst[1], piece):
                        new_position.append(dst)
                dst = [piece.position[0], piece.position[1] - 1]
                if is_in_board(dst[0], dst[1]):
                    if self.could_eat(dst[0], dst[1], piece):
                        new_position.append(dst)
                if self.could_eat(piece.position[0] - 1, piece.position[1], piece):
                    new_position.append([piece.position[0] - 1, piece.position[1]])
            else:
                if piece.position[1] + 1 <= 8:
                    if self.could_eat(piece.position[0], piece.position[1] + 1, piece):
                        new_position.append([piece.position[0], piece.position[1] + 1])
                if piece.position[1] - 1 >= 0:
                    if self.could_eat(piece.position[0], piece.position[1] - 1, piece):
                        new_position.append([piece.position[0], piece.position[1] - 1])
        # 車的移动逻辑
        if piece.name == "車":
            # 纵向移动逻辑
            for i in range(0, 10):
                # 如果是原来車所在的点则跳过
                if i == piece.position[0]:
                    continue
                # 创建一个目标队列，存储目标格的坐标
                dst = [i, piece.position[1]]

                # 判断棋子移动是否被阻拦的算法
                # 设置起点和终点，便于遍历
                minx, maxx = min(i, piece.position[0]), max(i, piece.position[0])
                # 后续检测是否有障碍物，如果有障碍物就不把目标格加入目标队列
                barrier = 0
                # 遍历检查起点和终点之间是否有障碍物，如果有则记录
                for n in range(minx + 1, maxx):
                    if self.board.board[n][dst[1]] is not None:
                        barrier = self.board.board[n][dst[1]]
                        break
                if barrier:
                    continue

                # 检查终点在有棋子的情况下，是否可以吃掉
                if not self.could_eat(i, dst[1], piece):
                    continue
                # 得到纵向目标队列
                new_position.append(dst)

            # 横向移动逻辑，和纵向同理
            for j in range(0, 9):
                # 如果是原来車所在的点则跳过
                if j == piece.position[1]:
                    continue
                # 创建一个目标队列，存储目标格的坐标
                dst = [piece.position[0], j]

                # 判断棋子移动是否被阻拦的算法
                # 设置起点和终点，便于遍历
                minx, maxx = min(j, piece.position[1]), max(j, piece.position[1])
                # 后续检测是否有障碍物，如果有障碍物就不把目标格加入目标队列
                barrier = 0
                # 遍历检查起点和终点之间是否有障碍物，如果有则记录
                for n in range(minx + 1, maxx):
                    if self.board.board[dst[0]][n] is not None:
                        barrier = self.board.board[dst[0]][n]
                        break
                if barrier:
                    continue

                # 检查终点在有棋子的情况下，是否可以吃掉
                if not self.could_eat(dst[0], j, piece):
                    continue

                # 得到横向目标队列
                new_position.append(dst)
        # 相的移动逻辑
        if piece.name == "相":
            # 相和象的移动方向和障碍所在方向
            movs = [[2, 2], [2, -2], [-2, 2], [-2, -2]]
            obstacle = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
            for i in range(len(movs)):
                if is_in_red(piece.position[0] + movs[i][0], piece.position[1] + movs[i][1]):
                    if self.board.board[piece.position[0] + obstacle[i][0]][piece.position[1] + obstacle[i][1]] is None:
                        if self.could_eat(piece.position[0] + movs[i][0], piece.position[1] + movs[i][1], piece):
                            new_position.append([piece.position[0] + movs[i][0], piece.position[1] + movs[i][1]])
        # 象的移动逻辑
        if piece.name == "象":
            # 相和象的移动方向和障碍所在方向
            movs = [[2, 2], [2, -2], [-2, 2], [-2, -2]]
            obstacle = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
            for i in range(len(movs)):
                if is_in_black(piece.position[0] + movs[i][0], piece.position[1] + movs[i][1]):
                    if self.board.board[piece.position[0] + obstacle[i][0]][piece.position[1] + obstacle[i][1]] is None:
                        if self.could_eat(piece.position[0] + movs[i][0], piece.position[1] + movs[i][1], piece):
                            new_position.append([piece.position[0] + movs[i][0], piece.position[1] + movs[i][1]])
        # 馬的移动逻辑
        if piece.name == "馬":
            # 馬的移动方向和障碍所在方向
            movs = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [-1, 2], [1, -2], [-1, -2]]
            obstacle = [[1, 0], [-1, 0], [0, 1], [0, -1]]
            for i in range(len(movs)):
                if is_in_board(piece.position[0] + movs[i][0], piece.position[1] + movs[i][1]):
                    if self.board.board[piece.position[0] + obstacle[i // 2][0]][
                        piece.position[1] + obstacle[i // 2][1]] is None:
                        if self.could_eat(piece.position[0] + movs[i][0], piece.position[1] + movs[i][1], piece):
                            new_position.append([piece.position[0] + movs[i][0], piece.position[1] + movs[i][1]])
        # 将的移动逻辑
        if piece.name == "帅":
            movs = [[0, 1], [0, -1], [-1, 0], [1, 0]]
            for mov in movs:
                if is_in_red_barrack(piece.position[0] + mov[0], piece.position[1] + mov[1]):
                    if self.could_eat(piece.position[0] + mov[0], piece.position[1] + mov[1], piece):
                        new_position.append([piece.position[0] + mov[0], piece.position[1] + mov[1]])
        # 将的移动逻辑
        if piece.name == "将":
            movs = [[0, 1], [0, -1], [-1, 0], [1, 0]]
            for mov in movs:
                if is_in_black_barrack(piece.position[0] + mov[0], piece.position[1] + mov[1]):
                    if self.could_eat(piece.position[0] + mov[0], piece.position[1] + mov[1], piece):
                        new_position.append([piece.position[0] + mov[0], piece.position[1] + mov[1]])
        # 仕的移动逻辑
        if piece.name == "仕":
            movs = [[1, 1], [-1, -1], [-1, 1], [1, -1]]
            for mov in movs:
                if is_in_red_barrack(piece.position[0] + mov[0], piece.position[1] + mov[1]):
                    if self.could_eat(piece.position[0] + mov[0], piece.position[1] + mov[1], piece):
                        new_position.append([piece.position[0] + mov[0], piece.position[1] + mov[1]])
        # 士的移动逻辑
        if piece.name == "士":
            movs = [[1, 1], [-1, -1], [-1, 1], [1, -1]]
            for mov in movs:
                if is_in_black_barrack(piece.position[0] + mov[0], piece.position[1] + mov[1]):
                    if self.could_eat(piece.position[0] + mov[0], piece.position[1] + mov[1], piece):
                        new_position.append([piece.position[0] + mov[0], piece.position[1] + mov[1]])
        # 炮和砲的移动逻辑
        if piece.name == "砲" or piece.name == "炮":
            # 纵向移动逻辑
            for i in range(0, 10):
                # 如果是原来炮或者砲所在的点则跳过
                if i == piece.position[0]:
                    continue
                # 创建一个目标队列，存储目标格的坐标
                dst = [i, piece.position[1]]

                # 检查是否可以翻过其他棋子吃掉敌方，区别于車的代码的部分
                # 先考虑目标点相同颜色棋子或者无棋子的情况
                if not self.could_eat(dst[0], dst[1], piece) or self.board.board[dst[0]][dst[1]] is None:
                    # 判断棋子移动是否被阻拦的算法
                    # 设置起点和终点，便于遍历
                    minx, maxx = min(i, piece.position[0]), max(i, piece.position[0])
                    # 后续检测是否有障碍物，如果有障碍物就不把目标格加入目标队列
                    barrier = 0
                    # 遍历检查起点和终点之间是否有障碍物，如果有则记录
                    for n in range(minx + 1, maxx):
                        if self.board.board[n][dst[1]] is not None:
                            barrier = self.board.board[n][dst[1]]
                            break
                    if self.board.board[dst[0]][dst[1]] is not None:
                        continue
                    if barrier:
                        continue
                else:  # 目标点有敌方棋子，判断是否可以吃掉
                    minx, maxx = min(i, piece.position[0]), max(i, piece.position[0])
                    # 后续检测是否有障碍物，如果有障碍物就不把目标格加入目标队列
                    barriers = []
                    # 遍历检查起点和终点之间是否有障碍物，如果有则记录
                    for n in range(minx + 1, maxx):
                        if self.board.board[n][dst[1]] is not None:
                            barrier = self.board.board[n][dst[1]]
                            barriers.append(barrier)
                    if len(barriers) != 1:
                        continue

                # 得到纵向目标队列
                new_position.append(dst)

            # 横向移动逻辑，和纵向同理
            for j in range(0, 9):
                # 如果是原来炮或者砲所在的点则跳过
                if j == piece.position[1]:
                    continue
                # 创建一个目标队列，存储目标格的坐标
                dst = [piece.position[0], j]

                # 检查是否可以翻过其他棋子吃掉敌方，区别于車的代码的部分
                # 先考虑目标点相同颜色棋子或者无棋子的情况
                if not self.could_eat(dst[0], dst[1], piece) or self.board.board[dst[0]][dst[1]] is None:
                    # 判断棋子移动是否被阻拦的算法
                    # 设置起点和终点，便于遍历
                    minx, maxx = min(j, piece.position[1]), max(j, piece.position[1])
                    # 后续检测是否有障碍物，如果有障碍物就不把目标格加入目标队列
                    barrier = 0
                    # 遍历检查起点和终点之间是否有障碍物，如果有则记录
                    for n in range(minx + 1, maxx):
                        if self.board.board[dst[0]][n] is not None:
                            barrier = self.board.board[dst[0]][n]
                            break
                    if self.board.board[dst[0]][dst[1]] is not None:
                        continue
                    if barrier:
                        continue
                else:  # 目标点有敌方棋子，判断是否可以吃掉
                    minx, maxx = min(j, piece.position[1]), max(j, piece.position[1])
                    # 检测要吃的目标棋子和起点中间有几个障碍物，设置barriers队列记录
                    barriers = []
                    # 遍历检查起点和终点之间是否有障碍物，如果有则记录
                    for n in range(minx + 1, maxx):
                        if self.board.board[dst[0]][n] is not None:
                            barrier = self.board.board[dst[0]][n]
                            barriers.append(barrier)
                    if len(barriers) != 1:
                        continue

                # 得到横向目标队列
                new_position.append(dst)
        # 打印目标队列
        return new_position

    #
    # def is_check_after_move(self, piece, new_position):
    #     # 判断移动是否会导致己方将军
    #     # 暂时模拟移动
    #     return False
    #
    #  检查该位置上的棋子是否会被吃掉，如果为将或者帅则说明出现将军的情况
    def checkmated(self, piece):
        #  遍历所有对方棋子，判断自己是否在对方可前进的路线上
        loc = [piece.position[0], piece.position[1]]
        for i in range(10):
            for j in range(9):
                pie = self.board.board[i][j]
                if pie:
                    if loc in self.piece_logic(pie):
                        return 1
        return 0

    # def check_win(self):
    #     # 判断胜负
    #     pass
# board = ChessBoard()
# print(board.board[0][1].name)
# gl = GameLogic(board)
# gl.checkmated(board.board[0][1])
