import pygame
from chess_front_init import ChessFrontInit
from chess_front_move import ChessFrontMove
from chess_board import ChessBoard

# 初始化 Pygame
pygame.init()

# 设置棋盘大小
CELL_SIZE = 60  # 每个棋格的大小
BOARD_WIDTH = 8 * CELL_SIZE
BOARD_HEIGHT = 9 * CELL_SIZE
SCREEN_SIZE = (BOARD_WIDTH + 400, BOARD_HEIGHT + 300)

# 创建窗口
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("中国象棋棋盘")

ChessFrontMove(screen, ChessFrontInit(screen).chessboard, ChessBoard()).run()

