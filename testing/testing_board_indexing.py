import sys, os
sys.path.append(os.path.join(sys.path[0], "../"))

from board_logic.board_indexing import BoardIndexing
from board_logic.board import Board
from board_logic.board_generator import BoardGenerator

board_indexes = BoardIndexing()
board = Board()
generator = BoardGenerator()

def display_cells():
    print(board_indexes.get_cell_indexes())

def display_cell_units():
    print(board_indexes.get_unit_indexes())

def display_cell_peers():
    print(board_indexes.get_peer_indexes())

def try_set_board():
    did_set = board.set_board('001')
    assert did_set == False
    did_set = board.set_board('00000000000000001000000000000000100000000000-000000000009000000000000000a00000000')
    print(board.get_board_2D())

def generate_board():
    print(generator.generate_board())

    

if __name__ == '__main__':
    

    pass