from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board import Board
    from cell import Cell

class IMovementStrategy(ABC):
    @abstractmethod
    def can_move(self, start: 'Cell', end: 'Cell', board: 'Board' = None) -> bool:
        """Check if the piece can move from start to end cell."""
        pass