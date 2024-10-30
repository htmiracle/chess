class ChessPiece:
    def __init__(self, name, color, position):
        self.name = name  # 棋子的名字
        self.color = color  # 棋子的颜色，红色或者黑色
        self.position = position  # 棋子的位置

    def move(self, new_position):
        self.position = new_position
