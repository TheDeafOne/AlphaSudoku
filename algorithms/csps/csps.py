'''
    A constraint satisfaction problem solver
'''
from .ac3 import AC3
import time
from board_logic.board import Board

class CSPS:
    '''
        constraint propagation and backtracking algorithm for solving sudoku boards
        
        ATTRIBUTES
        _board: unsolved sudoku board
        solved_board: solved sudoku board

        METHODS
        solve()
            returns solution to current board (solves if not already)
        
        search(group_board)
            searches for solution to given group_board and returns if found
        
        remove_value(group_board, cell_index, value)
            removes value from group_board at cell_index and runs propagation on remaining group values
        
        propagate(group_board, cell_index, value)
            runs ac3 on group board when value is set at cell_index in group_board
    '''
    def __init__(self, board, is_game_loop=False):
        if type(board) is str:
            board = Board(board)
        self._is_game_loop = is_game_loop
        self._next_step = False
        self._board = board.get_group_board()
        self.peer_indexes = board.peer_indexes
        self.unit_indexes = board.unit_indexes
        self.cell_indexes = board.cell_indexes
        self.solved_board = {}
    

    '''
        solve current board if not yet solved

        RETURNS
        solved board
    '''
    def solve(self): 
        # board not yet solved
        if len(self.solved_board) == 0:
            self.solved_board = self.search(self._board)
        return self.solved_board


    '''
        find board solution

        RETURNS
        solved board if solution could be found, false otherwise
    '''
    def search(self, group_board):
        # previous search failed
        if group_board is False:
            return False

        # all groups have an assigned value
        if all(len(group_board[cell_index]) == 1 for cell_index in self.cell_indexes):
            return group_board

        # smallest group heuristic
        _,sm_group_index = min((len(group_board[cell_index]), cell_index) for cell_index in self.cell_indexes if len(group_board[cell_index]) > 1)
        
        # recursive search and backtrack
        for value in group_board[sm_group_index]:
            solution = self.search(self.remove_value(group_board.copy(), sm_group_index, value))

            # solution found
            if solution:
                return solution
        
        # no solution found
        return False


    '''
        removes value from group at cell index and propagates according to remaining group values

        PARAMS
        group_board: current board state in backtracking stack
        cell_index: index of cell being set (e.g. A1)
        value: value being value being removed
    '''
    def remove_value(self, group_board, cell_index, value):
        # remove value from group and get remaining values
        group = group_board[cell_index].replace(value, '')
        self._board = group_board
        if self._is_game_loop:
            self._next_step = False
            while not self._next_step:
                time.sleep(0.1)
                

        # check that all possible next values are valid solutions
        for group_value in group:
            if not self.propagate(group_board, cell_index, group_value):
                return False
        return group_board
    

    '''
        runs ac3 on current board with new set value

        PARAMS
        group_board: current board state in backtracking stack
        cell_index: index of cell being set (e.g. A1)
        value: value being propagated on
        
        (group_board[A1] = 123 and value = 1, new group_board[A1] = 23, then run propagation on that)

        RETURNS
        propagated_board: if ac3 was successful, False otherwise
    '''
    def propagate(self, group_board, cell_index, value):
        # remove value from group at cell_index and set group board at cell index to new group
        group_board[cell_index] = group_board[cell_index].replace(value,'')

        # set up ac3 propagation and run on new group_board
        ac3 = AC3(group_board)
        propagated_board = ac3.ac3()

        if propagated_board:
            return propagated_board
        return False # ac3 found an inconsistency