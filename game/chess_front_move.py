from chess_front_init import ChessFrontInit, restart, hint, undo
import pygame
import time
import sys
from ai_logic_easy import AILogicEasy
from game_manager import GameManager
from game_logic import GameLogic
from game_manager import make_move
from image_button import ImageButton


# 玩家对战游戏模式移动判定
def checkmated_prompt(chess_board, gamelogic):
    for n in range(10):
        for j in range(9):
            pie = chess_board[n][j]
            if pie:
                if pie.name == "帅" and gamelogic.checkmated(pie):
                    return 1
                if pie.name == "将" and gamelogic.checkmated(pie):
                    return 1
    return 0


class ChessFrontMove:
    def __init__(self, screen, chessboard, board):
        self.come_x = None
        self.come_y = None
        self.screen = screen
        self.chessboard = chessboard
        self.board = board

    def init(self):
        self.come_x, self.come_y = -100, -100
        start_chosen = False  # 判定是否已经选定了起点
        gamelogic = GameLogic(self.board)  # 生成一个GameLogic的对象
        chess_board = self.board.initialize_pieces()  # 初始化棋盘，存入chess_board里，后端棋盘
        end_position = gamelogic.piece_logic  # 计算可落点的函数，传参为起点坐标
        gamemanager = GameManager(0, 0, chess_board, gamelogic)  # 游戏管理器
        i = ChessFrontInit(self.screen)  # 控制前端画图类
        self.chessboard = i.initialize()  # 前端棋盘初始化
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

    def chosen_start_piece(self, board_pos, end_position, chess_board, gamemanager, i):
        start_x, start_y = board_pos
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
                                                                                gamemanager, i)
                            start_chosen = True
                        else:
                            # 判断是否进行了重新选择棋子的行为，如果有则跳过选择终点阶段
                            if self.correct_piece(board_pos[0], board_pos[1], gamemanager, chess_board):
                                start_x, start_y, end_pos = self.chosen_start_piece(board_pos, end_position,
                                                                                    chess_board, gamemanager, i)
                                break

                            end_x, end_y = board_pos
                            if [end_x, end_y] not in end_pos:
                                print("请重新输入")
                                break
                            gamemanager.check_end(end_x, end_y)
                            chess_board = make_move([start_x, start_y], [end_x, end_y], chess_board)
                            self.chessboard[end_x][end_y], self.chessboard[start_x][start_y] = self.chessboard[start_x][
                                start_y], 0

                            start_chosen = False
                            # 切换玩家
                            if gamemanager.current_turn in [0, 1]:
                                gamemanager.next_turn()
                            self.come_x, self.come_y = start_x, start_y
                            # 判断
                            if gamemanager.current_turn in [2, 3]:
                                i.redraw(gamemanager.current_turn, [self.come_x, self.come_y])
                                break
                            #  检查是否被将军
                            if checkmated_prompt(chess_board, gamelogic):
                                i.checkmate(gamemanager.current_turn, [self.come_x, self.come_y])
                                break
                            # 重新绘制完成移动后的棋盘
                            i.redraw(gamemanager.current_turn, [self.come_x, self.come_y])
                    elif restart.is_clicked(event.pos) or undo.is_clicked(event.pos):
                        print(restart.rect)
                        pygame.event.post(event)
                        return

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    start_chosen, chess_board, end_position, gamemanager, i, gamelogic = self.init()

            pygame.display.update()  # 更新显示

    def p_vs_c(self):
        running = True  # 棋盘正在运行
        start_chosen, chess_board, end_position, gamemanager, i, gamelogic = self.init()
        ai = AILogicEasy(self.board)
        while running:
            for event in pygame.event.get():
                if gamemanager.current_turn == 0:
                    pygame.display.update()  # 更新显示
                    pygame.time.wait(1000)
                    pygame.event.clear()
                    start_x, start_y, end_x, end_y = ai.easy_ai_run()
                    print(start_x, start_y, end_x, end_y)
                    gamemanager.check_end(end_x, end_y)
                    chess_board = make_move([start_x, start_y], [end_x, end_y], chess_board)
                    self.chessboard[end_x][end_y], self.chessboard[start_x][start_y] = self.chessboard[start_x][start_y], 0

                    start_chosen = False
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
                    # 如果当前操作人编号大于1，说明游戏结束
                    if gamemanager.current_turn >= 2:
                        break
                    mouse_x, mouse_y = event.pos
                    print(mouse_x, mouse_y)
                    board_pos = ChessFrontInit(self.screen).get_board_pos(mouse_x, mouse_y)
                    # 移动移动，横纵坐标分别已经保存在了board_pos中
                    if board_pos:
                        # 起始格
                        if not start_chosen:
                            # 判断选择的棋子是否为空,选择的棋子是否是该回合棋手的颜色,如果不是则跳过
                            if not self.correct_piece(board_pos[0], board_pos[1], gamemanager, chess_board):
                                break
                            start_x, start_y, end_pos = self.chosen_start_piece(board_pos, end_position, chess_board,
                                                                                gamemanager, i)
                            start_chosen = True
                        else:
                            # 判断是否进行了重新选择棋子的行为，如果有则跳过选择终点阶段
                            if self.correct_piece(board_pos[0], board_pos[1], gamemanager, chess_board):
                                start_x, start_y, end_pos = self.chosen_start_piece(board_pos, end_position,
                                                                                    chess_board, gamemanager, i)
                                break

                            end_x, end_y = board_pos
                            if [end_x, end_y] not in end_pos:
                                print("请重新输入")
                                break
                            gamemanager.check_end(end_x, end_y)
                            chess_board = make_move([start_x, start_y], [end_x, end_y], chess_board)
                            self.chessboard[end_x][end_y], self.chessboard[start_x][start_y] = self.chessboard[start_x][
                                start_y], 0

                            start_chosen = False
                            # 切换玩家
                            if gamemanager.current_turn in [0, 1]:
                                gamemanager.next_turn()
                            self.come_x, self.come_y = start_x, start_y
                            if gamemanager.current_turn in [2, 3]:
                                i.redraw(gamemanager.current_turn, [self.come_x, self.come_y])
                                break
                            #  检查是否被将军
                            if checkmated_prompt(chess_board, gamelogic):
                                i.checkmate(gamemanager.current_turn, [self.come_x, self.come_y])
                                break
                            # 重新绘制完成移动后的棋盘
                            i.redraw(gamemanager.current_turn, [self.come_x, self.come_y])

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    pygame.event.clear()
                    start_chosen, chess_board, end_position, gamemanager, i, gamelogic = self.init()

            pygame.display.update()  # 更新显示

    def run(self, i):
        if i == 1:
            self.p_vs_p()
        elif i == 2:
            self.p_vs_c()
