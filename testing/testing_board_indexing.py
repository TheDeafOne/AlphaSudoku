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

    


def make_group_board(board):
    group_table=[]
    for i in range(9):
        group_table.append([[]] * 9)
        
    for row_idx, i in enumerate(board):
        possibilities = [p for p in range(1,10)]
        for col_idx, j in enumerate(i):
            if j == '0':
                new_list = list(set(possibilities)
                    .difference(row_vals(row_idx, col_idx, board))
                    .difference(col_vals(row_idx, col_idx, board))
                    .difference(block_vals(row_idx, col_idx, board)))
                group_table[row_idx][col_idx] = new_list
    return group_table


def row_vals(row, col, board):
    return set([val for val in board[row] if val != '0'])

def col_vals(row, col, board):
    return set([row[col] for row in board if row[col] != '0'])

def block_vals(row, col, board):
    start_row = 3*(row//3)
    start_col = 3*(col//3)
    vals = []
    for i in range(start_row, start_row+3):
        vals.extend([j for j in board[i][start_col:start_col+3] if j != '0'])
    return set(vals)


    

if __name__ == '__main__':
    # display_cells()
    # display_cell_units()
    # display_cell_peers()
    # try_set_board()
    # generate_board()
    

    # generator.generate_board(23,)
    # # generator.read_sudoku()
    # new_board = generator.generate_board(30,30)[0]

    # print(new_board.count('0'))
    # board.set_board(new_board)
    # val = board.get_group_board()
    # [print(row) for row in board.get_board_2D()]
    # [print(row, val[row]) for row in val]
    
    # print(board_indexes.get_cell_indexes())
    # [print(row) for row in board_indexes.get_peer_indexes()]

    pass