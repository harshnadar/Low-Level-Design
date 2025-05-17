from cell import Cell
from typing import List
from color import Color
from pieces.pawn import Pawn
from pieces.piece import Piece

class Board:
    def __init__(self, size: int):
        self.size = size
        self.board = [[Cell(x,y) for y in range(size)] for x in range(size)]
        self.__initialize_board()

    def __initialize_board(self):
        self.__initialize_piece_row(0, Color.WHITE)
        self.__initialize_pawn_row(1, Color.WHITE)

        self.__initialize_piece_row(self.size-1, Color.BLACK)
        self.__initialize_pawn_row(self.size - 2, Color.BLACK)

    def __initialize_piece_row(self, row: int, color: Color):
        pass

    def __initialize_pawn_row(self, row: int, color: Color):
        for col in range(self.size):
            self.board[row][col].set_piece(Pawn(color))

    def get_piece(self, x: int, y: int) -> Piece:
        return self.board[x][y].get_piece()
        

    def draw_board(self):
        for row in self.board:
            for cell in row:
                piece = cell.get_piece()
                if piece is not None:
                    print(piece.get_color().name_str + piece.get_piece_type_str(), end='  ')
                else:
                    print('.', end='   ')
            print()
    

        



    