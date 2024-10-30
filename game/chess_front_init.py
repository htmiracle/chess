import pygame
import sys

# 初始化 pygame
pygame.init()
# 初始化字体模块
pygame.font.init()

font = pygame.font.SysFont("华文隶书", 48)  # 设置字体大小

# 设置棋盘大小
CELL_SIZE = 60  # 每个棋格的大小
BOARD_WIDTH = 8 * CELL_SIZE
BOARD_HEIGHT = 9 * CELL_SIZE
SCREEN_SIZE = (BOARD_WIDTH + 400, BOARD_HEIGHT + 300)

# 设置颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (178, 34, 34)
WOOD = (245, 222, 179)

# 偏移量用于将棋盘居中
offset_x = (SCREEN_SIZE[0] - BOARD_WIDTH) // 2
offset_y = (SCREEN_SIZE[1] - BOARD_HEIGHT) // 2

# 加载棋子图像
piece_images = {
    "红车": pygame.image.load("../chess_png/red_rook.png"),
    "红马": pygame.image.load("../chess_png/red_knight.png"),
    "红相": pygame.image.load("../chess_png/red_elephant.png"),
    "红仕": pygame.image.load("../chess_png/red_advisor.png"),
    "红帅": pygame.image.load("../chess_png/red_king.png"),
    "红炮": pygame.image.load("../chess_png/red_cannon.png"),
    "红兵": pygame.image.load("../chess_png/red_pawn.png"),
    "黑车": pygame.image.load("../chess_png/black_rook.png"),
    "黑马": pygame.image.load("../chess_png/black_knight.png"),
    "黑象": pygame.image.load("../chess_png/black_elephant.png"),
    "黑士": pygame.image.load("../chess_png/black_advisor.png"),
    "黑将": pygame.image.load("../chess_png/black_king.png"),
    "黑炮": pygame.image.load("../chess_png/black_cannon.png"),
    "黑卒": pygame.image.load("../chess_png/black_pawn.png"),
}


