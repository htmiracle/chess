class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def make_move(self, start_pos, end_pos, board, logic):
        piece = board.get_piece(start_pos)
        if piece and piece.color == self.color:
            if logic.is_valid_move(piece, end_pos):
                board.move_piece(start_pos, end_pos)
                return True
        return False
