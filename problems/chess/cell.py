from pieces.piece import Piece

class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.piece: Piece = None 

    def set_piece(self, piece: Piece) -> None:
        """Set the piece on the cell."""
        self.piece = piece

    def get_piece(self) -> Piece | None:
        """Get the piece on the cell."""
        return self.piece
    

