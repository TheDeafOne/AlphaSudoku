import sys, os
sys.path.append(os.path.join(sys.path[0], "../"))

from board_logic.board import Board
from board_logic.board_generator import BoardGenerator
from algorithms.csps.ac3 import AC3
from algorithms.csps.csps import CSPS

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
    print(board.get_subgrids())
    board.display_board("large")
    # board.display_group_board()

def test_ac3():
    board = Board()
    # board.new_board(30,30)
    board.set_board('000130050800970001010008009050000960000064000001000070906087120072400000000003704')
    print(board.get_board_string())
    board.display_board("large")
    print()
    indexes = board.get_peer_indexes()
    constraints = [(index, peer) for index in indexes for peer in indexes[index]]
    gb = board.get_group_board()
    ac3 = AC3(gb, constraints)
    

    board.display_group_board()
    new_gb = ac3.ac3()
    print()

    group_board_2D = [[]]
    for i, cell_index in enumerate(new_gb):
        group_board_2D[-1].append(list(new_gb[cell_index]))
        if (i + 1) % 9 == 0 and i != 80:
            group_board_2D.append([])

    for i, row in enumerate(group_board_2D):
        for j, val in enumerate(row):
            print("".join(val).ljust(board._max_group_length + 1, " "), end="")
            if (j + 1) % 3 == 0 and j != 8:
                print("|   ", end="")
        if (i + 1) % 3 == 0 and i != 8:
            print()
            print("-" * (board._max_group_length * 11), end="")
        print()

    
def test_backtracking():
    board = Board()
    board.set_board('000130050800970001010008009050000960000064000001000070906087120072400000000003704')
    csps = CSPS(board)
    csps.solve(board)
    # csps._good_board.display_board()

def board_setting():
    board = Board()
    board.set_board('000130050800970001010008009050000960000064000001000070906087120072400000000003704')
    print('should be 0')
    board.display_board()

    new_board = Board()
    new_board.set_board(board)
    print('set old board A1: 1, old board values should be A1:1')
    board.set_board_value('A1', '2')
    board.display_board()
    board.display_group_board()
    print('2d board\n',board.get_board_2D())
    print('board string\n',board.get_board_string())
    print('board\n',board.get_board())
    print('subgrids\n',board.get_subgrids())
    print('groups\n',board.get_groups())
    print('group board 2d\n', board.get_group_board_2D())
    

def group_board_setting():
    board1 = Board()
    board1.set_board('000130050800970001010008009050000960000064000001000070906087120072400000000003704')
    board1.display_group_board()

    val = board1.set_board_value('A1', '4')
    print(val)
    

def test_backtracking():
    board = Board()
    board.new_board(23,23)
    csps = CSPS(board)
    b = csps.solve()
    print(b)
    print(board.get_board_string())
    
    

def test_wild_backtracking():
    board = Board()
    board.new_board(30,30)
    csps = CSPS(board)
    csps.solve(board)
    print(board.get_board_string())


if __name__ == '__main__':
    # test_board_grouping()
    # test_ac3()
    # board_setting()
    # group_board_setting()
    test_backtracking()
    # test_wild_backtracking()

    pass