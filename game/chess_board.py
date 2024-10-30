from chess_piece import ChessPiece
import copy

maps = [["〇" for _ in range(9)] for _ in range(10)]


class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(9)] for _ in range(10)]
        self.initialize_pieces()
        self.history = []  # 用于存储撤销操作的历史记录

    # 棋盘初始化
    def initialize_pieces(self):
        self.board = [[None for _ in range(9)] for _ in range(10)]
        # 初始化双方棋子的起始位置
        pieces_red = [
            ("車", [(0, 0), (0, 8)]),
            ("馬", [(0, 1), (0, 7)]),
            ("相", [(0, 2), (0, 6)]),
            ("仕", [(0, 3), (0, 5)]),
            ("帅", [(0, 4)]),
            ("炮", [(2, 1), (2, 7)]),
            ("兵", [(3, 0), (3, 2), (3, 4), (3, 6), (3, 8)])
        ]

        pieces_black = [
            ("車", [(9, 0), (9, 8)]),
            ("馬", [(9, 1), (9, 7)]),
            ("象", [(9, 2), (9, 6)]),
            ("士", [(9, 3), (9, 5)]),
            ("将", [(9, 4)]),
            ("砲", [(7, 1), (7, 7)]),
            ("卒", [(6, 0), (6, 2), (6, 4), (6, 6), (6, 8)])
        ]

        for name, positions in pieces_red:
            for pos in positions:
                self.board[pos[0]][pos[1]] = ChessPiece(name, "red", pos)
                maps[pos[0]][pos[1]] = name
        for name, positions in pieces_black:
            for pos in positions:
                self.board[pos[0]][pos[1]] = ChessPiece(name, "black", pos)
                maps[pos[0]][pos[1]] = name
        print(self.board)
        for line in maps:
            print(line)
        return self.board

    def is_valid_move(self, piece, new_position):
        # 实现棋子移动逻辑的验证
        # 这里是一个占位符逻辑，需要替换为实际规则
        x, y = new_position
        if 0 <= x < 9 and 0 <= y < 10 and (self.board[y][x] is None or self.board[y][x].color != piece.color):
            return True
        return False

    def move_piece(self, start_pos, end_pos):
        piece = self.get_piece_at(start_pos)
        if piece is not None and self.is_valid_move(piece, end_pos):
            self.history.append(copy.deepcopy(self.board))
            self.set_piece_at(end_pos, piece)
            self.set_piece_at(start_pos, None)
            piece.move(end_pos)
            return True
        return False

    def get_piece_at(self, position):
        x, y = position
        return self.board[y][x]

    def set_piece_at(self, position, piece):
        x, y = position
        self.board[y][x] = piece

    def undo_move(self):
        if self.history:
            self.board = self.history.pop()

    def get_game_state(self):
        # 返回当前游戏状态的副本，供前端使用
        return copy.deepcopy(self.board)

    def is_checkmate(self, color):
        # 占位符：判断是否被将死的逻辑
        return False

    def is_stalemate(self, color):
        # 占位符：判断是否和棋的逻辑
        return False


chessboard = ChessBoard()
