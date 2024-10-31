import pygame
from chess_front_init import ChessFrontInit, restart, hint, undo
from chess_front_move import ChessFrontMove
from chess_board import ChessBoard

# 设置棋盘大小
CELL_SIZE = 60  # 每个棋格的大小
BOARD_WIDTH = 8 * CELL_SIZE
BOARD_HEIGHT = 9 * CELL_SIZE
SCREEN_SIZE = (BOARD_WIDTH + 400, BOARD_HEIGHT + 300)

class DoublePage:
    def __init__(self, screen):
        self.screen = screen
        self.background_color = (0, 128, 0)
        self.font = pygame.font.SysFont("华文隶书", 48)

    def draw(self):
        # 创建窗口
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("中国象棋棋盘")

        ChessFrontMove(self.screen, ChessFrontInit(self.screen).chessboard, ChessBoard()).run(1)

    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # 检测是否点击了双人对战按钮
            if restart.is_clicked(mouse_pos):
                print(restart.rect)
                return "double"
            if undo.is_clicked(mouse_pos):
                return "start"  # 按下 ESC 键返回开始界面
        return "double"

class AiPage:
    def __init__(self, screen):
        self.screen = screen
        self.background_color = (0, 128, 0)
        self.font = pygame.font.SysFont("华文隶书", 48)

    def draw(self):
            # 创建窗口
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("中国象棋棋盘")

        ChessFrontMove(self.screen, ChessFrontInit(self.screen).chessboard, ChessBoard()).run(2)

    def check_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "start"  # 按下 ESC 键返回开始界面
        return "computer"





