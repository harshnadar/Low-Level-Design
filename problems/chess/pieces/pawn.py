from pieces.piece import Piece
from color import Color
from movement_strategy.pawn_movement_strategy import PawnMovementStrategy
from pieces.piece_type import PieceType

class Pawn(Piece):
    def __init__(self, color: Color):
        super().__init__(color=color, movement_strategy=PawnMovementStrategy(), piece_type=PieceType.PAWN)

    def can_move(self, start_x: int, start_y: int, end_x: int, end_y: int) -> bool:
        pass

    
        