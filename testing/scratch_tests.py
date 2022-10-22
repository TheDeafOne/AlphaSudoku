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
    print(board.get_subgrids())
    board.display_board("large")
    # board.display_group_board()


def test_ac3():
    board = Board()
    # board.new_board(30,30)
    did_work = board.set_board('000130050800970001010008009050000960000064000001000070906087120072400000000003704')
    print(did_work)
    print(board.get_board_string())
    board.display_board("large")
    board.display_group_board()
    print()
    indexes = board.peer_indexes
    constraints = [(index, peer) for index in indexes for peer in indexes[index]]
    gb = board.get_group_board()
    
    ac3 = AC3(gb, constraints)
    

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

    
def test_genetic():
    genetic_solver = GeneticSolver()
    genetic_solver.run()
    


def group_board_setting():
    board1 = Board()
    board1.set_board('000130050800970001010008009050000960000064000001000070906087120072400000000003704')
    board1.display_group_board()

    val = board1.set_board_value('A1', '4')
    print(val)
    

def test_backtracking():
    import time
    start = time.perf_counter()
    board = Board()
    # board.new_board(23,23)
    board.set_board('000000000000000000000000000000000000000000000000000000000000000000000000000000400')
    # board.new_board(23,23)
    # board.display_group_board()
    csps = CSPS(board)
    b = csps.solve()
    end = time.perf_counter()
    print('val',end-start)
    board.set_board(b)
    board.display_board()
    
    # print(board.get_board_string())
    

if __name__ == '__main__':
    # test_board_grouping()
    test_genetic()


    pass