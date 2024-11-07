import pygame
import sys
from image_button import ImageButton

# 初始化 pygame.mixer 模块
pygame.mixer.init()

# 加载移动声音

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
WOOD = (245, 245, 220)

chess_board_layer_width = 165
chess_board_layer_height = 115
chess_board_layer = pygame.Surface((880 - 2 * chess_board_layer_width, 840 - 2 * chess_board_layer_height))  # 840->720

# 偏移量用于将棋盘居中
offset_x = (SCREEN_SIZE[0] - BOARD_WIDTH) // 2 - chess_board_layer_width
offset_y = (SCREEN_SIZE[1] - BOARD_HEIGHT) // 2 - chess_board_layer_height

menu_layer_x = 500
menu_layer_y = 750
menu_layer = pygame.Surface((360, 50))
restart = ImageButton("../other_picture/restart.jpg", 0, 2, 90, 46,
                      transparency=230, layer_x=menu_layer_x, layer_y=menu_layer_y)
undo = ImageButton("../other_picture/undo.jpg", 100, 2, 90, 46,
                   transparency=230, layer_x=menu_layer_x, layer_y=menu_layer_y)
hint = ImageButton("../other_picture/hint.jpg", 200, 2, 90, 46,
                   transparency=230, layer_x=menu_layer_x, layer_y=menu_layer_y)
back = ImageButton("../other_picture/back.png", 0, 0, 100, 46,
                   transparency=230)

move_sound = pygame.mixer.Sound("../chess_mp3/move.mp3")



# 加载棋子图像
piece_images = {
    "red車": pygame.image.load("../chess_png/red_rook.png"),
    "red馬": pygame.image.load("../chess_png/red_knight.png"),
    "red相": pygame.image.load("../chess_png/red_elephant.png"),
    "red仕": pygame.image.load("../chess_png/red_advisor.png"),
    "red帅": pygame.image.load("../chess_png/red_king.png"),
    "red炮": pygame.image.load("../chess_png/red_cannon.png"),
    "red兵": pygame.image.load("../chess_png/red_pawn.png"),
    "black車": pygame.image.load("../chess_png/black_rook.png"),
    "black馬": pygame.image.load("../chess_png/black_knight.png"),
    "black象": pygame.image.load("../chess_png/black_elephant.png"),
    "black士": pygame.image.load("../chess_png/black_advisor.png"),
    "black将": pygame.image.load("../chess_png/black_king.png"),
    "black砲": pygame.image.load("../chess_png/black_cannon.png"),
    "black卒": pygame.image.load("../chess_png/black_pawn.png"),
}


