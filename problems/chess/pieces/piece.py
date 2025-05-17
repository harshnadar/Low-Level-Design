from abc import ABC, abstractmethod
from color import Color
from movement_strategy.i_movement_strategy import IMovementStrategy
from pieces.piece_type import PieceType


class Piece(ABC):
    def __init__(self, color: Color, movement_strategy: IMovementStrategy = None, piece_type: PieceType = None):
        self.color = color
        self.is_alive = True
        self.movement_strategy: IMovementStrategy = None  # Placeholder for movement strategy
        self.piece_type = piece_type

    @abstractmethod
    def can_move(self, start_x: int, start_y: int, end_x: int, end_y) -> bool:
        """Check if the piece can move from start to end cell."""
        pass

    def get_color(self) -> Color:
        """Get the color of the piece."""
        return self.color
    
    def is_alive(self)-> bool:
        """Check if the piece is alive."""
        return self.is_alive
    
    def set_alive(self, alive: bool) -> None:
        """Set the alive status of the piece."""
        self.is_alive = alive

    def get_piece_type(self) -> PieceType:
        """Get the type of the piece."""
        return self.piece_type
    
    def get_piece_type_str(self) -> str:
        if self.piece_type is not None:
            return self.piece_type.name_str
        return ""


    

    

    
