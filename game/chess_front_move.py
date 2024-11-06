from chess_front_init import ChessFrontInit, restart, hint, undo, back
from chess_front_init import CELL_SIZE, offset_x, offset_y, WOOD
import pygame
import copy
import time
import sys
from ai_logic_easy import AILogicEasy
from game_manager import GameManager
from game_logic import GameLogic
from game_manager import make_move
from ai_logic_hard import AILogicHard
from image_button import ImageButton
from image_button import ImageButton

# 初始化 pygame.mixer 模块
pygame.mixer.init()

jiang_sound = pygame.mixer.Sound("../chess_mp3/jiang.mp3")
end_sound = pygame.mixer.Sound("../chess_mp3/end.mp3")
# 玩家对战游戏模式移动判定
def checkmated_prompt(chess_board, gamelogic):
    sum = 0
    for n in range(10):
        for j in range(9):
            pie = chess_board[n][j]
            if pie:
                if pie.name == "帅" and gamelogic.checkmated(pie):
                    jiang_sound.play()
                    sum += 1
                if pie.name == "将" and gamelogic.checkmated(pie):
                    jiang_sound.play()
                    sum -= 1
    return sum


class ChessFrontMove:
    def __init__(self, screen, chessboard, board):
        self.come_x = None
        self.come_y = None
        self.screen = screen
        self.chessboard = chessboard
        self.board = board
        # self.board_list = None
        # self.chessboard_list = None
        self.board_list = []
        self.chessboard_list = []

    def init(self):
        self.come_x, self.come_y = -100, -100
        start_chosen = False  # 判定是否已经选定了起点
        gamelogic = GameLogic(self.board)  # 生成一个GameLogic的对象
        chess_board = self.board.initialize_pieces()  # 初始化棋盘，存入chess_board里，后端棋盘
        self.board_list.append(copy.deepcopy(chess_board))
        end_position = gamelogic.piece_logic  # 计算可落点的函数，传参为起点坐标
        gamemanager = GameManager(0, 0, chess_board, gamelogic)  # 游戏管理器
        i = ChessFrontInit(self.screen)  # 控制前端画图类
        self.chessboard = i.initialize()  # 前端棋盘初始化
        self.chessboard_list.append(copy.deepcopy(self.chessboard))
        return start_chosen, chess_board, end_position, gamemanager, i, gamelogic

    # 判断执棋方选择棋子是否正确
    def correct_piece(self, start_x, start_y, gamemanager, chess_board):
        if self.chessboard[start_x][start_y] == 0:
            return 0
        # 判断选择的棋子是否是该回合棋手的颜色,如果不是则跳过
        if gamemanager.current_turn and chess_board[start_x][start_y].color == "red":
            return 0
        if not gamemanager.current_turn and chess_board[start_x][start_y].color == "black":
            return 0
        return 1

    def chosen_start_piece(self, board_pos, end_position, chess_board, gamemanager, i, gamelogic):
        start_x, start_y = board_pos
        gamelogic.logic_board.board = chess_board
        end_pos = end_position(chess_board[start_x][start_y])
        # 重新绘制完成移动后的棋盘
        i.chosen_feedback([start_x, start_y], gamemanager.current_turn, end_pos,
                          [self.come_x, self.come_y])
        return start_x, start_y, end_pos

    def p_vs_p(self):
        running = True  # 棋盘正在运行
        start_chosen, chess_board, end_position, gamemanager, i, gamelogic = self.init()

        while running:
            for event in pygame.event.get():
                pygame.display.update()  # 更新显示
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    board_pos = ChessFrontInit(self.screen).get_board_pos(mouse_x, mouse_y)
                    # 移动移动，横纵坐标分别已经保存在了board_pos中
                    if board_pos:
                        # 如果当前操作人编号大于1，说明游戏结束
                        if gamemanager.current_turn >= 2:
                            break
                        # 起始格
                        if not start_chosen:
                            # 判断选择的棋子是否为空,选择的棋子是否是该回合棋手的颜色,如果不是则跳过
                            if not self.correct_piece(board_pos[0], board_pos[1], gamemanager, chess_board):
                                break
                            start_x, start_y, end_pos = self.chosen_start_piece(board_pos, end_position, chess_board,
                                                                                gamemanager, i, gamelogic)
                            start_chosen = True
                        else:
                            # 判断是否进行了重新选择棋子的行为，如果有则跳过选择终点阶段
                            if self.correct_piece(board_pos[0], board_pos[1], gamemanager, chess_board):
                                start_x, start_y, end_pos = self.chosen_start_piece(board_pos, end_position,
                                                                                    chess_board, gamemanager, i, gamelogic)
                                break

                            end_x, end_y = board_pos
                            if [end_x, end_y] not in end_pos:
                                print("请重新输入")
                                break
                            gamemanager.check_end(end_x, end_y, chess_board)
                            i.animate_piece_move(start_x, start_y, end_x, end_y, self.chessboard[start_x][start_y], gamemanager.current_turn)
                            chess_board = make_move([start_x, start_y], [end_x, end_y], chess_board)
                            self.chessboard[end_x][end_y], self.chessboard[start_x][start_y] = self.chessboard[start_x][
                                start_y], 0

                            gamelogic.logic_board.board = chess_board
                            self.board_list.append(copy.deepcopy(chess_board))
                            self.chessboard_list.append(copy.deepcopy(self.chessboard))
                            i.chessboard = self.chessboard
                            start_chosen = False
                            # 切换玩家
                            if gamemanager.current_turn in [0, 1]:
                                gamemanager.next_turn()
                            self.come_x, self.come_y = start_x, start_y
                            # 判断
                            if gamemanager.current_turn in [2, 3]:
                                i.redraw(gamemanager.current_turn, [self.come_x, self.come_y])
                                end_sound.play()
                                break
                            #  检查是否被将军
                            if checkmated_prompt(chess_board, gamelogic):
                                i.checkmate(gamemanager.current_turn, [self.come_x, self.come_y])
                                break
                            # 重新绘制完成移动后的棋盘

                            i.redraw(gamemanager.current_turn, [self.come_x, self.come_y])
                    elif restart.is_clicked(event.pos) or back.is_clicked(event.pos):
                        print(restart.rect)
                        pygame.event.post(event)
                        if restart.is_clicked(event.pos):
                            print("restart")
                        if undo.is_clicked(event.pos):
                            print("back")
                        return
                    elif undo.is_clicked(event.pos):
                        if gamemanager.current_turn in [2, 3]:
                            break
                        chess_board = copy.deepcopy(self.board_list[-3])
                        self.board_list = self.board_list[:-2]
                        i.chessboard = copy.deepcopy(self.chessboard_list[-3])
                        self.chessboard = copy.deepcopy(self.chessboard_list[-3])
                        self.chessboard_list = self.chessboard_list[:-2]
                        self.come_x = self.come_y = -100
                        i.redraw(gamemanager.current_turn, [-100, -100])
                elif event.type == pygame.KEYDOWN:
                    1

            pygame.display.update()  # 更新显示

    def p_vs_c(self):
        running = True  # 棋盘正在运行
        start_chosen, chess_board, end_position, gamemanager, i, gamelogic = self.init()
        # ai = AILogicHard(self.board, 1)
        ai = AILogicEasy(self.board)
        while running:
            for event in pygame.event.get():
                if gamemanager.current_turn == 0:
                    pygame.display.update()  # 更新显示
                    pygame.time.wait(500)
                    pygame.event.clear()
                    start_x, start_y, end_x, end_y = ai.easy_ai_run()
                    # start_x, start_y, end_x, end_y = ai.get_best_move(self.board.board)
                    gamemanager.check_end(end_x, end_y, chess_board)
                    i.animate_piece_move(start_x, start_y, end_x, end_y, self.chessboard[start_x][start_y],
                                         gamemanager.current_turn)
                    chess_board = make_move([start_x, start_y], [end_x, end_y], chess_board)
                    self.chessboard[end_x][end_y], self.chessboard[start_x][start_y] = self.chessboard[start_x][
                        start_y], 0

                    start_chosen = False
                    gamelogic.logic_board.board = chess_board
                    self.board_list.append(copy.deepcopy(chess_board))
                    self.chessboard_list.append(copy.deepcopy(self.chessboard))
                    i.chessboard = self.chessboard
                    # 切换玩家
                    if gamemanager.current_turn in [0, 1]:
                        gamemanager.next_turn()
                    self.come_x, self.come_y = start_x, start_y
                    if gamemanager.current_turn in [2, 3]:
                        i.redraw(gamemanager.current_turn, [self.come_x, self.come_y])
                        continue
                    #  检查是否被将军
                    if checkmated_prompt(chess_board, gamelogic):
                        i.checkmate(gamemanager.current_turn, [self.come_x, self.come_y])
                        continue
                    # 重新绘制完成移动后的棋盘
                    i.redraw(gamemanager.current_turn, [self.come_x, self.come_y])
                    break
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    print(mouse_x, mouse_y)
                    board_pos = ChessFrontInit(self.screen).get_board_pos(mouse_x, mouse_y)
                    # 移动移动，横纵坐标分别已经保存在了board_pos中
                    if board_pos:
                        # 如果当前操作人编号大于1，说明游戏结束
                        if gamemanager.current_turn >= 2:
                            continue
                        # 起始格
                        if not start_chosen:
                            # 判断选择的棋子是否为空,选择的棋子是否是该回合棋手的颜色,如果不是则跳过
                            if not self.correct_piece(board_pos[0], board_pos[1], gamemanager, chess_board):
                                break
                            start_x, start_y, end_pos = self.chosen_start_piece(board_pos, end_position, chess_board,
                                                                                gamemanager, i, gamelogic)
                            start_chosen = True
                        else:
                            # 判断是否进行了重新选择棋子的行为，如果有则跳过选择终点阶段
                            if self.correct_piece(board_pos[0], board_pos[1], gamemanager, chess_board):
                                start_x, start_y, end_pos = self.chosen_start_piece(board_pos, end_position,
                                                                                    chess_board, gamemanager, i, gamelogic)
                                break

                            end_x, end_y = board_pos
                            if [end_x, end_y] not in end_pos:
                                print("请重新输入")
                                break
                            gamemanager.check_end(end_x, end_y, chess_board)
                            i.animate_piece_move(start_x, start_y, end_x, end_y, self.chessboard[start_x][start_y],
                                                 gamemanager.current_turn)
                            chess_board = make_move([start_x, start_y], [end_x, end_y], chess_board)
                            self.chessboard[end_x][end_y], self.chessboard[start_x][start_y] = self.chessboard[start_x][
                                start_y], 0

                            for row in chess_board:
                                for pie in row:
                                    if pie:
                                        print(pie.name, end=" ")
                                    else:
                                        print("〇", end=" ")
                                print()
                            gamelogic.logic_board.board = chess_board
                            self.board_list.append(copy.deepcopy(chess_board))
                            self.chessboard_list.append(copy.deepcopy(self.chessboard))
                            i.chessboard = self.chessboard
                            start_chosen = False
                            # 切换玩家
                            if gamemanager.current_turn in [0, 1]:
                                gamemanager.next_turn()
                            self.come_x, self.come_y = start_x, start_y
                            if gamemanager.current_turn in [2, 3]:
                                end_sound.play()
                                i.redraw(gamemanager.current_turn, [self.come_x, self.come_y])
                                break
                            #  检查是否被将军
                            if checkmated_prompt(chess_board, gamelogic):
                                i.checkmate(gamemanager.current_turn, [self.come_x, self.come_y])
                                break
                            # 重新绘制完成移动后的棋盘
                            i.redraw(gamemanager.current_turn, [self.come_x, self.come_y])
                    elif restart.is_clicked(event.pos) or back.is_clicked(event.pos):
                        print(restart.rect)
                        pygame.event.post(event)
                        return
                    elif undo.is_clicked(event.pos):
                        if gamemanager.current_turn in [2, 3]:
                            break
                        chess_board = copy.deepcopy(self.board_list[-3])
                        self.board_list = self.board_list[:-2]
                        i.chessboard = copy.deepcopy(self.chessboard_list[-3])
                        self.chessboard = copy.deepcopy(self.chessboard_list[-3])
                        self.chessboard_list = self.chessboard_list[:-2]
                        self.come_x = self.come_y = -100
                        i.redraw(gamemanager.current_turn, [-100, -100])
                elif event.type == pygame.KEYDOWN:
                    1

            pygame.display.update()  # 更新显示

    def run(self, i):
        if i == 1:
            self.p_vs_p()
        elif i == 2:
            self.p_vs_c()
