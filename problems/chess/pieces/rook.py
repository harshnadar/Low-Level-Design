from color import Color
from pieces.piece import Piece
from movement_strategy.rook_movement_strategy import RookMovementStrategy
from pieces.piece_type import PieceType

class Rook(Piece):
    def __init__(self, color: Color):
        super().__init__(color = color, movement_strategy=RookMovementStrategy(), piece_type=PieceType.ROOK)

    def can_move(self, start_x: int, start_y: int, end_x: int, end_y: int) -> bool:
        pass
