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


    def __init__(self, board, depth_limit = 3):
        self.logic_board = board # 类
        self.init_board = ChessBoard().initialize_pieces()
        self.gamelogic = GameLogic(self.logic_board)  # 生成一个GameLogic的对象
        self.opening_library = OpeningLibrary()  # 初始化开局库
        self.depth_limit = depth_limit  # 设置搜索深度
        self.manager = GameManager(0, 0, self.init_board, self.gamelogic)
        self.board_hash = self.hash_board(board)

    def evaluate_board(self, board, new_board, piece, move, all_possible_move_black):
        """评估当前棋局分数，正数代表红方有利，负数代表黑方有利。"""
        score = 0

        position_value = 0
        if board[move[0]][move[1]] and board[move[0]][move[1]].color == "black":
            if board[move[0]][move[1]].name == "卒":
                position_value += 5
            elif board[move[0]][move[1]].name == "士":
                position_value += 10
            elif board[move[0]][move[1]].name == "象":
                position_value += 10
            elif board[move[0]][move[1]].name == "砲":
                position_value += 25
            elif board[move[0]][move[1]].name == "馬":
                position_value += 40
            elif board[move[0]][move[1]].name == "車":
                position_value += 50
            elif board[move[0]][move[1]].name == "将":
                position_value += 1000
        for black_piece,moves in all_possible_move_black.items():
            if move in moves:
                if piece.name == "兵":
                    position_value -= 5
                elif piece.name == "仕":
                    position_value -= 10
                elif piece.name == "相":
                    position_value -= 10
                elif piece.name == "炮":
                    position_value -= 25
                elif piece.name == "馬":
                    position_value -= 40
                elif piece.name == "車":
                    position_value -= 50
                elif piece.name == "帅":
                    position_value -= 1000
            if (black_piece.name == "車" or black_piece.name == "砲") and (piece.position[0] == black_piece[0] or piece.position[1] == black_piece[1]):
                if piece.name == "兵":
                    position_value -= 5
                elif piece.name == "仕":
                    position_value -= 10
                elif piece.name == "相":
                    position_value -= 10
                elif piece.name == "炮":
                    position_value -= 25
                elif piece.name == "馬":
                    position_value -= 40
                elif piece.name == "車":
                    position_value -= 50
                elif piece.name == "帅":
                    position_value -= 1000

            if piece.position in moves:

                if piece.name == "兵":
                    position_value += 5
                elif piece.name == "仕":
                    position_value += 10
                elif piece.name == "相":
                    position_value += 10
                elif piece.name == "炮":
                    position_value += 25
                elif piece.name == "馬":
                    position_value += 40
                elif piece.name == "車":
                    position_value += 50
                elif piece.name == "帅":
                    position_value += 1000


        #
        # # 如果低等级棋子移动后的位置会导致高等级棋子被吃，则给予高等级棋子相应等级的负奖励
        # for moves in all_possible_move_black.values():
        #     if move in moves:
        #         if piece.name in ["兵", "仕", "相"] and board[move[0]][move[1]] and board[move[0]][move[1]].name in ["車", "馬", "炮", "帅"]:
        #             if board[move[0]][move[1]].name == "車":
        #                 position_value -= 50
        #             elif board[move[0]][move[1]].name == "馬":
        #                 position_value -= 40
        #             elif board[move[0]][move[1]].name == "炮":
        #                 position_value -= 25
        #             elif board[move[0]][move[1]].name == "帅":
        #                 position_value -= 1000
        #
        # self.gamelogic.piece_logic(piece)
        # for moves in all_possible_move_black.values():
        #     if move in moves:
        #         break
        #     new_logic_board = ChessBoard()
        #     new_logic_board.board = new_board
        #     gamelogic = GameLogic(new_logic_board)
        #     this_piece_moves = gamelogic.piece_logic(piece)
        #     for move in this_piece_moves:
        #         if board[move[0]][move[1]] and board[move[0]][move[1]].color == "black":
        #             if board[move[0]][move[1]].name == "卒":
        #                 position_value += 4
        #             elif board[move[0]][move[1]].name == "士":
        #                 position_value += 8
        #             elif board[move[0]][move[1]].name == "象":
        #                 position_value += 8
        #             elif board[move[0]][move[1]].name == "砲":
        #                 position_value += 20
        #             elif board[move[0]][move[1]].name == "馬":
        #                 position_value += 32
        #             elif board[move[0]][move[1]].name == "車":
        #                 position_value += 40
        #             elif board[move[0]][move[1]].name == "将":
        #                 position_value += 800
        #
        #
        score += position_value

        return score


    def get_piece_value(self, piece):
        """根据棋子类型和颜色返回评分。"""
        piece_values = {
            "帅": 1000, "将": 1000,
            "車": 500, "馬": 300, "砲": 250, "炮": 250,
            "相": 50, "象": 50, "仕": 50, "士": 50,
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
    def minimax(self, board, new_board, depth, alpha, beta, maximizingPlayer, game_manager, piece, move):
        all_possible_move_red = self.get_all_possible_moves(board, 'red')
        all_possible_move_black = self.get_all_possible_moves(new_board, 'black')
        """Minimax 算法与 Alpha-Beta 剪枝相结合，用于寻找最佳走法。"""
        if depth == 0 or game_manager.current_turn >= 2 : # 如果递归深度 depth 为 0，或者游戏已经结束（通过 is_game_over 检查），则返回当前棋盘的评估值（evaluate_board），不再继续深入递归
            return self.evaluate_board(board, new_board, piece, move, all_possible_move_black) # 返回的是当前棋盘的一个分数，用于判断该棋局对当前玩家的有利程度（正数表示有利，负数表示不利）

        if maximizingPlayer:
            maxEval = float('-inf') # 如果当前轮到最大化玩家（例如 AI），我们初始化 maxEval 为负无穷大，以便在接下来的循环中找到最大的可能值。
            for piece,moves in all_possible_move_red.items(): # 获取当前棋盘上红方（最大化玩家）所有可能的走法
                for move in moves:
                    new1_board = self.make_move(board, move, piece) # 执行走棋，将棋子从起点移动到终点，并返回一个新棋盘（new_board），表示移动后的状态
                    eval = self.minimax(new_board, new1_board, depth - 1, alpha, beta, False, game_manager, piece, move) # 递归调用 minimax，通过对 new_board 递归深入搜索，并将 depth 减少 1。False 表示下一步是对手的轮次（最小化玩家）。
                    maxEval = max(maxEval, eval) # 更新当前的最大评分，取 maxEval 和递归返回的 eval 中的较大值
                    alpha = max(alpha, eval) # 更新 alpha（最大化玩家的最佳结果），以便在之后用于剪枝
                    if beta <= alpha: # 如果 alpha 已经大于等于 beta，那么对手（最小化玩家）不会选择这条路径，因此可以提前停止进一步的搜索，从而提升效率
                        break  # Alpha-Beta 剪枝
            return maxEval # 当所有可能的走法都被评估过，返回 maxEval，即最大化玩家能得到的最佳评分
        else:
            minEval = float('inf') # 如果当前是最小化玩家的轮次（例如对手），我们初始化 minEval 为正无穷大，以便在接下来的循环中找到最小的可能值
            for piece,moves in all_possible_move_black.items():
                for move in moves:
                    new1_board = self.make_move(board, move, piece) # 获取当前棋盘上黑方（最小化玩家）所有可能的走法，并执行这些走法，生成新的棋盘状态
                    eval = self.minimax(new_board, new1_board, depth - 1, alpha, beta, True, game_manager, piece, move) # 递归调用 minimax，进入下一层的搜索。True 表示下一轮是最大化玩家的轮次
                    minEval = min(minEval, eval) # 更新当前的最小评分，取 minEval 和递归返回的 eval 中的较小值
                    beta = min(beta, eval) # 更新 beta（最小化玩家的最佳结果），用于后续的剪枝
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
        all_possible_move_red = self.get_all_possible_moves(board, 'red')
        all_possible_move_black = self.get_all_possible_moves(board, 'black')

        for piece, moves in self.get_all_possible_moves(board, 'red').items():
            for move in moves:
                new_board = self.make_move(board,move,piece)
                board_value = self.evaluate_board(board, new_board, piece, move, all_possible_move_black)
                print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                print("board:"+piece.name+"board_value:" + str(board_value))
                print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                if board_value > best_value:
                    best_value = board_value
                    best_move = (piece.position[0], piece.position[1], move[0], move[1])

        print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
        print("best_value:" + str(best_value))
        print(best_move)
        return best_move


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
        """生成棋盘的哈希值，并将其限制在 0 到 6 的范围内。"""
        board_str = str(board)
        # 生成 MD5 哈希值
        hash_value = int(hashlib.md5(board_str.encode()).hexdigest(), 16)
        # 将哈希值限制在 0 到 6
        return hash_value % 7






