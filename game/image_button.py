import pygame
class ImageButton:
    def __init__(self, image_path, x, y, width, height, transparency=255, layer_x=0, layer_y=0):
        self.image = pygame.image.load(image_path)  # 加载按钮图片
        self.image = pygame.transform.scale(self.image, (width, height))  # 缩放图片
        self.image.set_alpha(transparency)  # 设置透明度 (0-255)
        self.rect = self.image.get_rect(topleft=(x, y))  # 设置按钮的位置和大小
        self.abs_rect = self.image.get_rect(topleft=(x+layer_x, y+layer_y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # 将图片绘制到屏幕

    def draw_layer(self, layer):
        layer.blit(self.image, self.rect)

    def is_clicked(self, mouse_pos):
        return self.abs_rect.collidepoint(mouse_pos)  # 检测是否点击了按钮