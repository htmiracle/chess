import random
from chess_board import ChessBoard
from game_logic import GameLogic


def merge_lists(list1, list2):
    merged_list = list1.copy()  # 先复制第一个列表

    for item in list2:
        if item not in merged_list:
            merged_list.append(item)  # 如果元素不在合并后的列表中，则添加

    return merged_list


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
                    break
        return x, y

    # 检查当前棋盘被队友保护的位置
    def protect_pos(self, end_position):
        protect_pos = []
        for row in range(10):
            for col in range(9):
                if self.board.board[row][col]:
                    if self.board.board[row][col].color == "red":
                        if self.board.board[row][col].name == "炮":
                            end_pos = end_position(self.board.board[row][col])
                            for end in end_pos:
                                if self.board.board[end[0]][end[1]]:
                                    protect_pos = merge_lists(protect_pos, [end])
                        else:
                            end_pos = end_position(self.board.board[row][col])
                            protect_pos = merge_lists(protect_pos, end_pos)
        return protect_pos

    def danger_pos(self, end_position):
        danger_pos = []
        for row in range(10):
            for col in range(9):
                if self.board.board[row][col]:
                    if self.board.board[row][col].color == "black":
                        if self.board.board[row][col].name == "砲":
                            end_pos = end_position(self.board.board[row][col])
                            for end in end_pos:
                                if self.board.board[end[0]][end[1]]:
                                    danger_pos = merge_lists(danger_pos, [end])
                        else:
                            end_pos = end_position(self.board.board[row][col])
                            danger_pos = merge_lists(danger_pos, end_pos)
        return danger_pos

    # 检查假设移动后的棋盘的危险位置
    def danger_after_move(self, end_position, danger_pos, x, y, row, col):
        self.board.board[x][y], temp_piece = self.board.board[row][col], self.board.board[x][y]
        self.board.board[row][col] = None
        self.board.board[x][y].position = [x, y]
        danger_des = self.danger_pos(end_position)
        danger_pos = merge_lists(danger_pos, danger_des)
        self.board.board[row][col] = self.board.board[x][y]
        self.board.board[row][col].position = [row, col]
        self.board.board[x][y] = temp_piece
        return danger_pos

    def is_protect_red(self, x, y, end_position):
        if self.board.board[x][y].color == "red":
            self.board.board[x][y].color = "black"
            protect_pos = self.protect_pos(end_position)
            if [x, y] in protect_pos:
                self.board.board[x][y].color = "red"
                return True
            self.board.board[x][y].color = "red"
        return False

    def is_protect_black(self, x, y, end_position):
        if self.board.board[x][y].color == "black":
            self.board.board[x][y].color = "red"
            danger_pos = self.danger_pos(end_position)
            if [x, y] in danger_pos:
                self.board.board[x][y].color = "black"
                return True
            self.board.board[x][y].color = "black"
        return False

    # 检查该位置的棋子是否被威胁
    def is_threatened(self, danger_pos, end_position):
        for row in range(10):
            for col in range(9):
                if self.board.board[row][col]:
                    if self.is_protect_red(row, col, end_position) and self.board.board[row][col].name != "帅":
                        continue
                    # 挑选ai方的棋子
                    if self.board.board[row][col].color == "red":
                        if [row, col] in danger_pos:
                            end_pos = end_position(self.board.board[row][col])
                            for x, y in end_pos:
                                danger_pos = self.danger_after_move(end_position, danger_pos, x, y, row, col)
                                if [x, y] not in danger_pos:
                                    return self.board.board[row][col], [x, y]
        return None

    def eat_black(self, danger_pos, end_position):
        for row in range(10):
            for col in range(9):
                if self.board.board[row][col]:
                    if self.board.board[row][col].color == "red":
                        end_pos = end_position(self.board.board[row][col])
                        for end in end_pos:
                            if self.board.board[end[0]][end[1]]:
                                if self.board.board[end[0]][end[1]].name == "将":
                                    return self.board.board[row][col], end
        for row in range(10):
            for col in range(9):
                if self.board.board[row][col]:
                    if self.board.board[row][col].color == "red":
                        end_pos = end_position(self.board.board[row][col])
                        for end in end_pos:
                            if self.board.board[end[0]][end[1]]:
                                if self.board.board[end[0]][end[1]].name == "将":
                                    return self.board.board[row][col], end
                                if self.is_protect_black(end[0], end[1], end_position):
                                    continue
                                return self.board.board[row][col], end
        return



    # 预测返回值为一个坐标
    def easy_ai_run(self):
        gamelogic = GameLogic(self.board)
        chess_board = self.board.board
        end_position = gamelogic.piece_logic
        danger_des = self.danger_pos(end_position)

        ate = False
        for col in range(3, 6):
            for row in range(0, 3):
                if chess_board[row][col]:
                    if chess_board[row][col].name == "帅":
                        if [row, col] in danger_des:
                            x, y = row, col
                            ate = True
        if ate:
            print("king_defend")
            for row in range(10):
                for col in range(9):
                    if chess_board[row][col]:
                        if chess_board[row][col].color == "red":
                            end_pos = end_position(chess_board[row][col])
                            for end in end_pos:
                                danger_des = self.danger_after_move(end_position, [], end[0], end[1], row, col)
                                if chess_board[row][col].name == "帅":
                                    if chess_board[end[0]][end[1]]:
                                        if chess_board[end[0]][end[1]].name == "将":
                                            return row, col, end[0], end[1]
                                    if [end[0], end[1]] not in danger_des:
                                        print([end[0], end[1]])
                                        return row, col, end[0], end[1]
                                else:
                                    if [x, y] not in danger_des:
                                        return row, col, end[0], end[1]
        cant_move = False
        # 优先进行进攻吃子策略
        if self.eat_black(danger_des, end_position):
            print("attack")
            pos, end = self.eat_black(danger_des, end_position)
            start_x, start_y = pos.position[0], pos.position[1]
            if chess_board[end[0]][end[1]].name == "将":
                return start_x, start_y, end[0], end[1]
            # 检查吃子后是否会导致被将军
            danger_des = self.danger_after_move(end_position, [], end[0], end[1], start_x, start_y)
            for col in range(3, 6):
                for row in range(0, 3):
                    if chess_board[row][col]:
                        if chess_board[row][col].name == "帅":
                            if [row, col] in danger_des:
                                cant_move = True
        # 无可吃子时防守
        elif self.is_threatened(danger_des, end_position):
            print("defend")
            pos, end = self.is_threatened(danger_des, end_position)
            start_x, start_y = pos.position[0], pos.position[1]
            # 检查逃跑后是否会导致被将军
            danger_des = self.danger_after_move(end_position, [], end[0], end[1], start_x, start_y)
            for col in range(3, 6):
                for row in range(0, 3):
                    if chess_board[row][col]:
                        if chess_board[row][col].name == "帅":
                            if [row, col] in danger_des:
                                cant_move = True
        # 随机挑选一个棋子进行移动
        else:
            print("random")
            nm = 1000
            while nm > 0:
                nm -= 1
                start_x, start_y = self.random_piece(0)
                end_pos = end_position(chess_board[start_x][start_y])
                if not end_pos:
                    continue
                end = random.choice(end_pos)
                danger_pos = self.danger_pos(end_position)
                danger_des = self.danger_after_move(end_position, [], end[0], end[1], start_x, start_y)
                danger = False
                ate = False
                for col in range(3, 6):
                    for row in range(0, 3):
                        if chess_board[row][col]:
                            if chess_board[row][col].name == "帅":
                                if [row, col] in danger_des:
                                    danger = True
                                if [row, col] in danger_pos:
                                    ate = True
                if danger:
                    continue
                else:
                    if end in danger_des and not ate:
                        continue
                    if end_pos:
                        break

        if cant_move:
            print("random")
            nm = 3000
            while nm > 0:
                nm -= 1
                start_x, start_y = self.random_piece(0)
                end_pos = end_position(chess_board[start_x][start_y])
                if not end_pos:
                    continue
                end = random.choice(end_pos)
                danger_pos = self.danger_pos(end_position)
                danger_des = self.danger_after_move(end_position, [], end[0], end[1], start_x, start_y)
                danger = False
                ate = False
                for col in range(3, 6):
                    for row in range(0, 3):
                        if chess_board[row][col]:
                            if chess_board[row][col].name == "帅":
                                if [row, col] in danger_des:
                                    danger = True
                                if [row, col] in danger_pos:
                                    ate = True
                if danger:
                    continue
                else:
                    if end in danger_des and not ate:
                        continue
                    if end_pos:
                        break
        return start_x, start_y, end[0], end[1]

# ai = AILogicEasy(ChessBoard())
# ai.easy_ai_run()
