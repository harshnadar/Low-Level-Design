from game import Game
from player import Player
from board import Board
from color import Color

def func():
    player1 = Player('alice', Color.WHITE)
    player2 = Player('bob', Color.BLACK)
    board = Board(8)
    game = Game(player1, player2, board)
    game.draw_board()

if __name__ == "__main__":
    func()