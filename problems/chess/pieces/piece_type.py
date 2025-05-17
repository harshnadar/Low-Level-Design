from enum import Enum

class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

    @property
    def name_str(self) -> str:
        """Return the name of the piece type."""
        return self.name[0].upper()