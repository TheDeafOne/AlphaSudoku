import sys, os
import csv
import time
sys.path.append(os.path.join(sys.path[0], "../"))

from board_logic.board import Board
from board_logic.board_generator import BoardGenerator
from algorithms.genetic.genetic import GeneticSolver
from algorithms.genetic.hybrid import HybridSolver
from algorithms.sa.sa import SASolver
from algorithms.csps.csps import CSPS
board = Board()
generator = BoardGenerator()

def try_set_board():
    did_set = board.set_board('001')
    assert did_set == False
    did_set = board.set_board('00000000000000001000000000000000100000000000-000000000009000000000000000a00000000')
    print(board.get_board_2D())

def generate_board():
    print(len(generator.generate_board().strip()))

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

def test_sa():
    sa_solver = HybridSolver()
    sa_solver.run()
    


def group_board_setting():
    board1 = Board()
    board1.set_board('000130050800970001010008009050000960000064000001000070906087120072400000000003704')
    board1.display_group_board()

    val = board1.set_board_value('A1', '4')
    print(val)
    

def test_backtracking():
    start = time.perf_counter()
    board = Board()
    # board.new_board(17,17)
    # board.set_board('.....6....59.....82....8....45........3........6..3.54...325..6..................')
    board.display_group_board()
    csps = CSPS(board)
    b = csps.solve()
    # print(b)
    end = time.perf_counter()
    print('val',end-start)
    board.set_board(b)
    board.display_board()
    
    # print(board.get_board_string())


def write_solution_data():
    file = open('backtracking-data.csv','w',newline='')
    file2 = open('bad-times.csv','w',newline='')
    badWriter = csv.writer(file2)
    badWriter.writerow(['clues','solve time', 'board'])
    writer = csv.writer(file)
    writer.writerow(['clues','solve time'])

    runtimes = 1000

    bd = Board()
    for i in range(17,80):
        print(i)
        for j in range(runtimes):
            if j % 10 == 0:
                print(j/runtimes)
            bd.new_board(i,i)
            csps = CSPS(bd)

            start = time.perf_counter()
            csps.solve()
            end = time.perf_counter()
            tm = end-start
            if tm > 2:
                badWriter.writerow([i,tm,bd.get_board_string()])

            writer.writerow([i,tm])




if __name__ == '__main__':
    # test_board_grouping()
    # test_sa()
    print(generator.generate_board())

    pass