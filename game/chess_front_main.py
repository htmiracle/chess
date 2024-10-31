import pygame
from chess_front_init import ChessFrontInit, restart, hint, undo
from chess_front_move import ChessFrontMove
from chess_board import ChessBoard

# 设置棋盘大小
CELL_SIZE = 60  # 每个棋格的大小
BOARD_WIDTH = 8 * CELL_SIZE
BOARD_HEIGHT = 9 * CELL_SIZE
SCREEN_SIZE = (BOARD_WIDTH + 400, BOARD_HEIGHT + 300)

class ImageButton:
    def __init__(self, image_path, x, y, width, height, transparency=255):
        self.image = pygame.image.load(image_path)  # 加载按钮图片
        self.image = pygame.transform.scale(self.image, (width, height))  # 缩放图片
        self.image.set_alpha(transparency)  # 设置透明度 (0-255)
        self.rect = self.image.get_rect(topleft=(x, y))  # 设置按钮的位置和大小

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # 将图片绘制到屏幕

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)  # 检测是否点击了按钮

class DoublePage:
    def __init__(self, screen):
        self.screen = screen
        self.background_color = (0, 128, 0)
        self.font = pygame.font.SysFont("华文隶书", 48)
        self.button_BACK = ImageButton("../other_picture/back.gif", 880 - 300,
                                       840 - 250, 200, 60,
                                       transparency=360)

    def draw(self):
        # 创建窗口
        pygame.display.set_caption("双人对战")

        ChessFrontMove(self.screen, ChessFrontInit(self.screen).chessboard, ChessBoard()).run(1)
        self.button_BACK.draw(self.screen)

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
        pygame.display.set_caption("ai对战")

        ChessFrontMove(self.screen, ChessFrontInit(self.screen).chessboard, ChessBoard()).run(2)

    def check_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            return "start"  # 按下 ESC 键返回开始界面
        return "computer"