class ChessFrontInit:
    def __init__(self, screen):
        self.chessboard = [[0 for _ in range(9)] for _ in range(10)]
        self.initialize_pieces()
        self.screen = screen

    def initialize_pieces(self):
        self.chessboard = [[0 for _ in range(9)] for _ in range(10)]
        self.chessboard[0] = ["red車", "red馬", "red相", "red仕", "red帅", "red仕", "red相", "red馬", "red車"]
        self.chessboard[2][1] = "red炮"
        self.chessboard[2][7] = "red炮"
        self.chessboard[3][0] = "red兵"
        self.chessboard[3][2] = "red兵"
        self.chessboard[3][4] = "red兵"
        self.chessboard[3][6] = "red兵"
        self.chessboard[3][8] = "red兵"

        self.chessboard[9] = ["black車", "black馬", "black象", "black士", "black将", "black士", "black象", "black馬",
                              "black車"]
        self.chessboard[7][1] = "black砲"
        self.chessboard[7][7] = "black砲"
        self.chessboard[6][0] = "black卒"
        self.chessboard[6][2] = "black卒"
        self.chessboard[6][4] = "black卒"
        self.chessboard[6][6] = "black卒"
        self.chessboard[6][8] = "black卒"

    def draw_chessboard(self):
        self.screen.fill(WOOD)  # 背景颜色为白色
        chess_board_layer.fill(WOOD)
        menu_layer.fill(WOOD)
        restart.draw_layer(menu_layer)
        undo.draw_layer(menu_layer)
        hint.draw_layer(menu_layer)
        back.draw(self.screen)
        # 绘制横线
        for row in range(10):
            pygame.draw.line(chess_board_layer, BLACK,
                             (offset_x, offset_y + row * CELL_SIZE),
                             (offset_x + BOARD_WIDTH, offset_y + row * CELL_SIZE), 2)

        # 绘制竖线
        for col in range(9):
            if col == 0 or col == 8:
                pygame.draw.line(chess_board_layer, BLACK,
                                 (offset_x + col * CELL_SIZE, offset_y),
                                 (offset_x + col * CELL_SIZE, offset_y + BOARD_HEIGHT), 2)
            else:
                pygame.draw.line(chess_board_layer, BLACK,
                                 (offset_x + col * CELL_SIZE, offset_y),
                                 (offset_x + col * CELL_SIZE, offset_y + BOARD_HEIGHT / 9 * 4), 2)
                pygame.draw.line(chess_board_layer, BLACK,
                                 (offset_x + col * CELL_SIZE, offset_y + BOARD_HEIGHT / 9 * 5),
                                 (offset_x + col * CELL_SIZE, offset_y + BOARD_HEIGHT), 2)

        # 绘制“楚河”和“汉界”之间的间隙
        pygame.draw.line(chess_board_layer, BLACK,
                         (offset_x, offset_y + 4 * CELL_SIZE),
                         (offset_x + BOARD_WIDTH, offset_y + 4 * CELL_SIZE), 2)
        pygame.draw.line(chess_board_layer, BLACK,
                         (offset_x, offset_y + 5 * CELL_SIZE),
                         (offset_x + BOARD_WIDTH, offset_y + 5 * CELL_SIZE), 2)

        # 绘制九宫格
        pygame.draw.line(chess_board_layer, BLACK,
                         (offset_x + 3 * CELL_SIZE, offset_y),
                         (offset_x + 5 * CELL_SIZE, offset_y + 2 * CELL_SIZE), 2)
        pygame.draw.line(chess_board_layer, BLACK,
                         (offset_x + 5 * CELL_SIZE, offset_y),
                         (offset_x + 3 * CELL_SIZE, offset_y + 2 * CELL_SIZE), 2)

        pygame.draw.line(chess_board_layer, BLACK,
                         (offset_x + 3 * CELL_SIZE, offset_y + 7 * CELL_SIZE),
                         (offset_x + 5 * CELL_SIZE, offset_y + 9 * CELL_SIZE), 2)
        pygame.draw.line(chess_board_layer, BLACK,
                         (offset_x + 5 * CELL_SIZE, offset_y + 7 * CELL_SIZE),
                         (offset_x + 3 * CELL_SIZE, offset_y + 9 * CELL_SIZE), 2)
        text = font.render("楚河          汉界", True, BLACK)
        text_rect = text.get_rect(center=(offset_x + BOARD_WIDTH // 2, offset_y + 4.5 * CELL_SIZE))
        chess_board_layer.blit(text, text_rect)

        self.screen.blit(chess_board_layer, (chess_board_layer_width, chess_board_layer_height))
        self.screen.blit(menu_layer, (500, 750))

    # 将点击的像素坐标转换为数组的行列坐标
    def get_board_pos(self, mouse_x, mouse_y):
        col = (mouse_x - offset_x + 30 - chess_board_layer_width) // CELL_SIZE
        row = (mouse_y - offset_y + 30 - chess_board_layer_height) // CELL_SIZE

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
        chess_board_layer.blit(glowing_surface, (center_x, center_y))
        self.screen.blit(chess_board_layer, (chess_board_layer_width, chess_board_layer_height))

    # 画出预测点
    def pridect_show(self, pos):
        for row in range(10):
            for col in range(9):
                if [row, col] in pos:
                    self.draw_glowing_point(row, col, color=(0, 255, 0), radius=10, transparency=128)

    # 在右侧居中显示当前回合的字样
    def draw_turn_info(self, turn, turn_len):
        turn_text = "当前回合"
        color = RED if turn == 0 else BLACK

        if turn_len == 0:
            return
        # 设置起始位置，使文本垂直居中在右侧
        start_x = SCREEN_SIZE[0] - 120  # 为数字预留空间
        start_y = (SCREEN_SIZE[1] // 2) - (len(turn_text) * 24) // 2  # 调整起始 y 位置实现居中

        # 逐个字符垂直排列
        for i, char in enumerate(turn_text):
            char_image = font.render(char, True, color)
            char_rect = char_image.get_rect(center=(start_x, start_y + i * 48))  # 每个字之间留一些间距
            self.screen.blit(char_image, char_rect)

        # 在 "当前回合" 右侧绘制数字
        num_image = font.render(str((turn_len + 1) // 2), True, color)
        num_rect = num_image.get_rect(center=(start_x + 60, start_y + (len(turn_text) - 1) * 24))  # 数字垂直居中对齐
        self.screen.blit(num_image, num_rect)

    def draw_piece(self):
        for row in range(10):
            for col in range(9):
                piece = self.chessboard[row][col]
                if piece:
                    piece_image = piece_images[piece]
                    piece_rect = piece_image.get_rect()
                    piece_rect.center = (offset_x + col * CELL_SIZE, offset_y + row * CELL_SIZE)
                    chess_board_layer.blit(piece_image, piece_rect)
                    self.screen.blit(chess_board_layer, (chess_board_layer_width, chess_board_layer_height))

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
                    chess_board_layer.blit(scaled_piece_image, piece_rect)
                    self.screen.blit(chess_board_layer, (chess_board_layer_width, chess_board_layer_height))

    # 显示红色方的文本
    def draw_text_red(self, text):
        text_image = font.render(text, True, RED)
        text_rect = text_image.get_rect(topleft=(20, 60))  # 将文本放在上方靠左
        # chess_board_layer.blit(text_image, text_rect)
        self.screen.blit(text_image, text_rect)

    def draw_text_chkmate(self, text):
        text_image = font.render(text, True, RED)
        text_rect = text_image.get_rect(topleft=(40, SCREEN_SIZE[1] / 2 - 20))  # 将文本放在上方靠左
        # chess_board_layer.blit(text_image, text_rect)
        self.screen.blit(text_image, text_rect)

    # 显示黑色方的文本
    def draw_text_black(self, text):
        text_image = font.render(text, True, BLACK)
        text_rect = text_image.get_rect(bottomleft=(20, SCREEN_SIZE[1] - 60))  # 将文本放在上方靠左
        # chess_board_layer.blit(text_image, text_rect)
        self.screen.blit(text_image, text_rect)

    # 初始化棋盘
    def initialize(self):
        self.draw_chessboard()
        self.initialize_pieces()
        self.draw_text_red("红方执棋")  # 绘制文本
        self.draw_text_black("黑方")  # 绘制文本
        self.draw_piece()
        return self.chessboard

    # 棋子移动后重新绘制棋盘
    # 重新绘制棋盘底格
    # 重新绘制棋子和双方文本提示
    def draw__(self, turn, turn_len):
        turn_str = [["执棋", ""], ["", "执棋"],
                    ["", "获胜"], ["获胜", ""]]
        self.draw_chessboard()
        self.draw_text_red("红方" + turn_str[turn][0])  # 绘制文本
        self.draw_text_black("黑方" + turn_str[turn][1])  # 绘制文本
        self.draw_turn_info(turn, turn_len)  # 绘制当前回合字样

    # 重新绘制完成移动后的棋盘
    def redraw(self, turn, last_pos, turn_len):
        self.draw__(turn, turn_len)
        self.draw_piece()
        self.draw_glowing_point(last_pos[0], last_pos[1], color=(255, 0, 0), radius=10, transparency=128)

    # 重新绘制完成移动后的棋盘
    def chosen_feedback(self, pos, turn, end_pos, last_pos, turn_len):
        self.draw__(turn, turn_len)
        self.draw_piece_scaled(pos, end_pos)
        self.pridect_show(end_pos)
        self.draw_glowing_point(last_pos[0], last_pos[1], color=(255, 0, 0), radius=10, transparency=128)

    def checkmate(self, turn, last_pos, turn_len):
        self.redraw(turn, last_pos, turn_len)
        self.draw_text_chkmate("将军")

    def animate_piece_move(self, start_x, start_y, end_x, end_y, piece_image, turn, turn_len):
        """
            实现棋子从起始位置到目标位置的动画
            """
        # 计算每一步的距离
        piece_image = piece_images[piece_image]
        delta_x = (end_x - start_x) * CELL_SIZE / 20  # 分10步完成移动
        delta_y = (end_y - start_y) * CELL_SIZE / 20

        current_x = start_x * CELL_SIZE + offset_x
        current_y = start_y * CELL_SIZE + offset_y
        target_x = end_x * CELL_SIZE + offset_x
        target_y = end_y * CELL_SIZE + offset_y

        temp_piece, self.chessboard[start_x][start_y] = self.chessboard[start_x][start_y], 0

        for _ in range(20):  # 分10步移动
            current_x += delta_x
            current_y += delta_y

            # 清空并重新绘制棋盘和其他元素
            self.screen.fill(WOOD)
            self.redraw(turn, (-100, -100), turn_len)
            piece_rect = piece_image.get_rect()
            piece_rect.center = (current_y, current_x)
            chess_board_layer.blit(piece_image, piece_rect)
            self.screen.blit(chess_board_layer, (chess_board_layer_width, chess_board_layer_height))

            pygame.display.flip()  # 刷新显示
            pygame.time.delay(3)  # 控制动画速度

        move_sound.play()
        self.chessboard[start_x][start_y] = temp_piece
        pygame.display.flip()
