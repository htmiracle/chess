import pygame
import sys
from image_button import ImageButton

# 设置屏幕大小
SCREEN_WIDTH = 880
SCREEN_HEIGHT = 840
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 设置标题
pygame.display.set_caption("开始界面")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
RED = (255, 0, 0)


class StartPage:
    def __init__(self, screen):
        self.screen = screen
        self.background_image = pygame.image.load("../other_picture/start_page.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (880, 840))
        self.font = pygame.font.SysFont("华文隶书", 48)
        # 创建按钮
        self.button_doub = ImageButton("../other_picture/double_comp.png", SCREEN_WIDTH // 2 - 100,
                                       SCREEN_HEIGHT // 2 - 50, 200, 60,
                                       transparency=230)
        self.button_ai = ImageButton("../other_picture/ai_comp.png", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50,
                                     200, 60,
                                     transparency=230)
        self.button_ai_hard = ImageButton("../other_picture/ai_comp.png", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150,
                                     200, 60,
                                     transparency=230)

    def draw(self, button):
        # 绘制背景
        self.screen.blit(self.background_image, (0, 0))
        # 绘制按钮
        if button == "doub":
            self.button_doub.draw(self.screen, clicked=True)
        else:
            self.button_doub.draw(self.screen)
        if button == "ai":
            self.button_ai.draw(self.screen, clicked=True)
        else:
            self.button_ai.draw(self.screen)
        if button == "hard_ai":
            self.button_ai_hard.draw(self.screen, clicked=True)
        else:
            self.button_ai_hard.draw(self.screen)


    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.button_doub.is_clicked(mouse_pos):
                return "start", "doub"
            # 检测是否点击了人机对战按钮
            elif self.button_ai.is_clicked(mouse_pos):
                return "start", "ai"
            elif self.button_ai_hard.is_clicked(mouse_pos):
                return "start", "hard_ai"
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = event.pos
            # 检测是否点击了双人对战按钮
            if self.button_doub.is_clicked(mouse_pos):
                return "double", None
            # 检测是否点击了人机对战按钮
            elif self.button_ai.is_clicked(mouse_pos):
                return "computer", None
            elif self.button_ai_hard.is_clicked(mouse_pos):
                return "hard_ai", None
        return "start", None
