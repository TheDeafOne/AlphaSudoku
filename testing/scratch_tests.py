import sys, os
sys.path.append(os.path.join(sys.path[0], "../"))

from board_logic.board import Board
from board_logic.board_generator import BoardGenerator
from algorithms.genetic.genetic import GeneticSolver

board = Board()
generator = BoardGenerator()

def try_set_board():
    did_set = board.set_board('001')
    assert did_set == False
    did_set = board.set_board('00000000000000001000000000000000100000000000-000000000009000000000000000a00000000')
    print(board.get_board_2D())

def generate_board():
    print(generator.generate_board())

def test_board_grouping():
    nb = generator.generate_board()
    board.set_board(nb)
    board.display_board("large")
    board.display_group_board()
    
def test_genetic():
    genetic_solver = GeneticSolver()
    genetic_solver.run()
    
    

if __name__ == '__main__':
    # test_board_grouping()
    test_genetic()


    pass