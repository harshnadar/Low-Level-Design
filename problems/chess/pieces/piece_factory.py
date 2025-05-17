from pieces.piece_type import PieceType
from color import Color
from pieces.pawn import Pawn
from pieces.rook import Rook

class PieceFactory:
    def create_piece(piece_type: PieceType, color: Color):
        if(piece_type == PieceType.PAWN):
            return Pawn(color)
        if(piece_type == PieceType.ROOK):
            return Rook(color)