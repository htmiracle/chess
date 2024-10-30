import copy

class OpeningLibrary:
    def __init__(self):
        self.openings = {
            'initial': [(2, 0, 3, 0), (2, 2, 3, 2)],  # 示例开局库，可根据实际情况扩充
        }

    def get_opening_move(self, board_hash):
        # 根据棋盘哈希值查找开局库中的最佳开局步骤
        if board_hash in self.openings:
            return self.openings[board_hash]
        return None


class AILogicHard:
    def __init__(self, board):
        self.board = board
        self.opening_library = OpeningLibrary()  # 初始化开局库
        self.depth_limit = 3  # 设置搜索深度

    def evaluate_board(self, board):
        """评估当前棋局分数，正数代表红方有利，负数代表黑方有利。"""
        score = 0
        for row in board:
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
        if depth == 0 or self.is_game_over(board):
            return self.evaluate_board(board)

        if maximizingPlayer:
            maxEval = float('-inf')
            for move in self.get_all_possible_moves(board, 'red'):
                new_board = self.make_move(board, move)
                eval = self.minimax(new_board, depth - 1, alpha, beta, False)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Alpha-Beta 剪枝
            return maxEval
        else:
            minEval = float('inf')
            for move in self.get_all_possible_moves(board, 'black'):
                new_board = self.make_move(board, move)
                eval = self.minimax(new_board, depth - 1, alpha, beta, True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha-Beta 剪枝
            return minEval

    def get_best_move(self, board):
        """结合开局库和 Minimax 算法，获取最佳走法。"""
        # 查找开局库的开局走法
        board_hash = self.hash_board(board)
        opening_move = self.opening_library.get_opening_move(board_hash)
        if opening_move:
            return opening_move[0]  # 返回开局库中的一步

        # 否则使用 Minimax + Alpha-Beta 剪枝选择最佳走法
        best_move = None
        best_value = float('-inf')
        for move in self.get_all_possible_moves(board, 'red'):
            new_board = self.make_move(board, move)
            board_value = self.minimax(new_board, self.depth_limit, float('-inf'), float('inf'), False)
            if board_value > best_value:
                best_value = board_value
                best_move = move
        return best_move

    def get_all_possible_moves(self, board, color):
        """获取当前棋盘上所有棋子的可能走法。"""
        moves = []
        # 假设你已经在其他部分实现了如何根据棋子获取可能的走法
        # 这里只需要调用该逻辑，将所有棋子的可能走法添加到 moves 中
        return moves

    def make_move(self, board, move):
        """执行走棋，返回新棋盘状态。"""
        new_board = copy.deepcopy(board)  # 深拷贝棋盘
        start_x, start_y, end_x, end_y = move
        new_board[end_x][end_y] = new_board[start_x][start_y]  # 移动棋子
        new_board[start_x][start_y] = None  # 将起点清空
        return new_board

    def hash_board(self, board):
        """生成棋盘的哈希值，用作开局库的键。"""
        return str(board)

    def is_game_over(self, board):
        """检查游戏是否结束。"""
        return False
