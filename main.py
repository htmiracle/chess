import pygame
import sys

# 初始化pygame
pygame.init()

# 设置棋盘大小
CELL_SIZE = 60  # 每个棋格的大小
BOARD_WIDTH = 8 * CELL_SIZE
BOARD_HEIGHT = 9 * CELL_SIZE
SCREEN_SIZE = (BOARD_WIDTH + 200, BOARD_HEIGHT + 200)
region_1 = pygame.Rect(100, 100, BOARD_WIDTH + 100, BOARD_HEIGHT + 100)

# 设置颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 创建窗口
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("中国象棋棋盘")

# 创建棋盘数组，0表示空位置
chessboard = [[0 for _ in range(9)] for _ in range(10)]

# 加载棋子图像
piece_images = {
    # "黑车": pygame.image.load("black_rook.png"),
    # "黑马": pygame.image.load("black_knight.png"),
    # "黑象": pygame.image.load("black_elephant.png"),
    # "黑士": pygame.image.load("black_advisor.png"),
    # "黑将": pygame.image.load("black_king.png"),
    # "黑炮": pygame.image.load("black_cannon.png"),
    # "黑卒": pygame.image.load("black_pawn.png"),
    "红车": pygame.image.load("red_rook.png"),
    "红马": pygame.image.load("red_knight.png"),
    "红相": pygame.image.load("red_elephant.png"),
    "红仕": pygame.image.load("red_advisor.png"),
    "红帅": pygame.image.load("red_king.png"),
    "红炮": pygame.image.load("red_cannon.png"),
    "红兵": pygame.image.load("red_pawn.png"),
}


# 初始化棋子位置
def initialize_pieces():
    # chessboard[0] = ["黑车", "黑马", "黑象", "黑士", "黑将", "黑士", "黑象", "黑马", "黑车"]
    # chessboard[2][1] = "黑炮"
    # chessboard[2][7] = "黑炮"
    # chessboard[3][0] = "黑卒"
    # chessboard[3][2] = "黑卒"
    # chessboard[3][4] = "黑卒"
    # chessboard[3][6] = "黑卒"
    # chessboard[3][8] = "黑卒"
    #
    chessboard[0] = ["红车", "红马", "红相", "红仕", "红帅", "红仕", "红相", "红马", "红车"]
    chessboard[2][1] = "红炮"
    chessboard[2][7] = "红炮"
    chessboard[3][0] = "红兵"
    chessboard[3][2] = "红兵"
    chessboard[3][4] = "红兵"
    chessboard[3][6] = "红兵"
    chessboard[3][8] = "红兵"


# 绘制棋盘函数
def draw_chessboard():
    screen.fill(WHITE)  # 背景颜色为白色

    # 绘制横线
    for row in range(10):
        pygame.draw.line(screen, BLACK, (0, row * CELL_SIZE), (BOARD_WIDTH, row * CELL_SIZE), 2)

    # 绘制竖线
    for col in range(9):
        pygame.draw.line(screen, BLACK, (col * CELL_SIZE, 0), (col * CELL_SIZE, BOARD_HEIGHT / 9 * 4), 2)
        pygame.draw.line(screen, BLACK, (col * CELL_SIZE, BOARD_HEIGHT / 9 * 5), (col * CELL_SIZE, BOARD_HEIGHT), 2)

    # 绘制“楚河”和“汉界”之间的间隙
    pygame.draw.line(screen, BLACK, (0, 4 * CELL_SIZE), (BOARD_WIDTH, 4 * CELL_SIZE), 2)
    pygame.draw.line(screen, BLACK, (0, 5 * CELL_SIZE), (BOARD_WIDTH, 5 * CELL_SIZE), 2)

    # 绘制九宫格
    pygame.draw.line(screen, BLACK, (3 * CELL_SIZE, 0), (5 * CELL_SIZE, 2 * CELL_SIZE), 2)
    pygame.draw.line(screen, BLACK, (5 * CELL_SIZE, 0), (3 * CELL_SIZE, 2 * CELL_SIZE), 2)

    pygame.draw.line(screen, BLACK, (3 * CELL_SIZE, 7 * CELL_SIZE), (5 * CELL_SIZE, 9 * CELL_SIZE), 2)
    pygame.draw.line(screen, BLACK, (5 * CELL_SIZE, 7 * CELL_SIZE), (3 * CELL_SIZE, 9 * CELL_SIZE), 2)

    # 绘制棋子
    for row in range(10):
        for col in range(9):
            piece = chessboard[row][col]
            if piece:
                piece_image = piece_images[piece]
                piece_rect = piece_image.get_rect()
                piece_rect.center = (col * CELL_SIZE - CELL_SIZE // 2, row * CELL_SIZE - CELL_SIZE // 2)
                screen.blit(piece_image, piece_rect.center)

    # 初始化棋子
    initialize_pieces()


# 将点击的像素坐标转换为数组的行列坐标
def get_board_pos(mouse_x, mouse_y):
    col = (mouse_x + 30) // CELL_SIZE
    row = (mouse_y + 30) // CELL_SIZE

    # 确保坐标在有效范围内
    if 0 <= col < 9 and 0 <= row < 10:
        return row, col
    else:
        return None


# 主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            board_pos = get_board_pos(mouse_x, mouse_y)
            if board_pos:
                row, col = board_pos
                print(f"点击位置：行 {row}, 列 {col}")
                #
                # 可以在这里进行对数组的操作，例如标记某个位置被点击
                # chessboard[row][col] = 1  # 例如将该位置标记为1，表示被点击过

    draw_chessboard()  # 绘制棋盘
    pygame.display.update()  # 更新显示