class ChessFrontInit:
    def __init__(self, screen):
        self.chessboard = [[0 for _ in range(9)] for _ in range(10)]
        self.screen = screen

    def initialize_pieces(self):
        self.chessboard = [[0 for _ in range(9)] for _ in range(10)]
        self.chessboard[0] = ["红车", "红马", "红相", "红仕", "红帅", "红仕", "红相", "红马", "红车"]
        self.chessboard[2][1] = "红炮"
        self.chessboard[2][7] = "红炮"
        self.chessboard[3][0] = "红兵"
        self.chessboard[3][2] = "红兵"
        self.chessboard[3][4] = "红兵"
        self.chessboard[3][6] = "红兵"
        self.chessboard[3][8] = "红兵"

        self.chessboard[9] = ["黑车", "黑马", "黑象", "黑士", "黑将", "黑士", "黑象", "黑马", "黑车"]
        self.chessboard[7][1] = "黑炮"
        self.chessboard[7][7] = "黑炮"
        self.chessboard[6][0] = "黑卒"
        self.chessboard[6][2] = "黑卒"
        self.chessboard[6][4] = "黑卒"
        self.chessboard[6][6] = "黑卒"
        self.chessboard[6][8] = "黑卒"

    def draw_chessboard(self):
        self.screen.fill(WHITE)  # 背景颜色为白色

        # 绘制横线
        for row in range(10):
            pygame.draw.line(self.screen, BLACK,
                             (offset_x, offset_y + row * CELL_SIZE),
                             (offset_x + BOARD_WIDTH, offset_y + row * CELL_SIZE), 2)

        # 绘制竖线
        for col in range(9):
            pygame.draw.line(self.screen, BLACK,
                             (offset_x + col * CELL_SIZE, offset_y),
                             (offset_x + col * CELL_SIZE, offset_y + BOARD_HEIGHT / 9 * 4), 2)
            pygame.draw.line(self.screen, BLACK,
                             (offset_x + col * CELL_SIZE, offset_y + BOARD_HEIGHT / 9 * 5),
                             (offset_x + col * CELL_SIZE, offset_y + BOARD_HEIGHT), 2)

        # 绘制“楚河”和“汉界”之间的间隙
        pygame.draw.line(self.screen, BLACK,
                         (offset_x, offset_y + 4 * CELL_SIZE),
                         (offset_x + BOARD_WIDTH, offset_y + 4 * CELL_SIZE), 2)
        pygame.draw.line(self.screen, BLACK,
                         (offset_x, offset_y + 5 * CELL_SIZE),
                         (offset_x + BOARD_WIDTH, offset_y + 5 * CELL_SIZE), 2)

        # 绘制九宫格
        pygame.draw.line(self.screen, BLACK,
                         (offset_x + 3 * CELL_SIZE, offset_y),
                         (offset_x + 5 * CELL_SIZE, offset_y + 2 * CELL_SIZE), 2)
        pygame.draw.line(self.screen, BLACK,
                         (offset_x + 5 * CELL_SIZE, offset_y),
                         (offset_x + 3 * CELL_SIZE, offset_y + 2 * CELL_SIZE), 2)

        pygame.draw.line(self.screen, BLACK,
                         (offset_x + 3 * CELL_SIZE, offset_y + 7 * CELL_SIZE),
                         (offset_x + 5 * CELL_SIZE, offset_y + 9 * CELL_SIZE), 2)
        pygame.draw.line(self.screen, BLACK,
                         (offset_x + 5 * CELL_SIZE, offset_y + 7 * CELL_SIZE),
                         (offset_x + 3 * CELL_SIZE, offset_y + 9 * CELL_SIZE), 2)

    # 将点击的像素坐标转换为数组的行列坐标
    def get_board_pos(self, mouse_x, mouse_y):
        col = (mouse_x - offset_x + 30) // CELL_SIZE
        row = (mouse_y - offset_y + 30) // CELL_SIZE

        # 确保坐标在有效范围内
        if 0 <= col < 9 and 0 <= row < 10:
            return row, col
        else:
            return None

    # 画一个透明圆
    def draw_glowing_point(self, row, col, color=(0, 255, 0), radius=10, transparency=128):
        # 创建一个支持 Alpha 通道的透明表面
        glowing_surface = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)

        # 在该透明表面上绘制圆形
        pygame.draw.circle(glowing_surface, color + (transparency,), (radius, radius), radius)

        # 计算荧光点的中心位置（在格子的顶点）
        center_x = offset_x + col * CELL_SIZE - radius
        center_y = offset_y + row * CELL_SIZE - radius

        # 将具有透明度的表面绘制到屏幕上
        self.screen.blit(glowing_surface, (center_x, center_y))

    # 画出预测点
    def pridect_show(self, pos):
        for row in range(10):
            for col in range(9):
                if [row, col] in pos:
                    self.draw_glowing_point(row, col, color=(0, 255, 0), radius=10, transparency=128)

    def draw_piece(self):
        for row in range(10):
            for col in range(9):
                piece = self.chessboard[row][col]
                if piece:
                    piece_image = piece_images[piece]
                    piece_rect = piece_image.get_rect()
                    piece_rect.center = (offset_x + col * CELL_SIZE, offset_y + row * CELL_SIZE)
                    self.screen.blit(piece_image, piece_rect)

    def draw_piece_scaled(self, pos, end_pos):
        for row in range(10):
            for col in range(9):
                piece = self.chessboard[row][col]
                if piece:
                    piece_image = piece_images[piece]
                    if pos[0] == row and pos[1] == col:
                        scaled_piece_image = pygame.transform.scale(piece_image, (CELL_SIZE - 15, CELL_SIZE - 15))
                    else:
                        scaled_piece_image = pygame.transform.scale(piece_image, (CELL_SIZE, CELL_SIZE))  # 将图片缩放
                    piece_rect = scaled_piece_image.get_rect()
                    piece_rect.center = (offset_x + col * CELL_SIZE, offset_y + row * CELL_SIZE)
                    self.screen.blit(scaled_piece_image, piece_rect)

    # 显示红色方的文本
    def draw_text_red(self, text):
        text_image = font.render(text, True, RED)
        text_rect = text_image.get_rect(topleft=(180, 60))  # 将文本放在上方靠左
        self.screen.blit(text_image, text_rect)

    def draw_text_chkmate(self, text):
        text_image = font.render(text, True, RED)
        text_rect = text_image.get_rect(topleft=(0, 0))  # 将文本放在上方靠左
        self.screen.blit(text_image, text_rect)

    # 显示黑色方的文本
    def draw_text_black(self, text):
        text_image = font.render(text, True, BLACK)
        text_rect = text_image.get_rect(bottomleft=(180, SCREEN_SIZE[1] - 60))  # 将文本放在上方靠左
        self.screen.blit(text_image, text_rect)

    # 初始化棋盘
    def initialize(self):
        self.draw_chessboard()
        self.initialize_pieces()
        self.draw_text_red("红方执棋——————")  # 绘制文本
        self.draw_text_black("黑方")  # 绘制文本
        self.draw_piece()
        return self.chessboard

    # 棋子移动后重新绘制棋盘
    # 重新绘制棋盘底格
    # 重新绘制棋子和双方文本提示
    def draw__(self, turn):
        turn_str = [["执棋——————", ""], ["", "执棋——————"],
                    ["", "获胜"], ["获胜", ""]]
        self.screen.fill(WHITE)
        self.draw_chessboard()
        self.draw_text_red("红方" + turn_str[turn][0])  # 绘制文本
        self.draw_text_black("黑方" + turn_str[turn][1])  # 绘制文本

    # 重新绘制完成移动后的棋盘
    def redraw(self, turn, last_pos):
        self.draw__(turn)
        self.draw_piece()
        self.draw_glowing_point(last_pos[0], last_pos[1], color=(255, 0, 0), radius=10, transparency=128)

    # 重新绘制完成移动后的棋盘
    def chosen_feedback(self, pos, turn, end_pos, last_pos):
        self.draw__(turn)
        self.draw_piece_scaled(pos, end_pos)
        self.pridect_show(end_pos)
        self.draw_glowing_point(last_pos[0], last_pos[1], color=(255, 0, 0), radius=10, transparency=128)

    def checkmate(self, turn, last_pos):
        self.redraw(turn, last_pos)
        self.draw_text_chkmate("将军")