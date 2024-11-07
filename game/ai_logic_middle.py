import random
from chess_board import ChessBoard
from game_logic import GameLogic

class SimpleChessAI:
    def __init__(self, board):
        self.board = board

    def get_valid_moves(self, piece, x, y):
        GameLogic(self.board)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        valid_moves = []

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 10 and 0 <= new_y < 9:
                # 检查目标位置是否为空或者是敌方棋子
                target_piece = self.board[new_x][new_y]
                if target_piece is None or target_piece.color != piece.color:
                    valid_moves.append((new_x, new_y))

        return valid_moves

    def evaluate_board(self):
        score = 0
        for i in range(10):
            for j in range(9):
                piece = self.board[i][j]
                if piece is not None:
                    if piece.color == 'red':
                        score += piece.value
                    else:
                        score -= piece.value
        return score

    def select_best_move(self):
        best_move = None
        best_score = float('-inf')

        # 遍历所有棋子，尝试找到最佳移动
        for i in range(10):
            for j in range(9):
                piece = self.board[i][j]
                if piece is not None and piece.color == 'red':  # 假设AI控制红方
                    valid_moves = self.get_valid_moves(piece, i, j)
                    for move in valid_moves:
                        new_x, new_y = move
                        # 进行试探性移动
                        original_piece = self.board[new_x][new_y]
                        self.board[new_x][new_y] = piece
                        self.board[i][j] = None

                        # 评估移动后的棋盘得分
                        score = self.evaluate_board()

                        # 如果该移动得分更高，则更新最佳移动
                        if score > best_score:
                            best_score = score
                            best_move = ((i, j), (new_x, new_y))

                        # 撤销试探性移动
                        self.board[i][j] = piece
                        self.board[new_x][new_y] = original_piece

        # 如果找不到最佳移动，则随机选择一个有效移动
        if best_move is None:
            all_valid_moves = []
            for i in range(10):
                for j in range(9):
                    piece = self.board[i][j]
                    if piece is not None and piece.color == 'red':
                        valid_moves = self.get_valid_moves(piece, i, j)
                        for move in valid_moves:
                            all_valid_moves.append(((i, j), move))
            if all_valid_moves:
                best_move = random.choice(all_valid_moves)

        return best_move

    def make_move(self):
        best_move = self.select_best_move()
        if best_move is not None:
            (start_x, start_y), (end_x, end_y) = best_move
            return (start_x, start_y), (end_x, end_y)
        else:
            return None

