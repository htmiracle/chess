import copy
from game_manager import GameManager
from chess_board import ChessBoard
from game_logic import GameLogic
import hashlib
import concurrent.futures


class OpeningLibrary:
    def __init__(self):
        self.openings = {
            0: [(2, 1, 2, 4), (0, 0, 2, 0), (0, 7, 2, 6)],
            1: [(2, 1, 2, 4), (0, 8, 2, 8), (0, 7, 2, 6)],
            2: [(2, 1, 2, 4), (0, 1, 2, 2), (0, 7, 2, 6)],
            3: [(2, 1, 2, 4), (0, 8, 1, 7), (0, 7, 2, 6)],
            4: [(0, 6, 2, 4), (2, 1, 2, 4), (0, 0, 2, 0)],
            5: [(2, 1, 2, 4), (2, 4, 2, 6), (0, 0, 2, 0)],
            6: [(2, 1, 2, 4), (0, 7, 2, 6), (0, 0, 2, 0)]
        }
        self.current_step = {key: 0 for key in self.openings}  # 初始化每个开局的步数指针

    def get_opening_move(self, board_hash):
        # 根据棋盘哈希值查找开局库中的最佳开局步骤
        if board_hash in self.openings:
            opening = self.openings[board_hash]
            step = self.current_step[board_hash]
            if step < len(opening):
                move = opening[step]  # 获取当前步的走法
                self.current_step[board_hash] += 1  # 步数指针递增
                return move
            else:
                return None  # 如果步数超出，返回 None 表示开局已结束
        return None


class AILogicHard:
    def __init__(self, board, depth_limit=3):
        self.logic_board = board  # 类
        self.init_board = ChessBoard().initialize_pieces()
        self.gamelogic = GameLogic(self.logic_board)  # 生成一个GameLogic的对象
        self.opening_library = OpeningLibrary()  # 初始化开局库
        self.depth_limit = depth_limit  # 设置搜索深度
        self.manager = GameManager(0, 0, self.init_board, self.gamelogic)
        self.board_hash = self.hash_board(board)

    def evaluate_board(self):
        """评估当前棋局分数，正数代表红方有利，负数代表黑方有利。"""
        score = 0
        position_values = {  # 示例位置分数表，可根据需要完善
            # 举例：为每个棋子在棋盘上的位置赋分
        }
        for row in self.logic_board.board:
            for piece in row:
                if piece:
                    piece_value = self.get_piece_value(piece)
                    position_value = position_values.get(piece.position, 0)
                    score += piece_value + position_value
        return score

    def get_piece_value(self, piece):
        """根据棋子类型和颜色返回评分。"""
        piece_values = {
            "帅": 1000, "将": -1000,
            "車": 50, "馬": 30, "砲": 30, "炮": 30,
            "相": 20, "象": 20, "仕": 20, "士": 20,
            "兵": 10, "卒": 10
        }
        # 从字典 piece_values 中获取指定棋子的评分,如果棋子是红方，直接返回正的棋子分数;如果棋子是黑方则返回该棋子的负分数
        return piece_values.get(piece.name, 0) if piece.color == 'red' else -piece_values.get(piece.name, 0)

    def minimax(self, board, depth, alpha, beta, maximizingPlayer, game_manager):
        """Minimax 算法与 Alpha-Beta 剪枝相结合，用于寻找最佳走法。"""
        if depth == 0 or game_manager.current_turn >= 2:
            return self.evaluate_board()  # 返回的是当前棋盘的一个分数，用于判断该棋局对当前玩家的有利程度（正数表示有利，负数表示不利）

        if maximizingPlayer:
            maxEval = float('-inf')
            for piece, moves in self.get_all_possible_moves(board, 'red').items():
                for move in moves:
                    new_board = self.make_move(board, move, piece)
                    new_game_manager = copy.deepcopy(game_manager)  # 复用 game_manager
                    eval = self.minimax(new_board, depth - 1, alpha, beta, False, new_game_manager)
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Alpha-Beta 剪枝
            return maxEval
        else:
            minEval = float('inf')
            for piece, moves in self.get_all_possible_moves(board, 'black').items():
                for move in moves:
                    new_board = self.make_move(board, move, piece)
                    new_game_manager = copy.deepcopy(game_manager)  # 复用 game_manager
                    eval = self.minimax(new_board, depth - 1, alpha, beta, True, new_game_manager)
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Alpha-Beta 剪枝
            return minEval

    def get_best_move(self, board):
        """结合开局库和 Minimax 算法，获取最佳走法，并使用多线程优化性能。"""
        # 查找开局库的开局走法
        opening_move = self.opening_library.get_opening_move(self.board_hash)
        if opening_move:
            return opening_move  # 按顺序返回开局库中的下一步

        # 否则使用 Minimax + Alpha-Beta 剪枝选择最佳走法
        best_move = None
        best_value = float('-inf')

        moves = [
            (piece, move)
            for piece, piece_moves in self.get_all_possible_moves(board, 'red').items()
            for move in piece_moves
        ]
        chunk_size = max(1, len(moves) // 4)  # 假设我们有4个线程

        # 定义线程池
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(self.evaluate_move_batch, board, moves[i:i + chunk_size]): moves[i:i + chunk_size]
                for i in range(0, len(moves), chunk_size)
            }

            # 遍历每个任务的结果
            for future in concurrent.futures.as_completed(futures):
                try:
                    board_value, move = future.result()
                    if board_value > best_value:
                        best_value = board_value
                        best_move = move
                except Exception as e:
                    print(f"Error evaluating move: {e}")

        return best_move

    def evaluate_move_batch(self, board, move_batch):
        """辅助方法，批量评估多个移动路径。"""
        best_value = float('-inf')
        best_move = None
        game_manager = GameManager(0, 0, board, self.gamelogic)  # 初始化 GameManager
        for piece, move in move_batch:
            new_board = self.make_move(board, move, piece)
            board_value = self.minimax(new_board, self.depth_limit, float('-inf'), float('inf'), False, game_manager)
            if board_value > best_value:
                best_value = board_value
                best_move = (piece.position[0], piece.position[1], move[0], move[1])
        return best_value, best_move

    def get_all_possible_moves(self, board, color):
        """获取当前棋盘上所有棋子的可能走法。"""
        moves = {}
        for row in board:
            for piece in row:
                if piece and piece.color == color:
                    moves[piece] = self.gamelogic.piece_logic(piece)
        return moves

    def make_move(self, board, move, piece):
        """执行走棋，返回新棋盘状态。"""
        new_board = copy.deepcopy(board)  # 深拷贝棋盘
        start_x, start_y = piece.position
        end_x, end_y = move
        new_board[end_x][end_y] = new_board[start_x][start_y]  # 移动棋子
        new_board[start_x][start_y] = None  # 将起点清空
        return new_board

    def hash_board(self, board):
        """生成棋盘的哈希值，并将其限制在适当范围内。"""
        board_str = str(board)
        # 生成 MD5 哈希值
        hash_value = int(hashlib.md5(board_str.encode()).hexdigest(), 16)
        # 使用更大范围的哈希值减少冲突
        return hash_value % 1000

    def evaluate_move(self, board, piece, move):
        """辅助方法，用于在多线程中评估每个棋子的移动路径。"""
        new_board = self.make_move(board, move, piece)
        return self.minimax(new_board, self.depth_limit, float('-inf'), float('inf'), False)
