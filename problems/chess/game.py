from player import Player
from board import Board

class Game:
    def __init__(self, player1: Player, player2: Player, board: Board):
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.current_player = player1

    def switch_turn(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def draw_board(self):
        self.board.draw_board()