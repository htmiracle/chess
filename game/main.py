import pygame
import sys
from start_page import StartPage
from chess_front_main import DoublePage
from chess_front_main import AiPage

# 初始化 pygame
pygame.init()

# 设置屏幕大小
SCREEN_WIDTH = 880
SCREEN_HEIGHT = 840
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 设置标题
pygame.display.set_caption("开始界面")

# 创建页面实例
start_page = StartPage(screen)
doub_page = DoublePage(screen)
ai_page = AiPage(screen)

# 当前页面状态
current_page = "start"

# 游戏主循环
running = True
while running:
    button = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # 根据当前页面状态处理事件
        if current_page == "start":
            current_page, button = start_page.check_events(event)
            start_page.draw(button)
        elif current_page == "double":
            current_page = doub_page.check_events(event)
        elif current_page == "computer":
            current_page = ai_page.check_events(event)

    # 根据当前页面状态绘制内容
    if current_page == "double":
        doub_page.draw()
    elif current_page == "computer":
        ai_page.draw()

    # 更新屏幕
    pygame.display.flip()
