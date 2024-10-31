import copy
from game_manager import GameManager
from chess_board import ChessBoard
from game_logic import GameLogic
import hashlib

class OpeningLibrary:
    def __init__(self):
        self.openings = {
            'initial': [(0, 0, 3, 0), (2, 1, 2, 4)],  # 示例开局库，可根据实际情况扩充
        }

    def get_opening_move(self, board_hash):
        # 根据棋盘哈希值查找开局库中的最佳开局步骤
        if board_hash in self.openings:
            return self.openings[board_hash]
        return None


class AILogicHard:


    def __init__(self, board, depth_limit = 3):
        self.logic_board = board # 类
        self.init_board = ChessBoard().initialize_pieces()
        self.gamelogic = GameLogic(self.logic_board)  # 生成一个GameLogic的对象
        self.opening_library = OpeningLibrary()  # 初始化开局库
        self.depth_limit = depth_limit  # 设置搜索深度
        self.manager = GameManager(0, 0, self.init_board, self.gamelogic)

    def evaluate_board(self):
        """评估当前棋局分数，正数代表红方有利，负数代表黑方有利。"""
        score = 0
        for row in self.logic_board.board:
            for piece in row:
                if piece:
                    score += self.get_piece_value(piece)
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

    '''
    minimax 函数：这是递归函数，使用 Minimax 算法来评估棋盘状态并寻找最佳走法
    board：当前棋局的状态（棋盘的布置）
    depth：搜索的深度限制，表示当前递归的层数。当 depth 达到 0 时停止递归
    alpha：当前已知的对当前玩家最好的情况（最高分），用于剪枝
    beta：当前已知的对对手最坏的情况（最低分），用于剪枝
    maximizingPlayer：一个布尔值，True 表示当前玩家是最大化玩家（一般是 AI），False 表示当前玩家是最小化玩家（对手）
    '''
    def minimax(self, board, depth, alpha, beta, maximizingPlayer): #
        """Minimax 算法与 Alpha-Beta 剪枝相结合，用于寻找最佳走法。"""
        if depth == 0 or self.manager.current_turn >=2 : # 如果递归深度 depth 为 0，或者游戏已经结束（通过 is_game_over 检查），则返回当前棋盘的评估值（evaluate_board），不再继续深入递归
            return self.evaluate_board() # 返回的是当前棋盘的一个分数，用于判断该棋局对当前玩家的有利程度（正数表示有利，负数表示不利）

        if maximizingPlayer:
            maxEval = float('-inf') # 如果当前轮到最大化玩家（例如 AI），我们初始化 maxEval 为负无穷大，以便在接下来的循环中找到最大的可能值。
            for piece,moves in self.get_all_possible_moves('red'): # 获取当前棋盘上红方（最大化玩家）所有可能的走法
                for move in moves:
                    new_board = self.make_move(board, move, piece) # 执行走棋，将棋子从起点移动到终点，并返回一个新棋盘（new_board），表示移动后的状态
                    eval = self.minimax(new_board, depth - 1, alpha, beta, False) # 递归调用 minimax，通过对 new_board 递归深入搜索，并将 depth 减少 1。False 表示下一步是对手的轮次（最小化玩家）。
                    maxEval = max(maxEval, eval) # 更新当前的最大评分，取 maxEval 和递归返回的 eval 中的较大值
                    alpha = max(alpha, eval) # 更新 alpha（最大化玩家的最佳结果），以便在之后用于剪枝
                    if beta <= alpha: # 如果 alpha 已经大于等于 beta，那么对手（最小化玩家）不会选择这条路径，因此可以提前停止进一步的搜索，从而提升效率
                        break  # Alpha-Beta 剪枝
            return maxEval # 当所有可能的走法都被评估过，返回 maxEval，即最大化玩家能得到的最佳评分
        else:
            minEval = float('inf') # 如果当前是最小化玩家的轮次（例如对手），我们初始化 minEval 为正无穷大，以便在接下来的循环中找到最小的可能值
            for piece,moves in self.get_all_possible_moves('black'):
                for move in moves:
                    new_board = self.make_move(board, move, piece) # 获取当前棋盘上黑方（最小化玩家）所有可能的走法，并执行这些走法，生成新的棋盘状态
                    eval = self.minimax(new_board, depth - 1, alpha, beta, True) # 递归调用 minimax，进入下一层的搜索。True 表示下一轮是最大化玩家的轮次
                    minEval = min(minEval, eval) # 更新当前的最小评分，取 minEval 和递归返回的 eval 中的较小值
                    beta = min(beta, eval) # 更新 beta（最小化玩家的最佳结果），用于后续的剪枝
                    if beta <= alpha:
                        break  # Alpha-Beta 剪枝
            return minEval

    def get_best_move(self, board):
        """结合开局库和 Minimax 算法，获取最佳走法。"""
        # 查找开局库的开局走法
        board_hash = self.hash_board(board) # 使用 hash_board 方法对当前棋盘进行哈希处理，生成一个唯一的字符串，用于在开局库中查找
        opening_move = self.opening_library.get_opening_move(board_hash) # 在开局库中查找该哈希值对应的开局步骤
        if opening_move:
            return opening_move[0]  # 返回开局库中的一步

        # 否则使用 Minimax + Alpha-Beta 剪枝选择最佳走法
        best_move = None
        best_value = float('-inf')
        for piece,moves in self.get_all_possible_moves('red'):
            for move in moves:
                new_board = self.make_move(board, move, piece)
                board_value = self.minimax(new_board, self.depth_limit, float('-inf'), float('inf'), False)
                if board_value > best_value:
                    best_value = board_value
                    best_move = piece.position[0],piece.position[1],move[0],move[1]
        return best_move

    def get_all_possible_moves(self, color):
        """获取当前棋盘上所有棋子的可能走法。"""
        moves = {}
        for piece in self.logic_board.board:
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
        """生成棋盘的紧凑哈希值。"""
        board_str = str(board)
        return hashlib.md5(board_str.encode()).hexdigest()  # 使用 MD5 生成固定长度哈希值


