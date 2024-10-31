import pygame
import sys

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

class StartPage:
    def __init__(self, screen):
        self.screen = screen
        self.background_image = pygame.image.load("../other_picture/start_page.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (880, 840))
        self.font = pygame.font.SysFont("华文隶书", 48)
        # 创建按钮
        self.button_doub = ImageButton("../other_picture/double_comp.png", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 60,
                                       transparency=180)
        self.button_ai = ImageButton("../other_picture/ai_comp.png", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 60,
                               transparency=180)


    def draw(self):
        # 绘制背景
        self.screen.blit(self.background_image, (0, 0))
        # 绘制按钮
        self.button_doub.draw(self.screen)
        self.button_ai.draw(self.screen)



    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # 检测是否点击了双人对战按钮
            if self.button_doub.is_clicked(mouse_pos):
                return "double"
            # 检测是否点击了人机对战按钮
            elif self.button_ai.is_clicked(mouse_pos):
                return "computer"
        return "start"








