from movement_strategy.i_movement_strategy import IMovementStrategy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board import Board
    from cell import Cell

class RookMovementStrategy(IMovementStrategy):
    def can_move(self, start: 'Cell', end: 'Cell', board: 'Board' = None) -> bool:
        return True